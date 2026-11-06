"""
CSS centralisé de Riskfolio, repris de BRVM Analytics.

Charte : Royal Navy Blue, accent Snake Fruit, neutres froids, Cambria. Les couleurs de Streamlit
(widgets, barre latérale) viennent de ``.streamlit/config.toml`` ; ce module porte le reste.

Règles de conception :
  - retour immédiat à la pression (``:active``), jamais d'animation qui bloque ni de ``transition: all`` ;
  - seuls ``transform``, ``opacity``, ``background-color`` et ``box-shadow`` s'animent ;
  - hiérarchie par la graisse et l'espacement, interlettrage adapté à la taille du texte ;
  - chiffres tabulaires partout où des nombres se comparent ;
  - contraste WCAG AA, focus visibles, cibles tactiles de 44 px ;
  - préférences respectées : mouvement réduit, transparence réduite, contraste renforcé.

Usage :
    from styles import inject_theme_css
    inject_theme_css()
"""

from __future__ import annotations

import plotly.graph_objects as go
import plotly.io as pio
import streamlit as st

POLICE = 'Cambria, "Times New Roman", Georgia, serif'
SERIES = ["#0C64CF", "#EF5C4B", "#01467A", "#7EA7F9", "#8D9297", "#1B8A5A", "#AC0707", "#B9CCFE"]

if "charte" not in pio.templates:
    _modele = go.layout.Template(pio.templates["plotly_white"])
    _modele.layout.font = dict(family=POLICE, color="#003250")
    _modele.layout.colorway = SERIES
    _modele.layout.hoverlabel = dict(font=dict(family=POLICE))
    _modele.layout.xaxis.gridcolor = "#E7E8ED"
    _modele.layout.yaxis.gridcolor = "#E7E8ED"
    pio.templates["charte"] = _modele
pio.templates.default = "charte"


