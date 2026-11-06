"""Riskfolio : allocation de portefeuille et backtest réaliste, BRVM et marché américain.

Lancement :  streamlit run app.py
"""
from pathlib import Path

import streamlit as st

from portefeuille.depot import DonneesIndisponibles
from styles import inject_theme_css

RACINE = Path(__file__).resolve().parent

st.set_page_config(page_title="Riskfolio", page_icon=str(RACINE / "assets" / "logo.png"), layout="wide",
                   initial_sidebar_state="expanded")
st.logo(str(RACINE / "assets" / "logo_clair.png"), size="large", icon_image=str(RACINE / "assets" / "logo.png"))
inject_theme_css()

page = st.navigation([
    st.Page("pages/1_🏠_Synthèse.py", title="Accueil", icon="🏠", url_path="accueil", default=True),
    st.Page("pages/2_📈_Optimisation.py", title="Optimisation", icon="📈", url_path="optimisation"),
    st.Page("pages/3_🧪_Backtest.py", title="Backtest", icon="🧪", url_path="backtest"),
    st.Page("pages/4_ℹ️_À_propos.py", title="À propos", icon="ℹ️", url_path="a-propos"),
], expanded=True)
try:
    page.run()
except DonneesIndisponibles as erreur:
    st.error(str(erreur))
