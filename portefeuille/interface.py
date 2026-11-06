"""Éléments communs aux pages : données en cache, choix du marché et de l'univers, graphiques."""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from styles import SERIES

from . import marches as M

SOURCE_FICHIER = "Fichier (CSV ou Excel)"
SOURCES = {"BRVM": "brvm", "Yahoo Finance (États-Unis)": "us", SOURCE_FICHIER: None}


@dataclass
class Donnees:
    marche: M.Marche | None          # None : fichier importé
    cours: pd.DataFrame
    volumes: pd.DataFrame | None
    seances: pd.DatetimeIndex
    reference: pd.Series | None
    dividendes: pd.DataFrame | None
    noms: dict[str, str]

    @property
    def devise(self) -> str:
        return self.marche.devise if self.marche else ""

    def libelle(self, ticker: str) -> str:
        nom = self.noms.get(ticker)
        return f"{ticker} : {nom}" if nom and nom != ticker else ticker


@st.cache_data(ttl=6 * 3600, show_spinner="Lecture des données du marché...")
def _marche(cle: str) -> dict:
    m = M.MARCHES[cle]
    return {"cours": M.cours(m), "volumes": M.volumes(m), "seances": M.seances(m),
            "reference": M.reference(m), "dividendes": M.dividendes(m), "noms": M.noms(m)}


def donnees_marche(cle: str) -> Donnees:
    d = _marche(cle)
    return Donnees(M.MARCHES[cle], d["cours"], d["volumes"], d["seances"], d["reference"], d["dividendes"], d["noms"])


def lire_fichier(fichier) -> Donnees:
    """Cours de clôture importés : une colonne Date (ou l'index), une colonne par titre."""
    if fichier.name.lower().endswith(".csv"):
        df = pd.read_csv(fichier, index_col=0, parse_dates=True, sep=None, engine="python")
    else:
        df = pd.read_excel(fichier, index_col=0, parse_dates=True)
    df.index = pd.to_datetime(df.index, errors="coerce")
    df = df[df.index.notna()].sort_index().apply(pd.to_numeric, errors="coerce").dropna(how="all")
    return Donnees(None, df, None, pd.DatetimeIndex(df.index), None, None, {})


def choisir_source(cle_etat: str) -> Donnees | None:
    """Barre latérale : marché ou fichier. ``None`` tant qu'aucun fichier n'est importé."""
    st.sidebar.header("Données")
    source = st.sidebar.radio("Source", list(SOURCES), key=f"{cle_etat}_source",
                              help="BRVM : Scraper-BRVM. États-Unis : Scraper-FinanceMatrix (Yahoo Finance).")
    cle = SOURCES[source]
    if cle is not None:
        return donnees_marche(cle)
    fichier = st.sidebar.file_uploader("Cours de clôture", type=["csv", "xlsx", "xls"], key=f"{cle_etat}_fichier",
                                       help="Première colonne : dates ; une colonne de cours par titre.")
    return lire_fichier(fichier) if fichier is not None else None


def choisir_univers(d: Donnees, cle_etat: str, minimum: int = 2) -> list[str]:
    """Titres retenus, par défaut ceux du marché (ou les huit premiers d'un fichier)."""
    titres = sorted(d.cours.columns)
    defaut = [t for t in (d.marche.min_tickers_defaut if d.marche else titres[:8]) if t in titres]
    choix = st.sidebar.multiselect("Titres", titres, default=defaut, key=f"{cle_etat}_titres_{d.marche.cle if d.marche else 'f'}",
                                   format_func=d.libelle)
    if len(choix) < minimum:
        st.info(f"Choisissez au moins {minimum} titres dans la barre latérale.")
        st.stop()
    return choix


def choisir_modele(cle_etat: str) -> "O.Parametres":
    """Barre latérale : modèle, mesure de risque et paramètres."""
    from . import optimisation as O
    st.sidebar.header("Modèle")
    noms = list(O.MODELES)
    modele = st.sidebar.selectbox("Modèle d'allocation", noms, index=noms.index("HRP (Hierarchical Risk Parity)"),
                                  key=f"{cle_etat}_modele", help="Détails mathématiques : page À propos.")
    st.sidebar.caption(O.MODELES[modele].description)
    mesures = O.mesures(modele)
    mesure = st.sidebar.selectbox("Mesure de risque", list(mesures), format_func=lambda k: f"{k} : {mesures[k]}",
                                  key=f"{cle_etat}_mesure_{O.MODELES[modele].famille}"
                                      + ("_nco" if O.MODELES[modele].objectif == "NCO" else ""))
    famille = O.MODELES[modele].famille
    with st.sidebar.expander("Paramètres"):
        rf = st.number_input("Taux sans risque annuel (%)", 0.0, 20.0, 3.0, 0.25, key=f"{cle_etat}_rf") / 100
        aversion = incertitude = None
        if "Utility" in O.MODELES[modele].objectif or O.MODELES[modele].objectif == "NCO":
            aversion = st.number_input("Aversion au risque λ", 0.1, 20.0, 2.0, 0.1, key=f"{cle_etat}_l")
        if famille == "robuste":
            incertitude = st.slider("Niveau de l'ensemble d'incertitude", 0.05, 0.95, 0.5, 0.05, key=f"{cle_etat}_q",
                                    help="Quantile du bootstrap qui borne la boîte d'incertitude sur μ et Σ.")
        liaison, codependance, poids_max = "ward", "pearson", 1.0
        if famille == "hierarchique":
            liaison = st.selectbox("Liaison", ["ward", "single", "complete", "average"], key=f"{cle_etat}_liaison")
            codependance = st.selectbox("Codépendance", ["pearson", "spearman", "kendall", "abs_pearson",
                                                         "distance"], key=f"{cle_etat}_codep")
        else:
            poids_max = st.slider("Poids maximal par titre (%)", 5, 100, 100, 5, key=f"{cle_etat}_wmax") / 100
    return O.Parametres(modele=modele, mesure=mesure, taux_sans_risque=rf, aversion=aversion or 2.0,
                        incertitude=incertitude or 0.5, liaison=liaison, codependance=codependance,
                        poids_max=poids_max)