# ----------------------------------------------------------------------------
# Thème de base + responsive + accessibilité : appliqué à toutes les pages
# ----------------------------------------------------------------------------
_BASE_CSS = """
:root {
    --primary-100: #F2F5FF; --primary-200: #B9CCFE; --primary-300: #7EA7F9;
    --primary-400: #4284EB; --primary-500: #0C64CF; --primary-600: #0456A4;
    --primary-700: #01467A; --primary-800: #003250; --primary-900: #001A26;
    --accent-100: #FFF6F2; --accent-200: #FECBBC; --accent-300: #FA9783;
    --accent-400: #EF5C4B; --accent-500: #D91F16; --accent-600: #AC0707;
    --accent-700: #800202; --accent-800: #530000; --accent-900: #260000;
    --neutral-100: #FAFAFC; --neutral-200: #E7E8ED; --neutral-300: #D5D7DD;
    --neutral-400: #C3C6CD; --neutral-500: #B1B6BD; --neutral-600: #8D9297;
    --neutral-700: #686D71; --neutral-800: #45494C; --neutral-900: #222526;
    --bull: #1B8A5A; --bear: #C0392B;
    --color-pos: var(--bull); --color-neg: var(--bear);
    --color-warn: #B7791F; --color-info: var(--primary-500);
    --ombre-1: 0 1px 2px rgba(0, 50, 80, 0.06), 0 1px 3px rgba(0, 50, 80, 0.05);
    --ombre-2: 0 2px 4px rgba(0, 50, 80, 0.07), 0 6px 16px rgba(0, 50, 80, 0.07);
    --presse: 100ms ease-out;
}

/* ---------------- Fond et texte ---------------- */
html, body, [class*="css"], .stApp, .stMarkdown, button, input, textarea, select {
    font-family: Cambria, "Times New Roman", Georgia, serif;
}
.stApp {
    background: linear-gradient(180deg, var(--neutral-100) 0%, var(--primary-100) 100%) fixed;
    color: var(--primary-900);
}
.block-container, [data-testid="stMainBlockContainer"] {
    padding-top: 2.5rem; padding-bottom: 3rem; max-width: 1300px;
}

/* La barre du haut flotte au-dessus du contenu, sans bandeau opaque */
[data-testid="stHeader"] {
    background: rgba(250, 250, 252, 0.72);
    -webkit-backdrop-filter: blur(16px) saturate(180%);
    backdrop-filter: blur(16px) saturate(180%);
}

/* L'interlettrage dépend de la taille : serré en grand, légèrement ouvert en petit */
h1, h2, h3, h4, h5, h6 { color: var(--primary-800) !important; font-family: Cambria, 'Times New Roman', Georgia, serif !important; }
h1 { font-size: 2.1rem !important; line-height: 1.12 !important; letter-spacing: -0.02em; font-weight: 700 !important; }
h2 { font-size: 1.55rem !important; line-height: 1.2 !important; letter-spacing: -0.012em; font-weight: 700 !important; }
h3 { font-size: 1.22rem !important; line-height: 1.28 !important; letter-spacing: -0.006em; font-weight: 600 !important; }
h4 { font-size: 1.05rem !important; line-height: 1.32 !important; font-weight: 600 !important; }
[data-testid="stCaptionContainer"], [data-testid="stCaptionContainer"] *, .stCaption { color: var(--neutral-700) !important; letter-spacing: 0.004em; }
[data-testid="stCaptionContainer"] { opacity: 1 !important; }
section[data-testid="stSidebar"] [data-testid="stCaptionContainer"], section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] * { color: var(--primary-200) !important; }
[data-testid="stSidebarHeader"] img { height: 4.5rem !important; max-width: 100%; width: auto; }
[data-testid="stSidebarHeader"] { height: auto; padding-bottom: 0.5rem; }
section[data-testid="stSidebar"] h1, section[data-testid="stSidebar"] h2, section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] h4 { color: var(--primary-100) !important; }
/* Rangée d'indicateurs (première et dernière colonnes) : grille qui passe à la ligne, cases de même largeur même sur la dernière ligne. */
[data-testid="stHorizontalBlock"]:has(> [data-testid="stColumn"]:first-child [data-testid="stMetric"]):has(> [data-testid="stColumn"]:last-child [data-testid="stMetric"]) {
  display: grid !important; grid-template-columns: repeat(auto-fit, minmax(9.5rem, 1fr)); }
[data-testid="stHorizontalBlock"]:has(> [data-testid="stColumn"]:first-child [data-testid="stMetric"]):has(> [data-testid="stColumn"]:last-child [data-testid="stMetric"]) > [data-testid="stColumn"] {
  width: auto !important; min-width: 0 !important; }
[data-testid="stMetricLabel"], [data-testid="stMetricLabel"] * { white-space: normal !important; overflow: visible !important; }
[data-testid="stMetricValue"], [data-testid="stMetricValue"] * { overflow: visible !important; text-overflow: clip !important; }
a { color: var(--primary-500); }
a:hover { color: var(--primary-700); }

/* ---------------- Métriques ---------------- */
[data-testid="stMetric"] {
    background-color: white;
    padding: 14px 16px;
    border-radius: 10px;
    border: 1px solid var(--neutral-200);
    box-shadow: var(--ombre-1);
}
[data-testid="stMetricLabel"] { color: var(--neutral-700) !important; }
[data-testid="stMetricValue"] {
    font-size: clamp(1.15rem, 1.9vw, 1.75rem) !important;
    color: var(--primary-800) !important;
    font-variant-numeric: tabular-nums;
    letter-spacing: -0.012em;
}
[data-testid="stMetricDelta"] { font-variant-numeric: tabular-nums; }

/* ---------------- Boutons : hiérarchie claire, retour à la pression ---------------- */
.stButton > button, .stDownloadButton > button, .stFormSubmitButton > button, .stLinkButton > a {
    border-radius: 8px;
    font-weight: 600;
    transition: transform var(--presse), background-color 120ms ease-out, box-shadow 120ms ease-out;
}
.stButton > button:active, .stDownloadButton > button:active,
.stFormSubmitButton > button:active, .stLinkButton > a:active { transform: scale(0.97); }
button[kind="primary"], button[data-testid="stBaseButton-primary"],
button[data-testid="stBaseButton-primaryFormSubmit"] {
    background-color: var(--primary-500) !important;
    border-color: var(--primary-500) !important;
    color: white !important;
}
button[kind="primary"]:hover, button[data-testid="stBaseButton-primary"]:hover,
button[data-testid="stBaseButton-primaryFormSubmit"]:hover {
    background-color: var(--primary-700) !important;
    border-color: var(--primary-700) !important;
}
[data-testid="stMain"] button[data-testid="stBaseButton-secondary"],
[data-testid="stMain"] button[data-testid="stBaseButton-secondaryFormSubmit"] {
    background-color: white;
    border: 1px solid var(--neutral-400);
    color: var(--primary-700);
}
[data-testid="stMain"] button[data-testid="stBaseButton-secondary"]:hover,
[data-testid="stMain"] button[data-testid="stBaseButton-secondaryFormSubmit"]:hover {
    background-color: var(--primary-100);
    border-color: var(--primary-500);
    color: var(--primary-700);
}

section[data-testid="stSidebar"] button[kind="secondary"],
section[data-testid="stSidebar"] button[data-testid^="stBaseButton-secondary"] {
    background-color: rgba(255, 255, 255, 0.08) !important;
    border: 1px solid var(--primary-700) !important;
    color: var(--primary-100) !important;
}
section[data-testid="stSidebar"] button[kind="secondary"] *,
section[data-testid="stSidebar"] button[data-testid^="stBaseButton-secondary"] * { color: var(--primary-100) !important; }
section[data-testid="stSidebar"] button[kind="secondary"]:hover,
section[data-testid="stSidebar"] button[data-testid^="stBaseButton-secondary"]:hover {
    background-color: rgba(255, 255, 255, 0.16) !important;
    border-color: var(--primary-400) !important;
}

/* ---------------- Onglets : contrôle segmenté qui défile sur petit écran ---------------- */
.stTabs [role="tablist"] {
    gap: 4px;
    background-color: var(--neutral-200);
    padding: 4px;
    border-radius: 10px;
    overflow-x: auto;
    scrollbar-width: none;
}
.stTabs [role="tablist"]::-webkit-scrollbar { display: none; }
.stTabs [role="tab"] {
    background-color: transparent;
    color: var(--primary-800);
    border-radius: 7px;
    padding: 8px 16px;
    white-space: nowrap;
    transition: background-color 120ms ease-out, color 120ms ease-out;
}
.stTabs [role="tab"]:hover { background-color: rgba(255, 255, 255, 0.55); }
.stTabs [aria-selected="true"], .stTabs [aria-selected="true"]:hover {
    background-color: var(--primary-500) !important;
    color: white !important;
}
.stTabs [aria-selected="true"] p { color: white !important; }
.stTabs [role="tab"] .react-aria-SelectionIndicator, .stTabs [data-baseweb="tab-highlight"], .stTabs [data-baseweb="tab-border"], .stTabs [role="tablist"] > div:empty { display: none; }
.stTabs [role="tablist"], .stTabs [role="tab"] { height: auto; }

/* ---------------- Champs, tableaux, volets ---------------- */
[data-testid="stMain"] .stSelectbox > div > div,
[data-testid="stMain"] .stMultiSelect > div > div { background-color: white; }
.stDataFrame, [data-testid="stDataFrame"], .stTable {
    border: 1px solid var(--neutral-200);
    border-radius: 10px;
    overflow: hidden;
    font-variant-numeric: tabular-nums;
}
[data-testid="stExpander"] details {
    background-color: white;
    border: 1px solid var(--neutral-200);
    border-radius: 10px;
}
[data-testid="stExpander"] summary:hover { color: var(--primary-500); }
section[data-testid="stSidebar"] [data-testid="stExpander"] details {
    background-color: rgba(255, 255, 255, 0.06);
    border-color: var(--primary-700);
}
section[data-testid="stSidebar"] [data-testid="stExpander"] summary,
section[data-testid="stSidebar"] [data-testid="stExpander"] summary * { color: var(--primary-100); }
section[data-testid="stSidebar"] [data-testid="stExpander"] summary:hover,
section[data-testid="stSidebar"] [data-testid="stExpander"] summary:hover * { color: white; }
[data-testid="stPlotlyChart"] { border-radius: 10px; overflow: hidden; }

/* ---------------- Cartes communes ---------------- */
.metric-card {
    background: white;
    padding: 18px 20px;
    border-radius: 12px;
    border: 1px solid var(--neutral-200);
    border-left: 4px solid var(--primary-500);
    box-shadow: var(--ombre-1);
    margin-bottom: 10px;
    font-variant-numeric: tabular-nums;
}
.metric-card-positive { border-left-color: var(--bull); }
.metric-card-negative { border-left-color: var(--bear); }
.perf-positive { color: var(--bull); font-weight: 700; font-variant-numeric: tabular-nums; }
.perf-negative { color: var(--bear); font-weight: 700; font-variant-numeric: tabular-nums; }

.info-card, .info-box {
    background: var(--primary-100);
    color: var(--primary-800);
    padding: 14px 16px;
    border-radius: 10px;
    border-left: 4px solid var(--primary-500);
    margin: 10px 0;
}
.warning-card, .warning-box {
    background: #FEF8E7;
    color: #6B4A08;
    padding: 14px 16px;
    border-radius: 10px;
    border-left: 4px solid var(--color-warn);
    margin: 10px 0;
}
.interpretation-card, .interpretation-box, .success-box {
    background: #EDF7F2;
    color: #0F5135;
    padding: 14px 16px;
    border-radius: 10px;
    border-left: 4px solid var(--bull);
    margin: 10px 0;
}

/* Toast pour gestion d'erreurs (errors.py) */
.brvm-toast {
    background: var(--accent-100);
    border-left: 4px solid var(--accent-500);
    padding: 10px 14px;
    border-radius: 8px;
    color: var(--accent-700);
    margin: 8px 0;
}
.brvm-toast.warn { background: #FEF8E7; border-color: var(--color-warn); color: #6B4A08; }
.brvm-toast.info { background: var(--primary-100); border-color: var(--primary-500); color: var(--primary-800); }

.claude-logo {
    font-size: 2rem;
    font-weight: 700;
    letter-spacing: -0.02em;
    color: var(--primary-800);
    text-align: center;
    padding: 20px 0;
}
.footer {
    text-align: center;
    padding: 20px;
    color: var(--neutral-700);
    font-size: 0.8rem;
}

/* ---------------- Accessibilité ---------------- */
*:focus-visible {
    outline: 3px solid var(--primary-400) !important;
    outline-offset: 2px !important;
    border-radius: 4px;
}
@media (pointer: coarse) {
    .stButton > button, .stDownloadButton > button, .stFormSubmitButton > button { min-height: 44px; }
    .stTabs [role="tab"] { min-height: 44px; }
}
@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        transition-duration: 1ms !important;
        animation-duration: 1ms !important;
        animation-iteration-count: 1 !important;
        scroll-behavior: auto !important;
    }
    .stButton > button:active, .stDownloadButton > button:active,
    .stFormSubmitButton > button:active, .nav-tile:active { transform: none; }
}
@media (prefers-reduced-transparency: reduce) {
    [data-testid="stHeader"] {
        background: var(--neutral-100);
        -webkit-backdrop-filter: none;
        backdrop-filter: none;
    }
}
@media (prefers-contrast: more) {
    [data-testid="stHeader"] { background: white; -webkit-backdrop-filter: none; backdrop-filter: none; }
    [data-testid="stMetric"], .metric-card, .nav-tile, .perf-card, .kpi-card, .stat-card { border: 1px solid var(--primary-800); }
    [data-testid="stCaptionContainer"], [data-testid="stMetricLabel"] { color: var(--neutral-900) !important; }
}

/* ---------------- Responsive ---------------- */
@media (max-width: 900px) {
    .market-band { flex-direction: column; align-items: flex-start !important; }
    .market-band .mb-value { font-size: 1.1rem; }
    .perf-card { grid-template-columns: 28px 1fr auto !important; padding: 10px 12px; }
    .perf-return { font-size: 1rem !important; }
    [data-testid="stMetric"] { padding: 10px 12px; }
    .nav-tile { min-height: 95px !important; padding: 12px 8px !important; }
    .nav-tile-icon { font-size: 1.5rem !important; }
    .nav-tile-title { font-size: 0.85rem !important; }
    .stTabs [role="tab"] { padding: 8px 10px; font-size: 0.85rem; }
}
@media (max-width: 640px) {
    h1 { font-size: 1.6rem !important; }
    h2 { font-size: 1.3rem !important; }
    .block-container, [data-testid="stMainBlockContainer"] { padding-left: 1rem !important; padding-right: 1rem !important; }
    .stDataFrame { font-size: 0.8rem; }
}
"""


