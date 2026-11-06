"""Backtest réaliste d'une allocation, sans regard vers l'avenir (walk-forward).

À chaque date de rééquilibrage (dernière séance du mois, du trimestre...), la décision est prise à la
clôture avec les seuls rendements des ``fenetre`` séances précédentes. Elle devient des ordres, exécutés
selon les règles du marché (``marches.Regles``), les mêmes que les moteurs de BRVM Analytics et de
FinanceMatrix :

1. **Transmission** : exécution au plus tôt à la clôture de la séance suivante, et seulement une séance où
   le titre s'échange (volume positif).
2. **Participation limitée** : au plus ``participation`` des titres échangés dans la séance ; le reste
   attend les séances suivantes, jusqu'au rééquilibrage suivant qui le remplace.
3. **Couverture des achats** : un ordre d'achat bloque sa provision (cours + ``marge_provision``, frais
   compris) ; il n'est financé que par la trésorerie disponible. Une vente ne finance un achat qu'après
   son règlement.
4. **Règlement-livraison à J+R** : espèces d'une vente et titres achetés disponibles à J+R ; on ne revend
   pas des titres pas encore livrés.
5. **Frais** sur chaque achat et chaque vente ; quantités entières ; ni découvert ni levier.
6. **Dividendes** nets, cohérents avec les cours : droit acquis pour les titres détenus la veille du
   détachement (livrés ou à recevoir), versés à la date de paiement (au détachement si elle manque).
7. **Valeur** = trésorerie libre + provisions + créances + titres (livrés et à recevoir) × dernier cours.

Seuils : un écart de poids inférieur à ``tolerance`` n'est pas corrigé ; aucun ordre sous ``ordre_min``.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Callable

import numpy as np
import pandas as pd

from .marches import Regles
from .optimisation import SEANCES_PAR_AN, EchecOptimisation

FREQUENCES = {"Mensuel": 1, "Trimestriel": 3, "Semestriel": 6, "Annuel": 12}   # mois par période


@dataclass
class Reglages:
    capital: float
    debut: pd.Timestamp
    fin: pd.Timestamp
    frequence: str = "Trimestriel"
    fenetre: int = 252                 # séances d'historique pour chaque décision
    min_observations: float = 0.6      # part minimale de séances cotées dans la fenêtre pour qu'un titre entre
    tolerance: float = 0.01            # écart de poids non corrigé
    ordre_min: float = 0.0             # montant minimal d'un ordre
    dividendes: bool = True
    taux_sans_risque: float = 0.03


@dataclass
class Resultat:
    valeur: pd.Series
    operations: pd.DataFrame
    poids: pd.DataFrame                # poids cibles à chaque rééquilibrage
    frais: float
    dividendes: float
    alertes: list[str] = field(default_factory=list)
    montant_demande: float = 0.0       # montant des ordres transmis
    montant_execute: float = 0.0


def dates_reequilibrage(seances: pd.DatetimeIndex, frequence: str) -> pd.DatetimeIndex:
    """Dernière séance de chaque période (mois, trimestre, semestre ou année)."""
    mois_par_periode = FREQUENCES[frequence]
    periode = seances.year * 12 + (seances.month - 1) // mois_par_periode
    return pd.DatetimeIndex(pd.Series(seances, index=seances).groupby(periode).max().sort_values().values)


def _rendements_fenetre(cours: pd.DataFrame, fin: int, fenetre: int, min_obs: float) -> pd.DataFrame:
    """Rendements des ``fenetre`` séances jusqu'à ``fin`` incluse, titres assez cotés dans la fenêtre."""
    bloc = cours.iloc[max(0, fin - fenetre):fin + 1]
    cotes = bloc.notna().mean()
    retenus = cotes[(cotes >= min_obs) & bloc.iloc[-1].notna()].index
    if len(retenus) == 0:
        return pd.DataFrame()
    r = bloc[retenus].ffill().pct_change(fill_method=None).iloc[1:]
    return r.dropna(axis=1, how="any").loc[:, lambda d: d.std() > 0]


