"""Parcours des pages : navigation, optimisation et backtest sur la BRVM, sans exception."""
import re
from pathlib import Path

import pytest

pytest.importorskip("streamlit")
pytest.importorskip("riskfolio")
from streamlit.testing.v1 import AppTest  # noqa: E402

from portefeuille import depot  # noqa: E402

RACINE = Path(__file__).resolve().parents[1]
PAGES = sorted((RACINE / "pages").glob("*.py"))
CLONES = all(depot.clone_local(s) for s in depot.SOURCES.values())


def test_liens_de_pages_existent():
    texte = (RACINE / "app.py").read_text(encoding="utf-8")
    cibles = re.findall(r'st\.Page\("(pages/[^"]+)"', texte)
    assert len(cibles) == len(PAGES) and all((RACINE / c).exists() for c in cibles)
    liens = set()
    for p in PAGES:
        liens |= set(re.findall(r'page_link\("(pages/[^"]+)"', p.read_text(encoding="utf-8")))
    assert liens <= set(cibles)


def test_aucune_page_ne_porte_le_nom_du_point_d_entree():
    assert not [p for p in PAGES if p.stem.split("_", 2)[-1] == "app"]


def _app():
    return AppTest.from_file(str(RACINE / "app.py"), default_timeout=600)


def test_accueil_et_a_propos():
    app = _app().run()
    assert not app.exception
    app.switch_page("pages/4_ℹ️_À_propos.py").run()
    assert not app.exception and len(app.expander) >= 10


@pytest.mark.skipif(not CLONES, reason="clones locaux des dépôts de données absents")
def test_optimisation_brvm_par_defaut():
    app = _app().run()
    app.switch_page("pages/2_📈_Optimisation.py").run()
    assert not app.exception and not app.error
    assert len(app.metric) == 4


@pytest.mark.skipif(not CLONES, reason="clones locaux des dépôts de données absents")
def test_backtest_brvm_par_defaut():
    app = _app().run()
    app.switch_page("pages/3_🧪_Backtest.py").run()
    assert not app.exception
    app.sidebar.button[0].click().run()
    assert not app.exception and not app.error
    assert [m.label for m in app.metric][:2] == ["Rendement annualisé", "Volatilité"]