_INDICATEURS = """
.indicator-box {
    background: white; padding: 15px; border-radius: 10px;
    border: 1px solid var(--neutral-200);
    border-left: 4px solid var(--primary-500); margin: 10px 0;
}
.oversold { color: var(--bull); font-weight: 700; }
.overbought { color: var(--bear); font-weight: 700; }
.neutral { color: var(--neutral-700); font-weight: 700; }
"""


# ----------------------------------------------------------------------------
# CSS spécifique par page (déduit des anciens blocs <style> de chaque fichier)
# ----------------------------------------------------------------------------
_PAGE_CSS: dict[str, str] = {
    "app": """
.nav-tile {
    background: white;
    padding: 18px 12px 14px 12px;
    border-radius: 14px;
    border: 1px solid var(--neutral-200);
    box-shadow: var(--ombre-1);
    text-align: center;
    min-height: 120px;
    display: flex; flex-direction: column; align-items: center; justify-content: center;
    gap: 6px;
    transition: transform var(--presse), box-shadow 150ms ease-out, border-color 150ms ease-out;
}
.nav-tile:hover { box-shadow: var(--ombre-2); border-color: var(--primary-300); }
.nav-tile:active { transform: scale(0.98); }
.nav-tile-icon { font-size: 1.9rem; line-height: 1; }
.nav-tile-title { font-size: 0.95rem; font-weight: 600; color: var(--primary-800); }
.nav-tile-badge {
    font-size: 0.72rem; padding: 2px 8px; border-radius: 999px; letter-spacing: 0.01em;
    background: var(--primary-100); color: var(--primary-700);
    font-variant-numeric: tabular-nums;
}
.nav-tile-badge.pos { color: #0F5135; background: #EDF7F2; }
.nav-tile-badge.neg { color: var(--accent-700); background: var(--accent-100); }
.nav-tile.pos { border-color: var(--bull); }
.nav-tile.neg { border-color: var(--bear); }
.pulse-card {
    background: white; border-radius: 14px; padding: 14px 16px;
    border: 1px solid var(--neutral-200);
    box-shadow: var(--ombre-1);
}
""",
    "accueil": """
.market-band {
    background: linear-gradient(135deg, var(--primary-800) 0%, var(--primary-600) 100%);
    color: var(--primary-100);
    padding: 18px 24px; border-radius: 14px;
    display: flex; justify-content: space-between; align-items: center;
    gap: 16px; box-shadow: 0 4px 12px rgba(1, 70, 122, 0.2);
    margin-bottom: 8px; flex-wrap: wrap;
}
.market-band .mb-item { display: flex; flex-direction: column; }
.market-band .mb-label {
    font-size: 0.75rem; opacity: 0.8;
    text-transform: uppercase; letter-spacing: 0.06em;
}
.market-band .mb-value {
    font-size: 1.3rem; font-weight: 700; letter-spacing: -0.01em;
    font-variant-numeric: tabular-nums;
}
.market-band .mb-pos { color: #86EFAC; }
.market-band .mb-neg { color: var(--accent-200); }

.perf-card {
    background: white; border-radius: 14px; padding: 14px 16px; margin: 8px 0;
    border: 1px solid var(--neutral-200);
    border-left: 4px solid var(--neutral-300);
    box-shadow: var(--ombre-1);
    display: grid; grid-template-columns: 34px 1fr auto;
    gap: 12px; align-items: center;
}
.perf-card.top { border-left-color: var(--bull); }
.perf-card.flop { border-left-color: var(--bear); }
.perf-rank {
    background: var(--primary-100); color: var(--primary-700);
    width: 34px; height: 34px; border-radius: 50%;
    font-weight: 700; display: flex; align-items: center; justify-content: center;
    font-size: 0.95rem; font-variant-numeric: tabular-nums;
}
.perf-name { color: var(--primary-800); font-weight: 600; font-size: 1rem; line-height: 1.15; }
.perf-ticker { color: var(--neutral-700); font-size: 0.75rem; letter-spacing: 0.01em; }
.perf-return {
    font-size: 1.25rem; font-weight: 700; text-align: right;
    letter-spacing: -0.01em; font-variant-numeric: tabular-nums;
}
.perf-return.pos { color: var(--bull); }
.perf-return.neg { color: var(--bear); }
""",
    "overview": """
.stat-card {
    background: white; padding: 18px 16px; border-radius: 12px;
    border: 1px solid var(--neutral-200);
    border-top: 3px solid var(--primary-500);
    box-shadow: var(--ombre-1);
    text-align: center; height: 100%;
}
.stat-value {
    font-size: clamp(1.05rem, 1.55vw, 1.6rem); white-space: nowrap; font-weight: 700; color: var(--primary-800); line-height: 1.15;
    letter-spacing: -0.012em; font-variant-numeric: tabular-nums;
}
.stat-label {
    color: var(--neutral-700); font-size: 0.78rem;
    text-transform: uppercase; letter-spacing: 0.05em; margin-top: 4px;
}
.breadth-card {
    background: white; padding: 16px; border-radius: 12px;
    border: 1px solid var(--neutral-200);
    border-top: 3px solid var(--primary-500);
    text-align: center; box-shadow: var(--ombre-1);
}
.breadth-value { font-size: 1.8rem; font-weight: 700; letter-spacing: -0.012em; font-variant-numeric: tabular-nums; }
.breadth-value.pos { color: var(--bull); }
.breadth-value.neg { color: var(--bear); }
.breadth-label { color: var(--neutral-700); font-size: 0.85rem; }
""",
    "performances": "",  # tout dans le base
    "indicateurs": """
.main .block-container,
section.main > div.block-container,
[data-testid="stMainBlockContainer"] {
    max-width: 95vw !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
}
.indicator-box {
    background: white; padding: 15px; border-radius: 10px;
    border: 1px solid var(--neutral-200);
    border-left: 4px solid var(--primary-500); margin: 10px 0;
}
.oversold { color: var(--bull); font-weight: 700; }
.overbought { color: var(--bear); font-weight: 700; }
.neutral { color: var(--neutral-700); font-weight: 700; }
@media (max-width: 900px) {
    .main .block-container, [data-testid="stMainBlockContainer"] { padding-left: 1rem !important; padding-right: 1rem !important; }
}
""",
    "importation": "",  # info-box est dans le base
    "apropos": """
.formula-box {
    background: white; padding: 20px; border-radius: 12px;
    border: 1px solid var(--neutral-200);
    border-left: 4px solid var(--primary-500); margin: 15px 0;
    font-family: 'Courier New', monospace;
    overflow-x: auto;
}
.example-box {
    background: var(--primary-100); padding: 15px; border-radius: 10px; margin: 10px 0;
}
""",
    "chatbot": """
.chat-container {
    background: white; padding: 20px; border-radius: 12px;
    margin: 10px 0; border: 1px solid var(--neutral-200);
}
.user-message {
    background: var(--primary-100); padding: 15px; border-radius: 12px;
    margin: 10px 0; border-left: 4px solid var(--primary-500);
}
.assistant-message {
    background: white; padding: 15px; border-radius: 12px;
    margin: 10px 0; border: 1px solid var(--neutral-200);
}
.config-box {
    background: white; padding: 20px; border-radius: 12px;
    border: 1px solid var(--neutral-200);
    border-left: 4px solid var(--primary-500); margin: 15px 0;
}
.model-card {
    background: white; padding: 15px; border-radius: 10px;
    border: 2px solid var(--neutral-200); margin: 5px 0; cursor: pointer;
    transition: border-color 120ms ease-out, transform var(--presse);
}
.model-card:hover { border-color: var(--primary-500); }
.model-card:active { transform: scale(0.98); }
""",
    "strategie": """
.strategy-card {
    background: white;
    border: 1px solid var(--neutral-200);
    border-radius: 14px; padding: 20px; margin: 10px 0;
    border-left: 4px solid var(--primary-500);
    box-shadow: var(--ombre-1);
}
.portfolio-item {
    background-color: var(--neutral-100);
    border: 1px solid var(--neutral-200);
    border-radius: 10px; padding: 15px; margin: 5px 0;
}
.weight-positive { color: var(--bull); font-weight: 700; font-variant-numeric: tabular-nums; }
.weight-negative { color: var(--bear); font-weight: 700; font-variant-numeric: tabular-nums; }
.maintenance-container {
    display: flex; flex-direction: column; align-items: center; justify-content: center;
    padding: 60px 20px; text-align: center;
}
.maintenance-emoji { font-size: 120px; margin-bottom: 20px; }
.maintenance-text { font-size: 28px; color: var(--primary-700); font-weight: 700; letter-spacing: -0.012em; margin-bottom: 10px; }
.maintenance-subtext { font-size: 18px; color: var(--neutral-800); font-style: italic; }
.frontier-info {
    background-color: #FEF8E7;
    border-left: 4px solid var(--color-warn);
    padding: 15px; border-radius: 0 10px 10px 0; margin: 15px 0;
}
""",
    "simulation": """
.kpi-card {
    background: white; border-radius: 12px; padding: 18px;
    text-align: center;
    border: 1px solid var(--neutral-200);
    border-top: 3px solid var(--primary-500);
    box-shadow: var(--ombre-1);
}
.kpi-label { color: var(--neutral-700); font-size: 0.85rem; }
.kpi-value {
    font-size: 1.6rem; font-weight: 700; color: var(--primary-800);
    letter-spacing: -0.012em; font-variant-numeric: tabular-nums;
}
.kpi-value.pos { color: var(--bull); }
.kpi-value.neg { color: var(--bear); }
.alert-warn {
    background-color: #FEF8E7;
    border-left: 4px solid var(--color-warn);
    padding: 12px; border-radius: 0 10px 10px 0; margin: 10px 0;
}
""",
}


