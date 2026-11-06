"""Les 13 modèles d'allocation (Riskfolio-Lib) derrière une seule fonction, ``optimiser``.

Le taux sans risque est saisi annuel et passé à Riskfolio en taux journalier, comme les rendements.
``optimiser`` lève ``EchecOptimisation`` au lieu d'afficher une erreur : le backtest l'appelle à chaque
rééquilibrage et garde alors l'allocation précédente.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

SEANCES_PAR_AN = 252


class EchecOptimisation(RuntimeError):
    pass


@dataclass(frozen=True)
class Modele:
    famille: str        # classique, parite, parite_relaxee, robuste, hierarchique
    objectif: str = ""  # MaxRet, MinRisk, Sharpe, Utility ; HRP / HERC / NCO pour les hiérarchiques
    description: str = ""


MODELES = {
    "Rendement maximum": Modele("classique", "MaxRet", "Maximise le rendement espéré."),
    "Risque minimum": Modele("classique", "MinRisk", "Minimise la mesure de risque choisie."),
    "Sharpe maximum": Modele("classique", "Sharpe", "Maximise le rendement excédentaire par unité de risque."),
    "Utilité maximum": Modele("classique", "Utility", "Rendement moins λ × risque."),
    "Parité de risque": Modele("parite", "", "Contribution égale de chaque titre au risque."),
    "Parité de risque relaxée": Modele("parite_relaxee", "", "Parité de risque assouplie (variance seulement)."),
    "Robuste : rendement maximum": Modele("robuste", "MaxRet", "Pire cas sur un ensemble d'incertitude en boîte."),
    "Robuste : risque minimum": Modele("robuste", "MinRisk", "Pire cas sur un ensemble d'incertitude en boîte."),
    "Robuste : Sharpe maximum": Modele("robuste", "Sharpe", "Pire cas sur un ensemble d'incertitude en boîte."),
    "Robuste : utilité maximum": Modele("robuste", "Utility", "Pire cas sur un ensemble d'incertitude en boîte."),
    "HRP (Hierarchical Risk Parity)": Modele("hierarchique", "HRP", "Classification puis allocation récursive."),
    "HERC (Hierarchical Equal Risk Contribution)": Modele("hierarchique", "HERC", "HRP à contributions égales par groupe."),
    "NCO (Nested Clustered Optimization)": Modele("hierarchique", "NCO", "Optimisation dans puis entre les groupes."),
}

MESURES_CLASSIQUES = {
    "MV": "Variance (écart-type)",
    "MAD": "Écart absolu moyen (MAD)",
    "MSV": "Semi-variance",
    "FLPM": "Moment partiel inférieur d'ordre 1",
    "SLPM": "Moment partiel inférieur d'ordre 2",
    "CVaR": "Valeur à risque conditionnelle (CVaR)",
    "EVaR": "Valeur à risque entropique (EVaR)",
    "WR": "Pire réalisation",
    "MDD": "Drawdown maximum",
    "ADD": "Drawdown moyen",
    "CDaR": "Drawdown conditionnel à risque (CDaR)",
    "UCI": "Indice Ulcer",
    "EDaR": "Drawdown entropique à risque (EDaR)",
}

MESURES_HIERARCHIQUES = {
    "vol": "Écart-type", "MV": "Variance", "KT": "Racine carrée de la kurtosis",
    "MAD": "Écart absolu moyen (MAD)", "GMD": "Différence moyenne de Gini", "CVRG": "Étendue de CVaR",
    "TGRG": "Étendue de Tail Gini", "RG": "Étendue", "MSV": "Semi-écart-type",
    "SKT": "Racine carrée de la semi-kurtosis", "FLPM": "Moment partiel inférieur d'ordre 1",
    "SLPM": "Moment partiel inférieur d'ordre 2", "VaR": "Valeur à risque (VaR)", "CVaR": "CVaR",
    "EVaR": "EVaR", "RLVaR": "VaR relativiste", "TG": "Tail Gini", "WR": "Pire réalisation",
    "MDD": "Drawdown maximum", "ADD": "Drawdown moyen", "UCI": "Indice Ulcer", "DaR": "Drawdown à risque",
    "CDaR": "CDaR", "EDaR": "EDaR", "RLDaR": "Drawdown relativiste à risque",
    "MDD_Rel": "Drawdown maximum, non composé", "ADD_Rel": "Drawdown moyen, non composé",
    "UCI_Rel": "Indice Ulcer, non composé", "DaR_Rel": "DaR, non composé", "CDaR_Rel": "CDaR, non composé",
    "EDaR_Rel": "EDaR, non composé", "RLDaR_Rel": "RLDaR, non composé",
}


# Mesures à programmation conique exponentielle : de quelques secondes à plusieurs minutes par optimisation.
MESURES_LENTES = {"EVaR", "EDaR", "RLVaR", "RLDaR", "EDaR_Rel", "RLDaR_Rel"}
# La parité de risque de Riskfolio ne gère pas ces mesures.
HORS_PARITE = {"WR", "MDD", "ADD"}


def mesures(nom_modele: str) -> dict[str, str]:
    """Mesures de risque proposées pour un modèle, les plus lentes signalées."""
    famille = MODELES[nom_modele].famille
    if famille == "hierarchique" and MODELES[nom_modele].objectif == "NCO":
        liste = MESURES_CLASSIQUES     # NCO optimise dans chaque groupe avec le modèle moyenne-risque classique
    elif famille == "hierarchique":
        liste = MESURES_HIERARCHIQUES
    elif famille in ("parite_relaxee", "robuste"):
        liste = {"MV": MESURES_CLASSIQUES["MV"]}   # variance seulement (parité relaxée, pire cas de Riskfolio)
    elif famille == "parite":
        liste = {k: v for k, v in MESURES_CLASSIQUES.items() if k not in HORS_PARITE}
    else:
        liste = MESURES_CLASSIQUES
    return {k: v + (" (calcul lent)" if k in MESURES_LENTES else "") for k, v in liste.items()}


@dataclass(frozen=True)
class Parametres:
    modele: str = "HRP (Hierarchical Risk Parity)"
    mesure: str = "vol"
    taux_sans_risque: float = 0.03        # annuel
    aversion: float = 2.0                 # λ des modèles d'utilité
    incertitude: float = 0.5              # ε des modèles robustes (quantile de la boîte)
    liaison: str = "ward"                 # modèles hiérarchiques
    codependance: str = "pearson"
    poids_max: float = 1.0                # plafond par titre (modèles classiques, parité, robustes)

    @property
    def rf_journalier(self) -> float:
        return self.taux_sans_risque / SEANCES_PAR_AN


def _portefeuille(rendements: pd.DataFrame, p: Parametres):
    import riskfolio as rp
    port = rp.Portfolio(returns=rendements)
    port.assets_stats(method_mu="hist", method_cov="hist")
    if p.poids_max < 1.0:
        port.upperlng = p.poids_max
    return port


def optimiser(rendements: pd.DataFrame, p: Parametres) -> tuple[pd.Series, object]:
    """Poids (somme 1, positifs) et l'objet Riskfolio, pour des rendements journaliers."""
    import riskfolio as rp

    if rendements.shape[1] < 2:
        raise EchecOptimisation("Il faut au moins deux titres.")
    if len(rendements) < 30:
        raise EchecOptimisation("Moins de 30 séances de rendements.")
    if p.modele not in MODELES:
        raise EchecOptimisation(f"Modèle inconnu : {p.modele}")
    m = MODELES[p.modele]
    rf = p.rf_journalier
    try:
        if m.famille == "hierarchique":
            port = rp.HCPortfolio(returns=rendements)
            options = dict(model=m.objectif, codependence=p.codependance, rm=p.mesure, rf=rf,
                           linkage=p.liaison, max_k=10, leaf_order=True)
            if m.objectif == "NCO":
                options.update(obj="Sharpe", l=p.aversion)
            w = port.optimization(**options)
        else:
            port = _portefeuille(rendements, p)
            port.rf = rf
            if m.famille == "classique":
                w = port.optimization(model="Classic", rm=p.mesure, obj=m.objectif, rf=rf,
                                      l=p.aversion if m.objectif == "Utility" else 0, hist=True)
            elif m.famille == "parite":
                w = port.rp_optimization(model="Classic", rm=p.mesure, rf=rf, b=None, hist=True)
            elif m.famille == "parite_relaxee":
                w = port.rrp_optimization(model="Classic", version="A", l=1, b=None)
            else:
                port.wc_stats(box="s", ellip="s", q=p.incertitude, n_sim=1000, window=3, seed=0)
                w = port.wc_optimization(obj=m.objectif, rf=rf, l=p.aversion if m.objectif == "Utility" else 0,
                                         Umu="box", Ucov="box")
    except Exception as erreur:  # noqa: BLE001 : solveur, données dégénérées...
        raise EchecOptimisation(f"{type(erreur).__name__} : {erreur}") from erreur
    if w is None or not isinstance(w, pd.DataFrame) or w.empty:
        raise EchecOptimisation("Le solveur n'a pas trouvé de solution.")
    poids = w.iloc[:, 0].astype(float).clip(lower=0)
    if not np.isfinite(poids).all() or poids.sum() <= 0:
        raise EchecOptimisation("Poids non exploitables.")
    return poids / poids.sum(), port


def statistiques(rendements: pd.DataFrame, poids: pd.Series, taux_sans_risque: float) -> dict[str, float]:
    """Rendement et volatilité annualisés, Sharpe, du portefeuille sur l'échantillon (estimation, pas backtest)."""
    r = rendements[poids.index] @ poids
    moyenne = r.mean() * SEANCES_PAR_AN
    vol = r.std() * np.sqrt(SEANCES_PAR_AN)
    return {"Rendement annualisé": moyenne, "Volatilité annualisée": vol,
            "Sharpe": (moyenne - taux_sans_risque) / vol if vol > 0 else np.nan}
