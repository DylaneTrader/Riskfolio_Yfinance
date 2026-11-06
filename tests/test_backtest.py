"""Moteur de backtest sur un marché synthétique : chaque règle d'exécution, une à une."""
import numpy as np
import pandas as pd
import pytest

from portefeuille import backtest as B
from portefeuille.marches import Regles

SEANCES = pd.bdate_range("2024-01-01", "2024-12-31")
REGLES = Regles(reglement=2, frais=0.01, participation=0.20, marge_provision=0.075, impot_dividendes="")


def _marche(prix=None, volume=1_000_000):
    n = len(SEANCES)
    rng = np.random.default_rng(0)
    if prix is None:
        prix = {t: 100 * np.exp(np.cumsum(rng.normal(0, 0.01, n))) for t in "ABC"}
    cours = pd.DataFrame(prix, index=SEANCES)
    volumes = pd.DataFrame(volume, index=SEANCES, columns=cours.columns, dtype=float)
    return cours, volumes


def _quasi_constant(niveau):
    """Cours presque constants : assez de variance pour l'optimisation, valeur stable au millionième."""
    return niveau * (1 + 1e-7 * np.sin(np.arange(len(SEANCES))))


def _reglages(**c):
    base = dict(capital=1_000_000, debut=pd.Timestamp("2024-03-01"), fin=pd.Timestamp("2024-12-31"),
                frequence="Mensuel", fenetre=40, tolerance=0.0)
    return B.Reglages(**{**base, **c})


def test_dates_de_reequilibrage_dernieres_seances():
    d = B.dates_reequilibrage(SEANCES, "Trimestriel")
    assert list(d.strftime("%Y-%m-%d")) == ["2024-03-29", "2024-06-28", "2024-09-30", "2024-12-31"]


def test_decision_sans_regard_vers_l_avenir_et_execution_le_lendemain():
    cours, volumes = _marche()
    vues = []

    def allocation(r):
        vues.append(r.index[-1])
        return B.poids_egaux(r)

    res = B.executer(cours, volumes, SEANCES, allocation, REGLES, _reglages())
    decisions = list(res.poids.index)
    assert vues == decisions                       # rendements arrêtés à la date de décision
    premiere = res.operations["Date"].min()
    assert premiere == SEANCES[SEANCES.get_loc(decisions[0]) + 1]


def test_frais_et_participation():
    cours, volumes = _marche(volume=300)           # 20 % de 300 titres : 60 au plus par séance
    res = B.executer(cours, volumes, SEANCES, B.poids_egaux, REGLES, _reglages())
    ops = res.operations
    assert res.frais == pytest.approx(0.01 * ops["Montant"].sum())
    assert ops["Quantité"].max() <= 60
    assert (ops.groupby(["Date", "Titre"])["Quantité"].sum() <= 60).all()


def test_titres_achetes_revendus_apres_livraison_et_ventes_reglees_a_j_plus_r():
    prix = {"A": _quasi_constant(100.0), "B": _quasi_constant(50.0)}
    cours, volumes = _marche(prix)
    etapes = iter([pd.Series({"A": 1.0, "B": 0.0}), pd.Series({"A": 0.0, "B": 1.0})])
    dernier = {}

    def allocation(r):
        dernier["p"] = next(etapes, dernier.get("p"))
        return dernier["p"]

    res = B.executer(cours, volumes, SEANCES, allocation, REGLES, _reglages())
    ops = res.operations
    vente_a = ops[(ops["Titre"] == "A") & (ops["Sens"] == "Vente")]["Date"].min()
    achat_a = ops[(ops["Titre"] == "A") & (ops["Sens"] == "Achat")]["Date"].min()
    assert SEANCES.get_loc(vente_a) >= SEANCES.get_loc(achat_a) + 2   # titres livrés à J+2 avant revente
    # Avant le règlement de la vente (J+2), les achats de B ne disposent que de la trésorerie restée libre.
    reglement = SEANCES[SEANCES.get_loc(vente_a) + 2]
    achats_a = ops[(ops["Titre"] == "A") & (ops["Sens"] == "Achat")]
    libre = 1_000_000 - (achats_a["Montant"] + achats_a["Frais"]).sum()
    achats_b = ops[(ops["Titre"] == "B") & (ops["Sens"] == "Achat")]
    avant = achats_b[achats_b["Date"] < reglement]
    assert (avant["Montant"] + avant["Frais"]).sum() <= libre + 1e-6
    assert achats_b["Date"].max() >= reglement                       # le reste, financé par la vente


def test_sans_frictions_prix_constants_valeur_conservee():
    cours, volumes = _marche({"A": _quasi_constant(10.0), "B": _quasi_constant(20.0)})
    res = B.executer(cours, volumes, SEANCES, B.poids_egaux, REGLES.sans_frictions(), _reglages())
    assert len(res.operations) > 0 and res.frais == 0
    assert res.valeur.max() == pytest.approx(1_000_000, rel=1e-5)
    assert res.valeur.min() == pytest.approx(1_000_000, rel=1e-5)


def test_dividende_verse_sur_les_titres_detenus_la_veille():
    cours, volumes = _marche({"A": _quasi_constant(100.0), "B": _quasi_constant(100.0)})
    div = pd.DataFrame({"Ticker": ["A"], "Date_Detachement": [pd.Timestamp("2024-06-03")],
                        "Date_Paiement": [pd.Timestamp("2024-06-10")], "Montant": [5.0]})
    res = B.executer(cours, volumes, SEANCES, B.poids_egaux, REGLES.sans_frictions(), _reglages(), div)
    detenus = res.operations.query("Titre == 'A'").assign(
        q=lambda d: np.where(d["Sens"] == "Achat", d["Quantité"], -d["Quantité"]))
    q_veille = detenus[detenus["Date"] < pd.Timestamp("2024-06-03")]["q"].sum()
    assert q_veille > 0
    assert res.dividendes == pytest.approx(5.0 * q_veille)
    avant, apres = res.valeur.loc["2024-06-07"], res.valeur.loc["2024-06-10"]
    assert apres - avant == pytest.approx(0, abs=1.0)    # créance comptée dès le détachement, encaissée au paiement
    assert res.valeur.loc["2024-06-03"] - res.valeur.loc["2024-05-31"] == pytest.approx(5.0 * q_veille, abs=1.0)


def test_echec_d_optimisation_garde_l_allocation_precedente():
    cours, volumes = _marche()
    appels = {"n": 0}

    def allocation(r):
        appels["n"] += 1
        if appels["n"] > 1:
            raise B.EchecOptimisation("solveur")
        return B.poids_egaux(r)

    res = B.executer(cours, volumes, SEANCES, allocation, REGLES, _reglages())
    assert res.alertes and len(res.poids) == appels["n"]
    assert (res.poids.nunique() == 1).all()


def test_titre_sans_echange_n_est_pas_execute():
    cours, volumes = _marche()
    volumes["C"] = 0.0
    res = B.executer(cours, volumes, SEANCES, B.poids_egaux, REGLES, _reglages())
    assert "C" not in set(res.operations["Titre"])


def test_mesures():
    v = pd.Series([100, 110, 99, 121], index=pd.bdate_range("2024-01-01", periods=4), dtype=float)
    m = B.mesures(v, 0.0)
    assert m["Rendement total"] == pytest.approx(0.21)
    assert m["Drawdown maximum"] == pytest.approx(99 / 110 - 1)
