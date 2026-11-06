"""Emplacement et lecture des données : archive filtrée, clones locaux, deux marchés côte à côte."""
import io
import sys
import tarfile

import pandas as pd
import pytest

from portefeuille import depot
from portefeuille import marches as M


def _archive(fichiers: dict[str, bytes]) -> bytes:
    tampon = io.BytesIO()
    with tarfile.open(fileobj=tampon, mode="w:gz") as tar:
        for nom, contenu in fichiers.items():
            info = tarfile.TarInfo(f"DylaneTrader-Scraper-BRVM-abc123/{nom}")
            info.size = len(contenu)
            tar.addfile(info, io.BytesIO(contenu))
    return tampon.getvalue()


def test_extraction_ne_garde_que_les_fichiers_utiles(tmp_path):
    archive = _archive({
        "lecture_donnees.py": b"x", "fiscalite.py": b"x", "scraper/scraper_brvm.py": b"x",
        "data/actions/SNTS_sn_historique.csv": b"x", "data/news/actualites.csv": b"x",
        "data/dividendes/dividendes.csv": b"x", "../evasion.py": b"x", "data/../../evasion.csv": b"x",
    })
    assert depot.extraire(archive, tmp_path) == 4
    ecrits = sorted(str(p.relative_to(tmp_path)).replace("\\", "/") for p in tmp_path.rglob("*") if p.is_file())
    assert ecrits == ["data/actions/SNTS_sn_historique.csv", "data/dividendes/dividendes.csv",
                      "fiscalite.py", "lecture_donnees.py"]
    assert not (tmp_path.parent / "evasion.py").exists()


def test_sans_clone_ni_jeton_message_clair(tmp_path, monkeypatch):
    source = depot.Source("DylaneTrader/Inexistant", "INEXISTANT_DIR", "INEXISTANT_TOKEN")
    monkeypatch.setitem(depot.SOURCES, "test", source)
    monkeypatch.setattr(depot.Source, "copie", property(lambda s: tmp_path / "copie"))
    with pytest.raises(depot.DonneesIndisponibles, match="INEXISTANT_TOKEN"):
        depot.racine("test")


def test_dossier_impose_par_variable(monkeypatch, tmp_path):
    monkeypatch.setenv("BRVM_DATA_DIR", str(tmp_path))
    assert depot.clone_local(depot.SOURCES["brvm"]) == tmp_path


CLONES = all(depot.clone_local(s) for s in depot.SOURCES.values())


@pytest.mark.skipif(not CLONES, reason="clones locaux de Scraper-BRVM et Scraper-FinanceMatrix absents")
def test_deux_marches_cote_a_cote_sans_se_melanger():
    brvm, us = M.lecture(M.MARCHES["brvm"]), M.lecture(M.MARCHES["us"])
    assert brvm is not us and "Scraper-BRVM" in brvm.__file__ and "Scraper-FinanceMatrix" in us.__file__
    assert brvm.F is not us.F                                   # chacun son module fiscal
    assert "lecture_donnees" not in sys.modules and "fiscalite" not in sys.modules
    assert all(t.endswith((".ci", ".sn", ".bf", ".tg", ".bj", ".ml", ".ne")) for t in M.tickers(M.MARCHES["brvm"]))
    assert all(t.endswith(".us") for t in M.tickers(M.MARCHES["us"]))


@pytest.mark.skipif(not CLONES, reason="clones locaux absents")
def test_titres_par_defaut_et_dividendes_nets():
    for m in M.MARCHES.values():
        assert set(m.min_tickers_defaut) <= set(M.tickers(m))
        d = M.dividendes(m)
        assert list(d.columns) == ["Ticker", "Date_Detachement", "Date_Paiement", "Montant"]
        assert (d["Montant"] > 0).all() and pd.api.types.is_datetime64_any_dtype(d["Date_Detachement"])