def inject_page_css(page_key: str | None = None) -> None:
    """Injecte le CSS de base + le bloc spécifique à la page.

    `page_key` doit correspondre à une clé de `_PAGE_CSS`. Si `None` ou inconnue,
    seul le CSS de base est injecté.
    """
    page_block = _PAGE_CSS.get(page_key, "") if page_key else ""
    css = f"<style>{_BASE_CSS}\n{page_block}</style>"
    st.markdown(css, unsafe_allow_html=True)


def css_global() -> str:
    """Règles générales et cartes de toutes les pages, injectées après celles de ``utils`` pour l'emporter.
    La mise en page large de la page Indicateurs reste à part (``inject_theme_css(wide_layout=True)``)."""
    blocs = "\n".join(v for k, v in _PAGE_CSS.items() if k != "indicateurs")
    return f"<style>{_BASE_CSS}\n{blocs}\n{_INDICATEURS}</style>"


_THEME_CSS = """
<style>
    /* ---- Messages Streamlit ---- */
    .stSuccess { background-color: #EDF7F2; border: 1px solid var(--bull); }
    .stError   { background-color: #FFF6F2; border: 1px solid var(--bear); }

    /* ====================================================== */
    /* COMPOSANTS RÉUTILISABLES (cartes HTML inline)           */
    /* ====================================================== */

    /* ---- Carte générique avec accent latéral (metric / stat / kpi / beta / config / formula / indicator / info-box) ---- */
    .metric-card,
    .stat-card,
    .kpi-card,
    .breadth-card,
    .beta-card,
    .config-box,
    .formula-box,
    .indicator-box,
    .info-box,
    .pulse-card {
        background: white;
        border-radius: 12px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
        border-left: 5px solid var(--primary-600);
    }
    .metric-card     { padding: 20px; border-left-width: 5px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 10px; }
    .stat-card       { padding: 18px 16px; text-align: center; height: 100%; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
    .kpi-card        { padding: 18px; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
    .breadth-card    { padding: 16px; text-align: center; }
    .beta-card       { padding: 20px; margin: 15px 0; border-left-width: 5px; border-radius: 12px; }
    .config-box      { padding: 20px; margin: 15px 0; border-left-width: 5px; }
    .formula-box     { padding: 20px; margin: 15px 0; border-left-width: 5px; font-family: 'Courier New', monospace; }
    .indicator-box   { padding: 15px; margin: 10px 0; border-left-width: 4px; border-radius: 10px; }
    .info-box        { padding: 18px 20px; margin: 12px 0; }
    .pulse-card      { padding: 14px 16px; border-left-width: 4px; }

    .metric-card-positive { border-left-color: var(--bull); }
    .metric-card-negative { border-left-color: var(--bear); }

    /* ---- Valeurs / labels génériques de carte ---- */
    .stat-value   { font-size: 1.6rem; font-weight: 700; color: var(--primary-800); line-height: 1.15; }
    .stat-label   { color: var(--primary-600); font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.04em; margin-top: 4px; }
    .kpi-label    { color: var(--primary-600); font-size: 0.85rem; }
    .kpi-value    { font-size: 1.6rem; font-weight: bold; color: var(--primary-800); }
    .kpi-value.pos { color: var(--bull); }
    .kpi-value.neg { color: var(--bear); }
    .breadth-value       { font-size: 1.8rem; font-weight: 700; }
    .breadth-value.pos   { color: var(--bull); }
    .breadth-value.neg   { color: var(--bear); }
    .breadth-label       { color: var(--primary-600); font-size: 0.85rem; }

    /* ---- Encadrés colorés (interprétation / warning / success / info / alert) ---- */
    .interpretation-card,
    .interpretation-box,
    .success-box {
        background: #EDF7F2;
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid var(--bull);
        margin: 10px 0;
    }
    .warning-card,
    .warning-box,
    .alert-warn {
        background: #FEF3C7;
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid var(--color-warn);
        margin: 10px 0;
    }
    .alert-ok {
        background: #EDF7F2;
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid var(--bull);
        margin: 10px 0;
        color: var(--primary-800);
    }
    .info-card {
        background: var(--neutral-200);
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .info-blue {
        background-color: #F2F5FF;
        border-left: 4px solid #4284EB;
        padding: 15px;
        border-radius: 0 10px 10px 0;
        margin: 15px 0;
    }
    .frontier-info {
        background-color: #FFF3CD;
        border-left: 4px solid #FFC107;
        padding: 15px;
        border-radius: 0 10px 10px 0;
        margin: 15px 0;
    }

    /* ---- Stratégie / portefeuille ---- */
    .strategy-card {
        background: linear-gradient(135deg, var(--neutral-200), var(--neutral-100));
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        border-left: 4px solid var(--primary-600);
    }
    .portfolio-item {
        background-color: var(--neutral-100);
        border: 1px solid var(--neutral-200);
        border-radius: 10px;
        padding: 15px;
        margin: 5px 0;
    }
    .weight-positive { color: var(--bull); font-weight: bold; }
    .weight-negative { color: var(--bear); font-weight: bold; }

    /* ---- Page maintenance ---- */
    .maintenance-container {
        display: flex; flex-direction: column;
        align-items: center; justify-content: center;
        padding: 60px 20px; text-align: center;
    }
    .maintenance-emoji   { font-size: 120px; margin-bottom: 20px; }
    .maintenance-text    { font-size: 28px; color: var(--primary-600); font-weight: bold; margin-bottom: 10px; }
    .maintenance-subtext { font-size: 18px; color: var(--primary-800); font-style: italic; }

    /* ---- Chatbot ---- */
    .chat-container {
        background: white;
        padding: 20px; border-radius: 12px;
        margin: 10px 0; border: 1px solid var(--neutral-200);
    }
    .user-message {
        background: var(--neutral-200);
        padding: 15px; border-radius: 12px;
        margin: 10px 0; border-left: 4px solid var(--primary-600);
    }
    .assistant-message {
        background: var(--neutral-100);
        padding: 15px; border-radius: 12px;
        margin: 10px 0; border-left: 4px solid var(--primary-800);
        border: 1px solid var(--neutral-200);
    }
    .model-card {
        background: white;
        padding: 15px; border-radius: 10px;
        border: 2px solid var(--neutral-200);
        margin: 5px 0; cursor: pointer;
    }
    .model-card:hover { border-color: var(--primary-600); }

    /* ---- Indicateurs techniques (signaux RSI / Stoch / etc.) ---- */
    .oversold   { color: var(--bull); font-weight: bold; }
    .overbought { color: var(--bear); font-weight: bold; }
    .neutral    { color: var(--primary-600); font-weight: bold; }

    /* ---- Bandeau marché (page Accueil) ---- */
    .market-band {
        background: linear-gradient(135deg, var(--primary-800) 0%, var(--primary-600) 100%);
        color: var(--neutral-100);
        padding: 18px 24px;
        border-radius: 14px;
        display: flex; justify-content: space-between; align-items: center;
        gap: 16px; flex-wrap: wrap;
        box-shadow: 0 4px 12px rgba(0,50,80,0.15);
        margin-bottom: 8px;
    }
    .market-band .mb-item  { display: flex; flex-direction: column; }
    .market-band .mb-label { font-size: 0.75rem; opacity: 0.75; text-transform: uppercase; letter-spacing: 0.06em; }
    .market-band .mb-value { font-size: 1.35rem; font-weight: 700; }
    .market-band .mb-pos   { color: #6EE7B7; }
    .market-band .mb-neg   { color: #FCA5A5; }

    /* ---- Cartes Top/Flop performers ---- */
    .perf-card {
        background: white;
        border-radius: 14px;
        padding: 14px 16px;
        margin: 8px 0;
        box-shadow: 0 2px 6px rgba(0,0,0,0.06);
        border-left: 5px solid var(--neutral-200);
        display: grid;
        grid-template-columns: 34px 1fr auto;
        gap: 12px;
        align-items: center;
    }
    .perf-card.top  { border-left-color: var(--bull); }
    .perf-card.flop { border-left-color: var(--bear); }
    .perf-rank {
        background: var(--neutral-200);
        color: var(--primary-800);
        width: 34px; height: 34px;
        border-radius: 50%;
        font-weight: 700;
        display: flex; align-items: center; justify-content: center;
        font-size: 0.95rem;
    }
    .perf-name   { color: var(--primary-800); font-weight: 600; font-size: 1rem; line-height: 1.15; }
    .perf-ticker { color: var(--primary-600); font-size: 0.75rem; }
    .perf-return { font-size: 1.25rem; font-weight: 700; text-align: right; }
    .perf-return.pos { color: var(--bull); }
    .perf-return.neg { color: var(--bear); }
    .perf-positive { color: var(--bull); font-weight: bold; }
    .perf-negative { color: var(--bear); font-weight: bold; }

    /* ---- Tuiles de navigation (page d'accueil) ---- */
    .nav-tile {
        background: white;
        padding: 18px 12px 14px 12px;
        border-radius: 14px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.06);
        border-top: 4px solid var(--primary-600);
        text-align: center;
        min-height: 120px;
        display: flex; flex-direction: column;
        align-items: center; justify-content: center;
        gap: 6px;
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .nav-tile-icon  { font-size: 1.9rem; line-height: 1; }
    .nav-tile-title { font-size: 0.95rem; font-weight: 600; color: var(--primary-800); }
    .nav-tile-badge {
        font-size: 0.72rem;
        padding: 2px 8px;
        border-radius: 999px;
        background: var(--neutral-100);
        color: var(--primary-600);
    }
    .nav-tile-badge.pos { color: #1B8A5A; background: #EDF7F2; }
    .nav-tile-badge.neg { color: #AC0707; background: #FFF6F2; }
    .nav-tile.accent { border-top-color: var(--primary-400); }
    .nav-tile.pos    { border-top-color: var(--bull); }
    .nav-tile.neg    { border-top-color: var(--bear); }

    /* ---- Encadrés didactiques (about) ---- */
    .example-box {
        background: var(--neutral-200);
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }

    /* ---- Bandeau sticky page Indicateurs Techniques ---- */
    .tech-sticky-header {
        position: sticky;
        top: 0;
        z-index: 999;
        background: rgba(250,250,252, 0.96);
        backdrop-filter: saturate(160%) blur(8px);
        -webkit-backdrop-filter: saturate(160%) blur(8px);
        padding: 10px 16px;
        border-radius: 10px;
        margin: 0 0 14px 0;
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 10px;
        box-shadow: 0 2px 8px rgba(0,50,80, 0.08);
        border: 1px solid var(--neutral-200);
    }
    .tech-sticky-left { display: flex; flex-direction: column; }
    .tech-sticky-ticker {
        font-size: 1.05rem; font-weight: 700; color: var(--primary-800);
    }
    .tech-sticky-symbol {
        font-size: 0.78rem; color: var(--primary-600); letter-spacing: 0.04em;
    }
    .tech-sticky-right {
        display: flex; align-items: center; gap: 10px;
        background: white; border-left: 5px solid var(--primary-600);
        padding: 8px 14px; border-radius: 8px;
    }
    .tech-sticky-emoji   { font-size: 1.3rem; }
    .tech-sticky-verdict { font-weight: 700; font-size: 1.0rem; }
    .tech-sticky-score   {
        font-size: 0.78rem; color: var(--primary-600);
        background: var(--neutral-100); padding: 3px 8px; border-radius: 999px;
    }

    /* ---- Bandeau sticky page Simulation Portefeuille ---- */
    .pf-sticky-header {
        position: sticky;
        top: 0;
        z-index: 999;
        background: rgba(250,250,252, 0.96);
        backdrop-filter: saturate(160%) blur(8px);
        -webkit-backdrop-filter: saturate(160%) blur(8px);
        padding: 14px 18px;
        border-radius: 12px;
        margin: 0 0 16px 0;
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 14px;
        box-shadow: 0 2px 10px rgba(0,50,80, 0.10);
        border: 1px solid var(--neutral-200);
        border-left: 5px solid var(--primary-600);
    }
    .pf-sticky-name {
        display: flex; align-items: center; gap: 10px;
        font-size: 1.15rem; font-weight: 700; color: var(--primary-800);
    }
    .pf-sticky-pf-icon { font-size: 1.4rem; }
    .pf-sticky-metrics {
        display: flex; gap: 14px; flex-wrap: wrap;
    }
    .pf-sticky-metric {
        background: white;
        padding: 8px 14px;
        border-radius: 10px;
        min-width: 160px;
        box-shadow: 0 1px 3px rgba(0,50,80, 0.06);
    }
    .pf-sticky-label {
        font-size: 0.72rem;
        color: var(--primary-600);
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-bottom: 2px;
    }
    .pf-sticky-value {
        font-size: 1.10rem;
        font-weight: 700;
        color: var(--primary-800);
    }
    .pf-sticky-value small { font-size: 0.78rem; font-weight: 500; opacity: 0.75; }

    /* ---- Cartes "définition + exemple chiffré" (page À propos) ---- */
    .def-card-title {
        font-size: 1.05rem; font-weight: 700;
        color: var(--primary-800);
        margin: 4px 0 10px 0;
    }
    .def-formula {
        background: white;
        border-left: 4px solid var(--primary-600);
        padding: 14px 18px;
        border-radius: 8px;
        font-family: 'Cambria Math', 'Latin Modern Math', 'Georgia', serif;
        font-size: 1.05rem;
        color: var(--primary-800);
        margin: 6px 0 10px 0;
    }
    .def-example {
        background: var(--neutral-200);
        padding: 12px 16px;
        border-radius: 8px;
        color: var(--primary-800);
        margin: 8px 0;
        font-size: 0.92rem;
    }
    .def-interp {
        background: #EDF7F2;
        border-left: 4px solid var(--bull);
        padding: 12px 16px;
        border-radius: 8px;
        color: var(--primary-800);
        margin: 8px 0;
        font-size: 0.92rem;
    }
    .def-where {
        background: #FEF3C7;
        border-left: 4px solid var(--color-warn);
        padding: 10px 14px;
        border-radius: 8px;
        color: var(--primary-800);
        margin: 8px 0;
        font-size: 0.85rem;
    }

    /* ---- Logo / footer ---- */
    .claude-logo {
        font-size: 2rem; font-weight: bold;
        color: var(--primary-800);
        text-align: center;
        padding: 20px 0;
    }
    .footer {
        text-align: center;
        padding: 20px;
        color: var(--primary-600);
        font-size: 0.8rem;
    }
</style>
"""


def inject_theme_css() -> None:
    """À appeler une fois par page, juste après ``st.set_page_config``."""
    st.markdown(_THEME_CSS, unsafe_allow_html=True)
    st.markdown(css_global(), unsafe_allow_html=True)