def format_pct(x: float, decimales: int = 1) -> str:
    return "n.d." if x is None or not np.isfinite(x) else f"{x * 100:,.{decimales}f} %".replace(",", " ").replace(".", ",")


def format_montant(x: float, devise: str) -> str:
    if x is None or not np.isfinite(x):
        return "n.d."
    return f"{x:,.0f} {devise}".replace(",", " ").strip()


def graphique_poids(poids: pd.Series, d: Donnees) -> go.Figure:
    p = poids[poids > 1e-4].sort_values()
    fig = go.Figure(go.Bar(x=p.values * 100, y=[d.libelle(t) for t in p.index], orientation="h",
                           marker_color=SERIES[0], hovertemplate="%{y}<br>%{x:.2f} %<extra></extra>"))
    fig.update_layout(height=max(260, 28 * len(p) + 80), xaxis_title="Poids (%)", yaxis_title=None,
                      margin=dict(l=10, r=10, t=10, b=40))
    return fig


def graphique_correlation(rendements: pd.DataFrame) -> go.Figure:
    c = rendements.corr()
    fig = go.Figure(go.Heatmap(z=c.values, x=c.columns, y=c.columns, zmin=-1, zmax=1, zmid=0,
                               colorscale=[[0, "#AC0707"], [0.5, "#FFFFFF"], [1, "#0C64CF"]],
                               text=np.round(c.values, 2), texttemplate="%{text}", colorbar=dict(title="ρ")))
    fig.update_layout(height=max(320, 34 * len(c) + 120), yaxis_autorange="reversed",
                      margin=dict(l=10, r=10, t=10, b=10))
    return fig


def graphique_dendrogramme(rendements: pd.DataFrame, liaison: str, codependance: str) -> go.Figure | None:
    from scipy.cluster.hierarchy import dendrogram, linkage
    from scipy.spatial.distance import squareform
    methode = codependance if codependance in ("pearson", "spearman", "kendall") else "pearson"
    distance = np.sqrt(0.5 * (1 - rendements.corr(method=methode))).clip(lower=0)
    try:
        z = linkage(squareform(distance.values, checks=False), method=liaison)
    except ValueError:
        return None
    arbre = dendrogram(z, labels=list(rendements.columns), no_plot=True)
    fig = go.Figure()
    for x, y in zip(arbre["icoord"], arbre["dcoord"]):
        fig.add_trace(go.Scatter(x=x, y=y, mode="lines", line=dict(color=SERIES[2], width=1.4),
                                 hoverinfo="skip", showlegend=False))
    fig.update_layout(height=380, yaxis_title="Distance", margin=dict(l=10, r=10, t=10, b=80),
                      xaxis=dict(tickmode="array", tickvals=np.arange(5, 10 * len(arbre["ivl"]), 10),
                                 ticktext=arbre["ivl"], tickangle=-45))
    return fig


def graphique_courbes(courbes: dict[str, pd.Series], titre_y: str = "Base 100") -> go.Figure:
    fig = go.Figure()
    for k, (nom, s) in enumerate(courbes.items()):
        s = s.dropna()
        if s.empty:
            continue
        fig.add_trace(go.Scatter(x=s.index, y=100 * s / s.iloc[0], name=nom, mode="lines",
                                 line=dict(color=SERIES[k % len(SERIES)], width=2 if k == 0 else 1.4)))
    fig.update_layout(height=420, yaxis_title=titre_y, hovermode="x unified",
                      legend=dict(orientation="h", y=1.08, x=0), margin=dict(l=10, r=10, t=30, b=10))
    return fig


def graphique_drawdown(courbes: dict[str, pd.Series]) -> go.Figure:
    fig = go.Figure()
    for k, (nom, s) in enumerate(courbes.items()):
        s = s.dropna()
        if s.empty:
            continue
        fig.add_trace(go.Scatter(x=s.index, y=100 * (s / s.cummax() - 1), name=nom, mode="lines",
                                 line=dict(color=SERIES[k % len(SERIES)], width=1.4),
                                 fill="tozeroy" if k == 0 else None))
    fig.update_layout(height=280, yaxis_title="Baisse depuis le plus haut (%)", hovermode="x unified",
                      legend=dict(orientation="h", y=1.12, x=0), margin=dict(l=10, r=10, t=30, b=10))
    return fig
