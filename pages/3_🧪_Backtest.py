"""Backtest : l'allocation choisie rejouée dans le passé, aux conditions réelles du marché."""
from dataclasses import asdict

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from portefeuille import backtest as B
from portefeuille import interface as I
from portefeuille import optimisation as O
from styles import SERIES

st.title("🧪 Backtest")
st.caption("À chaque rééquilibrage, l'allocation est recalculée avec le seul historique connu ce jour-là, puis "
           "exécutée aux règles du marché : séance suivante, volume limité, règlement-livraison, frais, "
           "dividendes nets. Règles détaillées sur la page d'accueil.")

d = I.choisir_source("bt")
if d is None or d.marche is None:
    st.info("Le backtest réaliste a besoin des volumes, des dividendes et du calendrier du marché : choisissez "
            "BRVM ou Yahoo Finance dans la barre latérale.")
    st.stop()
m = d.marche
titres = I.choisir_univers(d, "bt")
p = I.choisir_modele("bt")
if p.mesure in O.MESURES_LENTES:
    st.sidebar.warning("Mesure lente : une optimisation peut prendre plusieurs minutes, et le backtest en fait "
                       "une par rééquilibrage, deux fois. Préférez un rééquilibrage annuel ou une autre mesure.")

st.sidebar.header("Backtest")
fin_max = d.seances.max().date()
periode = st.sidebar.date_input("Période testée", ((pd.Timestamp(fin_max) - pd.DateOffset(years=5)).date(), fin_max),
                                min_value=(d.seances.min() + pd.DateOffset(years=1)).date(), max_value=fin_max,
                                key="bt_periode", format="DD/MM/YYYY")
if len(periode) != 2:
    st.info("Choisissez la date de fin de la période.")
    st.stop()
capital = st.sidebar.number_input(f"Capital initial ({m.devise})", min_value=1_000.0,
                                  value=10_000_000.0 if m.devise == "FCFA" else 100_000.0, step=1_000.0,
                                  key=f"bt_capital_{m.cle}")
frequence = st.sidebar.selectbox("Rééquilibrage", list(B.FREQUENCES), index=1, key="bt_frequence")
fenetre = st.sidebar.select_slider("Historique de chaque décision (séances)", [63, 126, 252, 504, 756], value=252,
                                   key="bt_fenetre")
with st.sidebar.expander("Seuils d'ordre"):
    tolerance = st.slider("Écart de poids non corrigé (%)", 0.0, 5.0, 1.0, 0.5, key="bt_tol") / 100
    ordre_min = st.number_input(f"Ordre minimal ({m.devise})", 0.0, value=0.0, step=1_000.0, key=f"bt_min_{m.cle}")
    dividendes = st.checkbox("Créditer les dividendes", True, key="bt_div")
reglages = B.Reglages(capital=capital, debut=pd.Timestamp(periode[0]), fin=pd.Timestamp(periode[1]),
                      frequence=frequence, fenetre=fenetre, tolerance=tolerance, ordre_min=ordre_min,
                      dividendes=dividendes, taux_sans_risque=p.taux_sans_risque)

if not st.sidebar.button("Lancer le backtest", type="primary", use_container_width=True) \
        and st.session_state.get("bt_cle") != (m.cle, tuple(titres), p, asdict(reglages).__repr__()):
    st.info("Réglez l'univers, le modèle et la période, puis lancez le backtest.")
    st.stop()
st.session_state["bt_cle"] = (m.cle, tuple(titres), p, asdict(reglages).__repr__())


@st.cache_data(show_spinner=False, max_entries=8)
def _executer(cle: str, titres: tuple, p: O.Parametres, reglages: B.Reglages):
    d = I.donnees_marche(cle)
    regles = d.marche.regles
    cours, volumes = d.cours[list(titres)], d.volumes[list(titres)]

    def allocation(rendements):
        return O.optimiser(rendements, p)[0]

    args = (cours, volumes, d.seances)
    return {
        "modele": B.executer(*args, allocation, regles, reglages, d.dividendes),
        "egaux": B.executer(*args, B.poids_egaux, regles, reglages, d.dividendes),
        "sans_frictions": B.executer(*args, allocation, regles.sans_frictions(), reglages, d.dividendes),
    }


with st.spinner("Backtest en cours : une optimisation par rééquilibrage, trois simulations..."):
    try:
        res = _executer(m.cle, tuple(titres), p, reglages)
    except ValueError as erreur:
        st.error(str(erreur))
        st.stop()

modele = res["modele"]
if modele.poids.empty:
    st.error("Aucune allocation n'a pu être calculée sur la période : "
             + (modele.alertes[0] if modele.alertes else "historique insuffisant."))
    st.stop()

