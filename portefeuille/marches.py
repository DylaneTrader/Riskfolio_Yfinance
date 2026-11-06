"""Les deux marchés de l'application, leurs règles d'exécution et la lecture de leurs données.

Les cours, volumes, indices et dividendes sont lus par le module ``lecture_donnees`` du dépôt de données
de chaque marché : mêmes règles que BRVM Analytics et FinanceMatrix (divisions du nominal appliquées,
dividendes contrôlés contre les cours, nets d'impôt). Les deux dépôts ont des modules de même nom : chacun
est chargé à part, sans entrer dans ``sys.modules`` sous son nom, pour que les deux marchés coexistent.
"""
from __future__ import annotations

import importlib
import sys
import threading
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from types import ModuleType

import pandas as pd

from . import depot

_NOMS = tuple(m.removesuffix(".py") for m in depot.MODULES)
_VERROU = threading.Lock()


@dataclass(frozen=True)
class Regles:
    """Conditions d'exécution d'un marché (celles des moteurs de BRVM Analytics et de FinanceMatrix)."""
    reglement: int          # règlement-livraison à J+R (séances)
    frais: float            # par achat et par vente, part du montant
    participation: float    # part maximale des titres échangés dans la séance (0 = sans limite)
    marge_provision: float  # provision bloquée au-delà du dernier cours pour un ordre d'achat
    impot_dividendes: str   # texte : traitement fiscal des dividendes

    def sans_frictions(self) -> "Regles":
        return Regles(reglement=0, frais=0.0, participation=0.0, marge_provision=0.0,
                      impot_dividendes=self.impot_dividendes)


@dataclass(frozen=True)
class Marche:
    cle: str
    nom: str
    devise: str
    reference: str          # indice de comparaison et calendrier des séances
    nom_reference: str
    note_reference: str     # ce que l'indice inclut ou non
    regles: Regles
    min_tickers_defaut: tuple[str, ...]

    @property
    def colonne_dividende(self) -> str:
        return f"Montant_Net_{self.devise}"


MARCHES = {
    "brvm": Marche(
        cle="brvm", nom="BRVM", devise="FCFA", reference="BRVMC", nom_reference="BRVM Composite",
        note_reference="indice de cours : sans dividendes (la BRVM ne publie pas d'indice de rendement global), sans frais",
        regles=Regles(reglement=2, frais=0.01, participation=0.20, marge_provision=0.075,
                      impot_dividendes="nets d'IRVM (particulier, 12 % sur les montants publiés bruts)"),
        min_tickers_defaut=("SNTS.sn", "ORAC.ci", "SGBC.ci", "ETIT.tg", "SIBC.ci", "PALC.ci")),
    "us": Marche(
        cle="us", nom="Yahoo Finance (États-Unis)", devise="USD", reference="SPXTR", nom_reference="S&P 500 (dividendes réinvestis)",
        note_reference="indice de rendement global : dividendes bruts réinvestis, sans frais ni retenue",
        regles=Regles(reglement=1, frais=0.001, participation=0.20, marge_provision=0.0,
                      impot_dividendes="nets de la retenue à la source de 15 %"),
        min_tickers_defaut=("AAPL.us", "MSFT.us", "JNJ.us", "JPM.us", "XOM.us", "PG.us")),
}


@lru_cache(maxsize=4)
def _lecture(racine: str, cle: str) -> ModuleType:
    """``lecture_donnees`` du dépôt ``racine``, avec ses propres ``fiscalite``, ``operations_titres``..."""
    with _VERROU:
        sauves = {n: sys.modules.pop(n) for n in _NOMS if n in sys.modules}
        sys.path.insert(0, racine)
        importlib.invalidate_caches()
        try:
            module = importlib.import_module("lecture_donnees")
        finally:
            sys.path.remove(racine)
            charges = {n: sys.modules.pop(n, None) for n in _NOMS}
            sys.modules.update(sauves)
        for n, m in charges.items():
            if m is not None:
                sys.modules[f"_riskfolio_{cle}_{n}"] = m
    if Path(module.__file__).resolve().parent != Path(racine).resolve():
        raise depot.DonneesIndisponibles(f"lecture_donnees chargé depuis {module.__file__}, pas depuis {racine}.")
    return module


def lecture(marche: Marche) -> ModuleType:
    return _lecture(str(depot.racine(marche.cle)), marche.cle)


def tickers(marche: Marche) -> list[str]:
    return lecture(marche).tickers()


def noms(marche: Marche) -> dict[str, str]:
    lec = lecture(marche)
    return {t: lec.nom(t) for t in lec.tickers()}


def cours(marche: Marche) -> pd.DataFrame:
    """Clôtures, une colonne par titre, NaN les jours sans cotation (nominal le plus récent)."""
    return lecture(marche).panneau("Cloture")


def volumes(marche: Marche) -> pd.DataFrame:
    """Titres échangés par séance, une colonne par titre."""
    return lecture(marche).panneau("Volume_Titres")


def seances(marche: Marche) -> pd.DatetimeIndex:
    return lecture(marche).seances()


def reference(marche: Marche) -> pd.Series:
    return lecture(marche).indice(marche.reference)["Cloture"]


def dividendes(marche: Marche) -> pd.DataFrame:
    """Dividendes à créditer (contrôlés contre les cours), nets : Ticker, Date_Detachement, Date_Paiement, Montant."""
    d = lecture(marche).dividendes_retenus()
    d = d.rename(columns={marche.colonne_dividende: "Montant"})
    return d[["Ticker", "Date_Detachement", "Date_Paiement", "Montant"]].reset_index(drop=True)
