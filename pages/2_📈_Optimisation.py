"""Optimisation : allocation d'un univers de titres sur une période d'estimation."""
import numpy as np
import pandas as pd
import streamlit as st

from portefeuille import interface as I
from portefeuille import optimisation as O

st.title("📈 Optimisation")
st.caption("Allocation estimée sur l'historique choisi. Pour savoir ce qu'elle aurait rapporté, avec les frais, "
           "la liquidité et les délais du marché, passez par la page Backtest.")

d = I.choisir_source("opt")
if d is None:
    st.info("Importez un fichier de cours dans la barre latérale.")
    st.stop()
titres = I.choisir_univers(d, "opt")
fin_max = d.cours.index.max().date()
debut_defaut = (pd.Timestamp(fin_max) - pd.DateOffset(years=3)).date()
periode = st.sidebar.date_input("Période d'estimation", (debut_defaut, fin_max),
                                min_value=d.cours.index.min().date(), max_value=fin_max, key="opt_periode",
                                format="DD/MM/YYYY")
if len(periode) != 2:
    st.info("Choisissez la date de fin de la période.")
    st.stop()
debut, fin = periode
p = I.choisir_modele("opt")

bloc = d.cours.loc[pd.Timestamp(debut):pd.Timestamp(fin), titres]
cotes = bloc.notna().mean()
peu_cotes = cotes[cotes < 0.6].index.tolist()
if peu_cotes:
    st.warning("Cotés moins de 60 % des séances de la période, donc écartés : "
               + ", ".join(d.libelle(t) for t in peu_cotes) + ".")
rendements = bloc.drop(columns=peu_cotes).ffill().pct_change(fill_method=None).iloc[1:].dropna(axis=1)
rendements = rendements.loc[:, rendements.std() > 0]
if rendements.shape[1] < 2 or len(rendements) < 30:
    st.error("Il faut au moins deux titres et 30 séances de rendements sur la période.")
    st.stop()


@st.cache_data(show_spinner="Optimisation...")
def _optimiser(rendements: pd.DataFrame, p: O.Parametres):
    poids, port = O.optimiser(rendements, p)
    frontiere = None
    if O.MODELES[p.modele].famille in ("classique", "parite", "robuste"):
        try:
            f = port.efficient_frontier(model="Classic", rm=p.mesure if O.MODELES[p.modele].famille != "robuste" else "MV",
                                        points=30, rf=p.rf_journalier, hist=True)
            frontiere = f
        except Exception:  # noqa: BLE001 : frontière facultative
            frontiere = None
    return poids, frontiere


try:
    poids, frontiere = _optimiser(rendements, p)
except O.EchecOptimisation as erreur:
    st.error(f"L'optimisation a échoué : {erreur}. Essayez une autre mesure de risque ou un autre univers.")
    st.stop()

stats = O.statistiques(rendements, poids, p.taux_sans_risque)
c = st.columns(4)
c[0].metric("Rendement annualisé (estimé)", I.format_pct(stats["Rendement annualisé"]))
c[1].metric("Volatilité annualisée", I.format_pct(stats["Volatilité annualisée"]))
c[2].metric("Sharpe", "n.d." if not np.isfinite(stats["Sharpe"]) else f"{stats['Sharpe']:.2f}".replace(".", ","))
c[3].metric("Titres en portefeuille", f"{int((poids > 1e-4).sum())} / {len(poids)}")
st.caption(f"Estimation sur {len(rendements)} séances, du {rendements.index[0]:%d/%m/%Y} au "
           f"{rendements.index[-1]:%d/%m/%Y} : rendement passé, pas une prévision.")

onglets = st.tabs(["Poids", "Corrélations", "Frontière efficiente", "Statistiques des titres"])
with onglets[0]:
    st.plotly_chart(I.graphique_poids(poids, d), use_container_width=True)
    tableau = pd.DataFrame({"Titre": [d.libelle(t) for t in poids.index], "Poids": poids.values * 100})
    tableau = tableau[tableau["Poids"] > 0.01].sort_values("Poids", ascending=False)
    st.dataframe(tableau, hide_index=True, use_container_width=True,
                 column_config={"Poids": st.column_config.NumberColumn("Poids (%)", format="%.2f")})
    st.download_button("Télécharger les poids (CSV)", tableau.to_csv(index=False, sep=";", decimal=",").encode("utf-8-sig"),
                       file_name="poids.csv", mime="text/csv")
with onglets[1]:
    st.plotly_chart(I.graphique_correlation(rendements), use_container_width=True)
    if O.MODELES[p.modele].famille == "hierarchique":
        fig = I.graphique_dendrogramme(rendements, p.liaison, p.codependance)
        if fig is not None:
            st.markdown("**Classification hiérarchique**")
            st.plotly_chart(fig, use_container_width=True)
with onglets[2]:
    if frontiere is None or frontiere.empty:
        st.info("Frontière efficiente disponible pour les modèles classiques, de parité et robustes.")
    else:
        mu, cov = rendements.mean(), rendements.cov()
        pts = [(np.sqrt(w @ cov @ w) * np.sqrt(O.SEANCES_PAR_AN), (w @ mu) * O.SEANCES_PAR_AN)
               for w in (frontiere[col].reindex(mu.index).fillna(0).values for col in frontiere.columns)]
        import plotly.graph_objects as go
        fig = go.Figure(go.Scatter(x=[x * 100 for x, _ in pts], y=[y * 100 for _, y in pts], mode="lines+markers",
                                   name="Frontière"))
        w = poids.reindex(mu.index).fillna(0).values
        fig.add_trace(go.Scatter(x=[np.sqrt(w @ cov @ w) * np.sqrt(O.SEANCES_PAR_AN) * 100],
                                 y=[(w @ mu) * O.SEANCES_PAR_AN * 100], mode="markers", name="Allocation retenue",
                                 marker=dict(size=14, symbol="star")))
        fig.update_layout(height=420, xaxis_title="Volatilité annualisée (%)", yaxis_title="Rendement annualisé (%)")
        st.plotly_chart(fig, use_container_width=True)
with onglets[3]:
    r = rendements
    cumul = (1 + r).cumprod()
    stats_titres = pd.DataFrame({
        "Rendement annualisé (%)": r.mean() * O.SEANCES_PAR_AN * 100,
        "Volatilité annualisée (%)": r.std() * np.sqrt(O.SEANCES_PAR_AN) * 100,
        "Drawdown maximum (%)": (cumul / cumul.cummax() - 1).min() * 100,
        "Asymétrie": r.skew(), "Kurtosis": r.kurtosis(),
        "Séances sans échange (%)": (r == 0).mean() * 100,
    })
    stats_titres.index = [d.libelle(t) for t in stats_titres.index]
    st.dataframe(stats_titres.round(2), use_container_width=True)
    st.caption("Séances sans échange : rendement nul faute de cotation. Élevé sur la BRVM pour les titres peu "
               "liquides, il sous-estime leur volatilité.")