reference = d.reference.reindex(modele.valeur.index).ffill()
courbes = {p.modele: modele.valeur, "Poids égaux (mêmes règles)": res["egaux"].valeur,
           f"{p.modele}, sans frictions": res["sans_frictions"].valeur, m.nom_reference: reference}

mesures = {nom: B.mesures(v, p.taux_sans_risque, None if nom == m.nom_reference else reference)
           for nom, v in courbes.items()}
mm = mesures[p.modele]
c = st.columns(5)
c[0].metric("Rendement annualisé", I.format_pct(mm.get("Rendement annualisé")),
            delta=f"{(mm.get('Rendement annualisé', 0) - mesures[m.nom_reference].get('Rendement annualisé', 0)) * 100:+.1f} pts vs indice".replace(".", ","))
c[1].metric("Volatilité", I.format_pct(mm.get("Volatilité annualisée")))
c[2].metric("Drawdown maximum", I.format_pct(mm.get("Drawdown maximum")))
c[3].metric("Frais payés", I.format_montant(modele.frais, m.devise))
c[4].metric("Dividendes nets reçus", I.format_montant(modele.dividendes, m.devise))

couts = mesures[f"{p.modele}, sans frictions"].get("Rendement annualisé", 0) - mm.get("Rendement annualisé", 0)
taux_exec = modele.montant_execute / modele.montant_demande if modele.montant_demande else float("nan")
st.markdown(f"Les conditions du marché coûtent **{couts * 100:.2f} point(s) de rendement par an**".replace(".", ",")
            + f" à cette allocation (frais, délais, liquidité). Ordres exécutés : **{I.format_pct(taux_exec, 0)}** "
              "du montant demandé"
            + (" : la participation limitée au volume ralentit l'exécution des titres peu échangés ; le reste d'un "
               "ordre est remplacé au rééquilibrage suivant." if taux_exec < 0.95 else "."))

onglets = st.tabs(["Performance", "Allocation", "Opérations", "Alertes"])
with onglets[0]:
    st.plotly_chart(I.graphique_courbes(courbes), use_container_width=True)
    st.plotly_chart(I.graphique_drawdown(courbes), use_container_width=True)
    lignes = ["Rendement total", "Rendement annualisé", "Volatilité annualisée", "Sharpe", "Sortino",
              "Drawdown maximum", "Calmar", "Bêta", "Tracking error"]
    tableau = pd.DataFrame(mesures).reindex(lignes)
    pourcent = ["Rendement total", "Rendement annualisé", "Volatilité annualisée", "Drawdown maximum", "Tracking error"]
    affichage = tableau.copy().astype(object)
    for ligne in lignes:
        affichage.loc[ligne] = [I.format_pct(x) if ligne in pourcent else
                                ("n.d." if pd.isna(x) else f"{x:.2f}".replace(".", ",")) for x in tableau.loc[ligne]]
    st.dataframe(affichage, use_container_width=True)
    st.caption(f"Taux sans risque {I.format_pct(p.taux_sans_risque)} ; volatilité sur rendements journaliers (√252). "
               f"{m.nom_reference} : {m.note_reference}.")
with onglets[1]:
    w = modele.poids.loc[:, (modele.poids > 1e-4).any()]
    fig = go.Figure()
    for k, t in enumerate(w.columns):
        fig.add_trace(go.Scatter(x=w.index, y=w[t] * 100, name=d.libelle(t), stackgroup="poids", mode="lines",
                                 line=dict(width=0.5, color=SERIES[k % len(SERIES)])))
    fig.update_layout(height=420, yaxis_title="Poids cible (%)", hovermode="x unified",
                      legend=dict(orientation="h", y=-0.15))
    st.plotly_chart(fig, use_container_width=True)
    st.caption(f"Poids cibles décidés à chaque rééquilibrage ({len(w)} décisions, historique de {fenetre} séances).")
with onglets[2]:
    ops = modele.operations.copy()
    st.markdown(f"{len(ops)} opérations ; montant échangé {I.format_montant(ops['Montant'].sum(), m.devise)}.")
    ops["Titre"] = ops["Titre"].map(d.libelle)
    st.dataframe(ops.sort_values("Date", ascending=False), hide_index=True, use_container_width=True,
                 column_config={"Date": st.column_config.DateColumn(format="DD/MM/YYYY"),
                                "Cours": st.column_config.NumberColumn(format="%.2f"),
                                "Montant": st.column_config.NumberColumn(format="%.0f"),
                                "Frais": st.column_config.NumberColumn(format="%.0f")})
    st.download_button("Télécharger les opérations (CSV)",
                       ops.to_csv(index=False, sep=";", decimal=",", date_format="%d/%m/%Y").encode("utf-8-sig"),
                       file_name="operations_backtest.csv", mime="text/csv")
with onglets[3]:
    if modele.alertes:
        for a in modele.alertes:
            st.warning(a)
    else:
        st.success("Toutes les optimisations ont abouti.")