def executer(cours: pd.DataFrame, volumes: pd.DataFrame, seances: pd.DatetimeIndex,
             allocation: Callable[[pd.DataFrame], pd.Series], regles: Regles, reglages: Reglages,
             dividendes: pd.DataFrame | None = None) -> Resultat:
    """Simule l'allocation séance par séance.

    ``cours`` / ``volumes`` : une colonne par titre (NaN : pas de cotation) ; ``seances`` : calendrier du
    marché. ``allocation(rendements)`` rend des poids (somme <= 1) ; une ``EchecOptimisation`` garde
    l'allocation précédente.
    """
    seances = seances[(seances <= reglages.fin)]
    cal = seances[seances >= reglages.debut]
    if len(cal) < 2:
        raise ValueError("Période trop courte.")
    historique = cours.reindex(seances)
    vol = volumes.reindex(index=seances, columns=historique.columns).fillna(0.0)
    cl = historique.to_numpy(float)
    vl = vol.to_numpy(float)
    dernier = historique.ffill().to_numpy(float)
    titres = list(historique.columns)
    col = {t: j for j, t in enumerate(titres)}
    i0 = int(seances.get_indexer([cal[0]])[0])
    n = len(seances)
    R, f, part, marge = regles.reglement, regles.frais, regles.participation, regles.marge_provision
    reeq = set(dates_reequilibrage(cal, reglages.frequence))

    # Dividendes : {indice de la séance de détachement: [(colonne, montant, indice de paiement)]}
    a_detacher: dict[int, list[tuple[int, float, int]]] = {}
    if reglages.dividendes and dividendes is not None and len(dividendes):
        for x in dividendes.itertuples():
            if x.Ticker not in col or pd.isna(x.Date_Detachement):
                continue
            k = int(seances.searchsorted(pd.Timestamp(x.Date_Detachement)))
            if k <= i0 or k >= n:
                continue
            paiement = x.Date_Paiement if pd.notna(x.Date_Paiement) else x.Date_Detachement
            kp = max(k, int(seances.searchsorted(pd.Timestamp(paiement))))
            a_detacher.setdefault(k, []).append((col[x.Ticker], float(x.Montant), kp))

    tresorerie = float(reglages.capital)
    livres = np.zeros(len(titres))                 # titres livrés
    a_livrer: list[tuple[int, int, float]] = []    # (séance de livraison, colonne, quantité)
    creances: list[tuple[int, float]] = []         # (séance de règlement, montant)
    ordres: dict[int, dict] = {}                   # colonne -> {"sens", "reste", "provision"}
    operations, poids_hist, alertes, valeurs = [], {}, [], []
    frais_total = div_total = demande = execute = 0.0
    poids_courants: pd.Series | None = None

    def quantite_totale() -> np.ndarray:
        q = livres.copy()
        for _, j, qt in a_livrer:
            q[j] += qt
        return q

    def liberer_ordres() -> None:
        nonlocal tresorerie
        for o in ordres.values():
            tresorerie += o.get("provision", 0.0)
        ordres.clear()

    for i in range(i0, n):
        jour = seances[i]
        # 1. Règlements et livraisons échus
        tresorerie += sum(m for k, m in creances if k <= i)
        creances = [(k, m) for k, m in creances if k > i]
        for k, j, qt in [x for x in a_livrer if x[0] <= i]:
            livres[j] += qt
        a_livrer = [x for x in a_livrer if x[0] > i]

        # 2. Dividendes détachés aujourd'hui : droit sur les titres détenus hier soir
        for j, montant, kp in a_detacher.get(i, []):
            q = quantite_totale()[j]
            if q > 0:
                total = q * montant
                div_total += total
                if kp <= i:
                    tresorerie += total
                else:
                    creances.append((kp, total))

        # 3. Exécution des ordres transmis (ventes d'abord, puis achats)
        if ordres:
            # Achats : compléter les provisions avec la trésorerie libérée, au prorata des besoins
            besoins = {j: o["reste"] * dernier[i - 1, j] * (1 + marge) * (1 + f) - o["provision"]
                       for j, o in ordres.items() if o["sens"] == "achat"}
            besoins = {j: b for j, b in besoins.items() if b > 0}
            total_besoin = sum(besoins.values())
            if total_besoin > 0 and tresorerie > 0:
                ratio = min(1.0, tresorerie / total_besoin)
                for j, b in besoins.items():
                    ordres[j]["provision"] += b * ratio
                    tresorerie -= b * ratio
            for sens in ("vente", "achat"):
                for j, o in list(ordres.items()):
                    if o["sens"] != sens or not (vl[i, j] > 0 and np.isfinite(cl[i, j])):
                        continue
                    prix = cl[i, j]
                    plafond = math.floor(part * vl[i, j]) if part > 0 else o["reste"]
                    if sens == "vente":
                        q = min(o["reste"], livres[j], plafond)
                    else:
                        q = min(o["reste"], plafond, math.floor(o["provision"] / (prix * (1 + f))))
                    if q <= 0:
                        continue
                    montant = q * prix
                    frais = montant * f
                    frais_total += frais
                    execute += montant
                    if sens == "vente":
                        livres[j] -= q
                        creances.append((i + R, montant - frais))
                    else:
                        o["provision"] -= montant + frais
                        a_livrer.append((i + R, j, q))
                    o["reste"] -= q
                    operations.append({"Date": jour, "Titre": titres[j], "Sens": sens.capitalize(), "Quantité": q,
                                       "Cours": prix, "Montant": montant, "Frais": frais})
                    if o["reste"] <= 0:
                        tresorerie += o.get("provision", 0.0)
                        del ordres[j]
            # Livraison et règlement le jour même quand R = 0 (marché sans frictions)
            if R == 0:
                tresorerie += sum(m for k, m in creances if k <= i)
                creances = [(k, m) for k, m in creances if k > i]
                for k, j, qt in [x for x in a_livrer if x[0] <= i]:
                    livres[j] += qt
                a_livrer = [x for x in a_livrer if x[0] > i]

        # 4. Valeur à la clôture
        q = quantite_totale()
        titres_valeur = float(np.nansum(q * np.nan_to_num(dernier[i], nan=0.0)))
        provisions = sum(o.get("provision", 0.0) for o in ordres.values())
        valeur = tresorerie + provisions + sum(m for _, m in creances) + titres_valeur
        valeurs.append(valeur)

        # 5. Décision à la clôture d'une date de rééquilibrage
        if jour in reeq and i < n - 1:
            rendements = _rendements_fenetre(historique, i, reglages.fenetre, reglages.min_observations)
            try:
                if rendements.shape[1] < 2:
                    raise EchecOptimisation("moins de deux titres assez cotés sur la fenêtre")
                poids = allocation(rendements).reindex(titres).fillna(0.0).clip(lower=0)
                if poids.sum() > 1:
                    poids = poids / poids.sum()
                poids_courants = poids
            except EchecOptimisation as erreur:
                alertes.append(f"{jour:%d/%m/%Y} : allocation précédente conservée ({erreur}).")
                if poids_courants is None:
                    continue
                poids = poids_courants
            poids_hist[jour] = poids
            liberer_ordres()
            prix = dernier[i]
            for j, t in enumerate(titres):
                if not np.isfinite(prix[j]) or prix[j] <= 0:
                    continue
                cible = math.floor(poids.iloc[j] * valeur / (prix[j] * (1 + f)))
                ecart = cible - q[j]
                montant = abs(ecart) * prix[j]
                if ecart == 0 or montant < reglages.ordre_min or montant < reglages.tolerance * valeur:
                    continue
                if ecart < 0:
                    ordres[j] = {"sens": "vente", "reste": -ecart, "provision": 0.0}
                else:
                    ordres[j] = {"sens": "achat", "reste": ecart, "provision": 0.0}
                demande += montant

    valeur = pd.Series(valeurs, index=seances[i0:n], name="Valeur")
    colonnes = ["Date", "Titre", "Sens", "Quantité", "Cours", "Montant", "Frais"]
    return Resultat(valeur=valeur, operations=pd.DataFrame(operations, columns=colonnes),
                    poids=pd.DataFrame(poids_hist).T, frais=frais_total, dividendes=div_total,
                    alertes=alertes, montant_demande=demande, montant_execute=execute)


