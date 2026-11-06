"""Chaque modèle avec chaque mesure proposée (hors mesures lentes) aboutit à des poids valides."""
import numpy as np
import pandas as pd
import pytest

pytest.importorskip("riskfolio")
from portefeuille import optimisation as O  # noqa: E402

RNG = np.random.default_rng(1)
RENDEMENTS = pd.DataFrame(RNG.multivariate_normal(np.full(6, 4e-4), np.diag(np.linspace(1, 3, 6)) * 1e-4 + 2e-5, 300),
                          columns=list("ABCDEF"), index=pd.bdate_range("2023-01-02", periods=300))
CAS = [(m, r) for m in O.MODELES for r in O.mesures(m) if r not in O.MESURES_LENTES]


@pytest.mark.parametrize("modele,mesure", CAS, ids=[f"{m[:20]}-{r}" for m, r in CAS])
def test_modele_et_mesure(modele, mesure):
    poids, _ = O.optimiser(RENDEMENTS, O.Parametres(modele=modele, mesure=mesure))
    assert poids.sum() == pytest.approx(1) and (poids >= 0).all() and list(poids.index) == list("ABCDEF")


def test_poids_maximal_respecte():
    poids, _ = O.optimiser(RENDEMENTS, O.Parametres(modele="Rendement maximum", mesure="MV", poids_max=0.3))
    assert poids.max() <= 0.3 + 1e-6


def test_taux_sans_risque_journalier():
    assert O.Parametres(taux_sans_risque=0.0252).rf_journalier == pytest.approx(0.0001)


def test_entrees_insuffisantes():
    with pytest.raises(O.EchecOptimisation):
        O.optimiser(RENDEMENTS[["A"]], O.Parametres())
    with pytest.raises(O.EchecOptimisation):
        O.optimiser(RENDEMENTS.iloc[:10], O.Parametres())
