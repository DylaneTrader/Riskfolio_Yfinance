"""Emplacement des données de marché : un dépôt de données par marché.

- BRVM : ``DylaneTrader/Scraper-BRVM`` ;
- marché américain (Yahoo Finance) : ``DylaneTrader/Scraper-FinanceMatrix``.

En local, l'application lit un clone voisin (``private/<dépôt>`` ou à côté de ce dépôt ; ``BRVM_DATA_DIR`` /
``FM_DATA_DIR`` peuvent désigner un autre dossier, racine du clone). Là où il n'y en a pas, par exemple sur
Streamlit Cloud, elle télécharge du dépôt privé, avec un jeton en lecture seule (``SCRAPER_BRVM_TOKEN``,
``SCRAPER_FM_TOKEN``, dans les secrets ou l'environnement), les seuls fichiers utiles : les règles de lecture
(``lecture_donnees.py`` et ses modules) et ``data/actions``, ``data/indices``, ``data/dividendes``,
``data/societes``. La copie est renouvelée toutes les ``DUREE_VALIDITE`` secondes ; si un renouvellement
échoue, la dernière copie reste utilisée. Aucune donnée n'est écrite dans ce dépôt.
"""
from __future__ import annotations

import io
import os
import shutil
import tarfile
import tempfile
import time
import urllib.request
from dataclasses import dataclass
from pathlib import Path

RACINE_APP = Path(__file__).resolve().parents[1]
BRANCHE = "main"
DUREE_VALIDITE = 6 * 3600
MODULES = ("lecture_donnees.py", "operations_titres.py", "fiscalite.py", "typographie.py")
DOSSIERS = ("actions", "indices", "dividendes", "societes")


class DonneesIndisponibles(RuntimeError):
    """Ni clone local, ni copie téléchargée, ni jeton pour en obtenir une."""


@dataclass(frozen=True)
class Source:
    depot: str          # propriétaire/nom sur GitHub
    variable: str       # dossier local imposé
    jeton: str          # nom du secret

    @property
    def nom(self) -> str:
        return self.depot.split("/")[1]

    @property
    def copie(self) -> Path:
        return Path(tempfile.gettempdir()) / f"riskfolio_{self.nom.lower()}"


SOURCES = {
    "brvm": Source("DylaneTrader/Scraper-BRVM", "BRVM_DATA_DIR", "SCRAPER_BRVM_TOKEN"),
    "us": Source("DylaneTrader/Scraper-FinanceMatrix", "FM_DATA_DIR", "SCRAPER_FM_TOKEN"),
}


def _complet(dossier: Path) -> bool:
    return (dossier / "lecture_donnees.py").is_file() and (dossier / "data" / "actions").is_dir()


def clone_local(source: Source, racine_app: Path = RACINE_APP) -> Path | None:
    """Racine d'un clone : dossier imposé, sinon voisin de ce dépôt, sinon dans ``private/``."""
    variable = os.environ.get(source.variable)
    if variable:
        return Path(variable)
    for dossier in (racine_app.parent / source.nom, racine_app.parents[1] / "private" / source.nom):
        if _complet(dossier):
            return dossier
    return None


def _jeton(source: Source) -> str | None:
    if os.environ.get(source.jeton):
        return os.environ[source.jeton]
    try:
        import streamlit as st
        return st.secrets.get(source.jeton)
    except Exception:  # streamlit absent, ou aucun fichier de secrets
        return None


def _archive(source: Source, jeton: str) -> bytes:
    requete = urllib.request.Request(
        f"https://api.github.com/repos/{source.depot}/tarball/{BRANCHE}",
        headers={"Authorization": f"Bearer {jeton}", "Accept": "application/vnd.github+json",
                 "User-Agent": "riskfolio-app"})
    with urllib.request.urlopen(requete, timeout=300) as reponse:
        return reponse.read()


def _retenu(parties: tuple[str, ...]) -> bool:
    """Chemin relatif à la racine du dépôt : un module de lecture, ou un fichier d'un dossier de données utile."""
    if ".." in parties or not parties:
        return False
    if len(parties) == 1:
        return parties[0] in MODULES
    return len(parties) >= 3 and parties[0] == "data" and parties[1] in DOSSIERS


def extraire(archive: bytes, destination: Path) -> int:
    """Écrit les seuls fichiers retenus, sans sortir de ``destination``. Rend leur nombre."""
    n = 0
    with tarfile.open(fileobj=io.BytesIO(archive), mode="r:gz") as tar:
        for membre in tar.getmembers():
            parties = Path(membre.name).parts[1:]          # premier niveau : <proprietaire>-<depot>-<commit>
            if not membre.isfile() or not _retenu(parties):
                continue
            cible = destination.joinpath(*parties)
            cible.parent.mkdir(parents=True, exist_ok=True)
            cible.write_bytes(tar.extractfile(membre).read())
            n += 1
    return n


def _telecharger(source: Source, jeton: str) -> None:
    copie = source.copie
    copie.parent.mkdir(parents=True, exist_ok=True)
    provisoire = Path(tempfile.mkdtemp(prefix=f"{copie.name}_", dir=copie.parent))
    try:
        extraire(_archive(source, jeton), provisoire)
        if not _complet(provisoire):
            raise DonneesIndisponibles(f"L'archive de {source.depot} ne contient pas lecture_donnees.py et data/actions.")
        ancienne = copie.with_name(copie.name + "_ancienne")
        shutil.rmtree(ancienne, ignore_errors=True)
        if copie.exists():
            copie.rename(ancienne)
        provisoire.rename(copie)
        shutil.rmtree(ancienne, ignore_errors=True)
    finally:
        shutil.rmtree(provisoire, ignore_errors=True)


def racine(cle: str) -> Path:
    """Racine du dépôt de données du marché ``cle`` (clone local, sinon copie à jour). Télécharge au besoin."""
    source = SOURCES[cle]
    local = clone_local(source)
    if local is not None:
        return local
    copie = source.copie
    presente = _complet(copie)
    if presente and time.time() - copie.stat().st_mtime < DUREE_VALIDITE:
        return copie
    jeton = _jeton(source)
    if not jeton:
        if presente:
            return copie
        raise DonneesIndisponibles(
            f"Données de {source.nom} introuvables. Placez un clone de {source.depot} à côté de ce dépôt, ou "
            f"renseignez {source.jeton} (jeton en lecture seule sur ce dépôt) dans les secrets de l'application.")
    try:
        _telecharger(source, jeton)
    except Exception as erreur:
        if presente:
            return copie
        raise DonneesIndisponibles(f"Téléchargement de {source.depot} impossible : {type(erreur).__name__}.") from erreur
    return copie