def mesures(valeur: pd.Series, taux_sans_risque: float, reference: pd.Series | None = None) -> dict[str, float]:
    """Mesures de performance d'une courbe de valeur journalière."""
    v = valeur.dropna()
    if len(v) < 2 or v.iloc[0] <= 0:
        return {}
    r = v.pct_change().dropna()
    annees = max((v.index[-1] - v.index[0]).days / 365.25, 1 / 365.25)
    cagr = (v.iloc[-1] / v.iloc[0]) ** (1 / annees) - 1
    vol = r.std() * np.sqrt(SEANCES_PAR_AN)
    baisse = r[r < 0].std() * np.sqrt(SEANCES_PAR_AN)
    dd = (v / v.cummax() - 1).min()
    res = {
        "Rendement total": v.iloc[-1] / v.iloc[0] - 1,
        "Rendement annualisé": cagr,
        "Volatilité annualisée": vol,
        "Sharpe": (cagr - taux_sans_risque) / vol if vol > 0 else np.nan,
        "Sortino": (cagr - taux_sans_risque) / baisse if baisse and baisse > 0 else np.nan,
        "Drawdown maximum": dd,
        "Calmar": cagr / abs(dd) if dd < 0 else np.nan,
    }
    if reference is not None:
        ref = reference.reindex(v.index).ffill().pct_change().dropna()
        commun = r.index.intersection(ref.index)
        if len(commun) > 20 and ref.loc[commun].var() > 0:
            res["Bêta"] = float(np.cov(r.loc[commun], ref.loc[commun])[0, 1] / ref.loc[commun].var())
            ecart = r.loc[commun] - ref.loc[commun]
            res["Tracking error"] = ecart.std() * np.sqrt(SEANCES_PAR_AN)
    return res


def poids_egaux(rendements: pd.DataFrame) -> pd.Series:
    return pd.Series(1.0 / rendements.shape[1], index=rendements.columns)
