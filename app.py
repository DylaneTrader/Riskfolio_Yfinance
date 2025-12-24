"""
Application d'Optimisation de Portefeuille avec Riskfolio-Lib, Plotly et yfinance
"""

import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import riskfolio as rp
import warnings
from io import BytesIO

# Import des modèles d'optimisation
from models import (
    optimize_max_return,
    optimize_min_risk,
    optimize_max_sharpe,
    optimize_max_utility,
    optimize_risk_parity,
    optimize_relaxed_risk_parity,
    optimize_robust_max_return,
    optimize_robust_min_risk,
    optimize_robust_max_sharpe,
    optimize_robust_max_utility,
    optimize_hrp,
    optimize_herc,
    optimize_nco
)

warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Optimisation de Portefeuille",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for page navigation
if 'page' not in st.session_state:
    st.session_state.page = 'Accueil'

# Sidebar navigation
st.sidebar.title("🧭 Navigation")
page = st.sidebar.radio(
    "Aller à:",
    ["Accueil", "Optimisation", "À propos"]
)
st.session_state.page = page

st.sidebar.markdown("---")

# Dictionnaire de traduction des mesures de risque (modèles classiques)
RISK_MEASURES_DICT = {
    "MV": "Variance (Écart-type)",
    "MAD": "Écart Absolu Moyen (MAD)",
    "MSV": "Semi-Variance",
    "FLPM": "Moment Partiel Inférieur du Premier Ordre",
    "SLPM": "Moment Partiel Inférieur du Second Ordre",
    "CVaR": "Valeur à Risque Conditionnelle (CVaR)",
    "EVaR": "Valeur à Risque Entropic (EVaR)",
    "WR": "Pire Réalisation (Worst Realization)",
    "MDD": "Drawdown Maximum",
    "ADD": "Drawdown Moyen",
    "CDaR": "Drawdown Conditionnel à Risque (CDaR)",
    "UCI": "Indice Ulcer",
    "EDaR": "Drawdown Entropic à Risque (EDaR)"
}

# Dictionnaire des 32 mesures de risque pour HRP et HERC
HRP_HERC_RISK_MEASURES = {
    # Mesures de Dispersion
    "vol": "Écart-type (Standard Deviation)",
    "variance": "Variance",
    "kurt": "Racine Carrée de la Kurtosis",
    "mad": "Écart Absolu Moyen (MAD)",
    "gmd": "Différence Moyenne de Gini (GMD)",
    "cvrg": "Plage CVaR (CVaR Range)",
    "tgrg": "Plage Tail Gini (Tail Gini Range)",
    "rg": "Plage (Range)",
    
    # Mesures de Risque à la Baisse
    "semi": "Écart-type Semi (Semi Standard Deviation)",
    "skurt": "Racine Carrée Semi-Kurtosis",
    "flpm": "Premier Moment Partiel Inférieur (Omega Ratio)",
    "slpm": "Second Moment Partiel Inférieur (Sortino Ratio)",
    "var": "Valeur à Risque (VaR)",
    "cvar": "Valeur à Risque Conditionnelle (CVaR)",
    "evar": "Valeur à Risque Entropic (EVaR)",
    "rlvar": "Valeur à Risque Relativiste (RLVaR)",
    "tg": "Tail Gini",
    "wr": "Pire Réalisation (Minimax)",
    
    # Mesures de Drawdown (rendements composés)
    "mdd": "Drawdown Maximum (Calmar Ratio)",
    "add": "Drawdown Moyen",
    "uci": "Indice Ulcer",
    "dar": "Drawdown à Risque (DaR)",
    "cdar": "Drawdown Conditionnel à Risque (CDaR)",
    "edar": "Drawdown Entropic à Risque (EDaR)",
    "rdar": "Drawdown Relativiste à Risque (RDaR)",
    
    # Mesures de Drawdown (rendements non composés)
    "mdd_rel": "Drawdown Maximum - Non Composé",
    "add_rel": "Drawdown Moyen - Non Composé",
    "uci_rel": "Indice Ulcer - Non Composé",
    "dar_rel": "DaR - Non Composé",
    "cdar_rel": "CDaR - Non Composé",
    "edar_rel": "EDaR - Non Composé",
    "rdar_rel": "RDaR - Non Composé"
}

# Functions
@st.cache_data
def download_data(tickers, start_date, end_date):
    """Télécharge les données historiques depuis Yahoo Finance"""
    try:
        data = yf.download(tickers, start=start_date, end=end_date, progress=False)
        if isinstance(data.columns, pd.MultiIndex):
            prices = data['Close']
        else:
            prices = data[['Close']]
        
        # Clean data
        prices = prices.dropna(how='all')
        prices = prices.ffill().bfill()
        
        return prices
    except Exception as e:
        st.error(f"Erreur lors du téléchargement des données: {str(e)}")
        return None

def read_uploaded_file(uploaded_file):
    """Lit un fichier CSV ou XLSX uploadé"""
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file, index_col=0, parse_dates=True)
        elif uploaded_file.name.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(uploaded_file, index_col=0, parse_dates=True)
        else:
            st.error("Format de fichier non supporté. Utilisez CSV ou XLSX.")
            return None
        
        # Clean data
        df = df.dropna(how='all')
        df = df.ffill().bfill()
        
        return df
    except Exception as e:
        st.error(f"Erreur lors de la lecture du fichier: {str(e)}")
        return None

def calculate_portfolio(prices, model, risk_measure, rf, risk_aversion, uncertainty):
    """
    Calcule les poids optimaux du portefeuille selon le modèle sélectionné
    Utilise les modules séparés dans le dossier models/
    """
    try:
        # Calculate returns
        returns = prices.pct_change().dropna()
        
        # Dictionnaire de mapping des modèles vers les fonctions
        model_functions = {
            "Portefeuille de Rendement Maximum": optimize_max_return,
            "Portefeuille de Risque Minimum": optimize_min_risk,
            "Portefeuille de Sharpe Maximum": optimize_max_sharpe,
            "Portefeuille d'Utilité Maximum": optimize_max_utility,
            "Portefeuille de Parité de Risque": optimize_risk_parity,
            "Portefeuille de Parité de Risque Relaxée": optimize_relaxed_risk_parity,
            "Portefeuille Robuste - Rendement Maximum": optimize_robust_max_return,
            "Portefeuille Robuste - Risque Minimum": optimize_robust_min_risk,
            "Portefeuille Robuste - Sharpe Maximum": optimize_robust_max_sharpe,
            "Portefeuille Robuste - Utilité Maximum": optimize_robust_max_utility,
            "Hierarchical Risk Parity (HRP)": optimize_hrp,
            "Hierarchical Equal Risk Contribution (HERC)": optimize_herc,
            "Nested Clustered Optimization (NCO)": optimize_nco
        }
        
        # Obtenir la fonction d'optimisation correspondante
        optimize_func = model_functions.get(model)
        
        if optimize_func is None:
            st.error(f"Modèle non reconnu: {model}")
            return None, None, None
        
        # Appeler la fonction d'optimisation avec les paramètres appropriés
        w, port, returns_calc = optimize_func(
            returns=returns,
            risk_measure=risk_measure,
            rf=rf,
            risk_aversion=risk_aversion,
            uncertainty=uncertainty
        )
        
        if w is None or w.sum().sum() == 0:
            st.error("L'optimisation a échoué. Essayez différents paramètres.")
            return None, None, None
            
        return w, port, returns_calc
        
    except Exception as e:
        st.error(f"Erreur lors de l'optimisation: {str(e)}")
        return None, None, None
        
    except Exception as e:
        st.error(f"Erreur lors de l'optimisation: {str(e)}")
        return None, None

def calculate_metrics(weights, port):
    """Calcule les métriques du portefeuille"""
    try:
        metrics = {}
        
        # Expected return
        metrics['Rendement Annuel Attendu'] = (port.mu @ weights).iloc[0, 0] * 252
        
        # Volatility
        metrics['Volatilité Annuelle'] = np.sqrt(weights.T @ port.cov @ weights).iloc[0, 0] * np.sqrt(252)
        
        # Sharpe Ratio
        if metrics['Volatilité Annuelle'] > 0:
            metrics['Ratio de Sharpe'] = (metrics['Rendement Annuel Attendu'] - port.rf) / metrics['Volatilité Annuelle']
        else:
            metrics['Ratio de Sharpe'] = 0
        
        return metrics
    except Exception as e:
        st.error(f"Erreur lors du calcul des métriques: {str(e)}")
        return None

def get_descriptive_stats(prices):
    """Calcule les statistiques descriptives pour les actifs"""
    returns = prices.pct_change().dropna()
    
    stats = pd.DataFrame({
        'Rendement Moyen (%)': returns.mean() * 252 * 100,
        'Volatilité (%)': returns.std() * np.sqrt(252) * 100,
        'Min (%)': returns.min() * 100,
        'Max (%)': returns.max() * 100,
        'Skewness': returns.skew(),
        'Kurtosis': returns.kurtosis()
    })
    
    return stats

def get_performance_table(prices, returns, port):
    """Génère un tableau de performance avec indicateurs de risque"""
    try:
        # Calcul des rendements annualisés
        annual_returns = returns.mean() * 252
        
        # Calcul des volatilités annualisées
        annual_vol = returns.std() * np.sqrt(252)
        
        # Sharpe ratio
        sharpe = (annual_returns - port.rf) / annual_vol
        
        # Max drawdown
        cumulative_returns = (1 + returns).cumprod()
        running_max = cumulative_returns.cummax()
        drawdown = (cumulative_returns - running_max) / running_max
        max_dd = drawdown.min()
        
        # VaR et CVaR
        var_95 = returns.quantile(0.05)
        cvar_95 = returns[returns <= var_95].mean()
        
        performance_df = pd.DataFrame({
            'Rendement Annuel (%)': annual_returns * 100,
            'Volatilité Annuelle (%)': annual_vol * 100,
            'Ratio de Sharpe': sharpe,
            'Drawdown Maximum (%)': max_dd * 100,
            'VaR 95% (%)': var_95 * 100,
            'CVaR 95% (%)': cvar_95 * 100
        })
        
        return performance_df
    except Exception as e:
        st.error(f"Erreur lors du calcul du tableau de performance: {str(e)}")
        return None

def plot_weights(weights):
    """Affiche les poids du portefeuille en graphique à barres"""
    weights_df = weights.copy()
    weights_df.columns = ['Poids']
    weights_df = weights_df[weights_df['Poids'] > 0.001].sort_values('Poids', ascending=False)
    
    fig = go.Figure(data=[
        go.Bar(
            x=weights_df.index,
            y=weights_df['Poids'] * 100,
            marker_color='indianred'
        )
    ])
    
    fig.update_layout(
        title="Poids du Portefeuille",
        xaxis_title="Actifs",
        yaxis_title="Poids (%)",
        height=400,
        showlegend=False
    )
    
    return fig

def plot_pie_chart(weights):
    """Affiche les poids du portefeuille en diagramme circulaire"""
    weights_df = weights.copy()
    weights_df.columns = ['Poids']
    weights_df = weights_df[weights_df['Poids'] > 0.001]
    
    fig = go.Figure(data=[go.Pie(
        labels=weights_df.index,
        values=weights_df['Poids'],
        hole=.3
    )])
    
    fig.update_layout(
        title="Allocation du Portefeuille",
        height=400
    )
    
    return fig

def plot_efficient_frontier(port, weights, risk_measure):
    """Affiche la frontière efficiente"""
    try:
        points = 50
        frontier = port.efficient_frontier(model='Classic', rm=risk_measure, points=points, rf=port.rf, hist=True)
        
        if frontier is None:
            return None
        
        # Calculate risk and return for each point
        risk_values = []
        return_values = []
        
        for i in range(frontier.shape[1]):
            w = frontier.iloc[:, i:i+1]
            ret = (port.mu @ w).iloc[0, 0] * 252
            vol = np.sqrt(w.T @ port.cov @ w).iloc[0, 0] * np.sqrt(252)
            return_values.append(ret)
            risk_values.append(vol)
        
        # Calculate current portfolio
        current_ret = (port.mu @ weights).iloc[0, 0] * 252
        current_vol = np.sqrt(weights.T @ port.cov @ weights).iloc[0, 0] * np.sqrt(252)
        
        fig = go.Figure()
        
        # Efficient frontier
        fig.add_trace(go.Scatter(
            x=risk_values,
            y=return_values,
            mode='lines',
            name='Frontière Efficiente',
            line=dict(color='blue', width=2)
        ))
        
        # Current portfolio
        fig.add_trace(go.Scatter(
            x=[current_vol],
            y=[current_ret],
            mode='markers',
            name='Portefeuille Sélectionné',
            marker=dict(color='red', size=12, symbol='star')
        ))
        
        fig.update_layout(
            title="Frontière Efficiente",
            xaxis_title="Risque (Volatilité)",
            yaxis_title="Rendement Attendu",
            height=500,
            showlegend=True
        )
        
        return fig
    except Exception as e:
        st.warning(f"Impossible d'afficher la frontière efficiente: {str(e)}")
        return None

def plot_correlation_matrix(returns):
    """Affiche la matrice de corrélation"""
    corr = returns.corr()
    
    fig = go.Figure(data=go.Heatmap(
        z=corr.values,
        x=corr.columns,
        y=corr.columns,
        colorscale='RdBu',
        zmid=0,
        text=corr.values,
        texttemplate='%{text:.2f}',
        textfont={"size": 10},
        colorbar=dict(title="Corrélation")
    ))
    
    fig.update_layout(
        title="Matrice de Corrélation",
        height=500,
        xaxis_showgrid=False,
        yaxis_showgrid=False,
        yaxis_autorange='reversed'
    )
    
    return fig

def plot_dendrogram(returns, linkage='ward', codependence='pearson'):
    """Affiche le dendrogramme pour les modèles hiérarchiques"""
    try:
        from scipy.cluster.hierarchy import dendrogram, linkage as sp_linkage
        from scipy.spatial.distance import squareform
        
        # Calculate distance matrix based on codependence method
        if codependence == 'pearson':
            corr = returns.corr()
            # Convert correlation to distance: d = sqrt(0.5 * (1 - corr))
            dist = np.sqrt(0.5 * (1 - corr))
        elif codependence == 'spearman':
            corr = returns.corr(method='spearman')
            dist = np.sqrt(0.5 * (1 - corr))
        elif codependence == 'kendall':
            corr = returns.corr(method='kendall')
            dist = np.sqrt(0.5 * (1 - corr))
        else:
            corr = returns.corr()
            dist = np.sqrt(0.5 * (1 - corr))
        
        # Convert to condensed distance matrix
        dist_condensed = squareform(dist, checks=False)
        
        # Perform hierarchical clustering
        Z = sp_linkage(dist_condensed, method=linkage)
        
        # Create dendrogram
        fig = go.Figure()
        
        # Calculate dendrogram data
        dendro = dendrogram(Z, labels=returns.columns.tolist(), no_plot=True)
        
        # Add lines for dendrogram
        icoord = np.array(dendro['icoord'])
        dcoord = np.array(dendro['dcoord'])
        
        for i in range(len(icoord)):
            fig.add_trace(go.Scatter(
                x=icoord[i],
                y=dcoord[i],
                mode='lines',
                line=dict(color='rgb(100,100,100)', width=1),
                showlegend=False,
                hoverinfo='skip'
            ))
        
        # Add labels
        labels = dendro['ivl']
        x_labels = np.arange(5, len(labels) * 10 + 5, 10)
        
        fig.update_layout(
            title=f"Dendrogramme (Clustering Hiérarchique - {linkage.capitalize()})",
            xaxis=dict(
                tickmode='array',
                tickvals=x_labels,
                ticktext=labels,
                tickangle=-45
            ),
            yaxis_title="Distance",
            height=500,
            showlegend=False,
            plot_bgcolor='white'
        )
        
        return fig
        
    except Exception as e:
        st.warning(f"Impossible d'afficher le dendrogramme: {str(e)}")
        return None


# ============================================================================
# PAGE: ACCUEIL
# ============================================================================
def show_home_page():
    st.title("📊 Optimisation de Portefeuille avec Riskfolio-Lib")
    
    st.markdown("""
    ## Bienvenue dans l'Application d'Optimisation de Portefeuille
    
    Cette application vous permet d'optimiser des portefeuilles financiers en utilisant diverses 
    méthodes quantitatives avancées, incluant des modèles classiques et de machine learning, 
    basée sur la bibliothèque **Riskfolio-Lib**.
    
    ### 🎯 Fonctionnalités Principales
    
    - **13 Modèles d'Optimisation**: Modèles classiques et modèles ML (HRP, HERC, NCO)
    - **45 Mesures de Risque**: 13 mesures classiques + 32 mesures pour HRP/HERC
    - **Import de Données Flexible**: Yahoo Finance, CSV ou fichiers Excel
    - **Visualisations Interactives**: Graphiques de poids, frontière efficiente, corrélations
    - **Statistiques Détaillées**: Analyse descriptive et indicateurs de performance
    
    ### 📖 Comment Utiliser l'Application
    
    1. **Navigation**: Utilisez le menu latéral pour naviguer entre les pages
    2. **Optimisation**: Configurez votre portefeuille et lancez l'optimisation
    3. **À propos**: Consultez les explications mathématiques des modèles
    
    ### 🚀 Pour Commencer
    
    Cliquez sur **"Optimisation"** dans le menu de navigation pour commencer à construire 
    votre portefeuille optimal.
    """)
    
    # Afficher quelques statistiques ou exemples
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("**13** Modèles d'Optimisation")
    
    with col2:
        st.info("**45** Mesures de Risque")
    
    with col3:
        st.info("**3** Sources de Données")
    
    st.markdown("---")
    
    st.markdown("""
    ### 📚 Modèles Disponibles
    
    #### Modèles Classiques
    - Portefeuille de Rendement Maximum
    - Portefeuille de Risque Minimum
    - Portefeuille de Sharpe Maximum
    - Portefeuille d'Utilité Maximum
    - Portefeuille de Parité de Risque
    - Portefeuille de Parité de Risque Relaxée
    - Portefeuilles Robustes (4 variantes)
    
    #### Modèles de Machine Learning
    - Hierarchical Risk Parity (HRP)
    - Hierarchical Equal Risk Contribution (HERC)
    - Nested Clustered Optimization (NCO)
    
    ### 🔍 Mesures de Risque
    
    - **13 mesures classiques**: Variance, CVaR, Drawdown Maximum, etc.
    - **32 mesures HRP/HERC**: Dispersions, Downside, Drawdowns composés et non-composés
    
    Consultez la page **"À propos"** pour plus de détails sur chaque modèle.
    """)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    **Sources de Données:** Yahoo Finance, CSV, Excel  
    **Bibliothèque d'Optimisation:** Riskfolio-Lib  
    **Visualisation:** Plotly  
    """)

# ============================================================================
# PAGE: OPTIMISATION
# ============================================================================
def show_optimization_page():
    st.title("⚙️ Optimisation de Portefeuille")
    
    # Sidebar configuration
    st.sidebar.header("Configuration du Portefeuille")
    
    # Data source selection
    data_source = st.sidebar.radio(
        "Source de données",
        ["Yahoo Finance", "Importer un fichier"]
    )
    
    prices = None
    
    if data_source == "Yahoo Finance":
        # Default tickers
        default_tickers = "AAPL,MSFT,GOOGL,AMZN,TSLA,JPM,JNJ,V,PG,NVDA"
        tickers_input = st.sidebar.text_area(
            "Entrez les symboles boursiers (séparés par des virgules)",
            value=default_tickers,
            help="Entrez les symboles boursiers séparés par des virgules"
        )
        
        # Parse tickers
        tickers = [ticker.strip().upper() for ticker in tickers_input.split(",") if ticker.strip()]
        
        # Date range selection
        st.sidebar.subheader("Période")
        end_date = st.sidebar.date_input(
            "Date de fin",
            value=datetime.now(),
            max_value=datetime.now()
        )
        start_date = st.sidebar.date_input(
            "Date de début",
            value=end_date - timedelta(days=365*2),
            max_value=end_date
        )
        
    else:
        # File upload
        uploaded_file = st.sidebar.file_uploader(
            "Télécharger un fichier CSV ou XLSX",
            type=['csv', 'xlsx', 'xls'],
            help="Le fichier doit contenir les prix avec les dates en index et les actifs en colonnes"
        )
    
    # Portfolio optimization model selection
    st.sidebar.subheader("Modèle d'Optimisation")
    optimization_models = [
        "Portefeuille de Rendement Maximum",
        "Portefeuille de Risque Minimum",
        "Portefeuille de Sharpe Maximum",
        "Portefeuille d'Utilité Maximum",
        "Portefeuille de Parité de Risque",
        "Portefeuille de Parité de Risque Relaxée",
        "Portefeuille Robuste - Rendement Maximum",
        "Portefeuille Robuste - Risque Minimum",
        "Portefeuille Robuste - Sharpe Maximum",
        "Portefeuille Robuste - Utilité Maximum",
        "Hierarchical Risk Parity (HRP)",
        "Hierarchical Equal Risk Contribution (HERC)",
        "Nested Clustered Optimization (NCO)"
    ]
    
    selected_model = st.sidebar.selectbox(
        "Sélectionnez le modèle d'optimisation",
        options=optimization_models
    )
    
    # Risk measure selection - différent pour HRP/HERC
    st.sidebar.subheader("Mesure de Risque")
    
    # Vérifier si le modèle est HRP ou HERC pour afficher les bonnes mesures
    if selected_model in ["Hierarchical Risk Parity (HRP)", "Hierarchical Equal Risk Contribution (HERC)"]:
        risk_measures = list(HRP_HERC_RISK_MEASURES.keys())
        risk_measure_names = [f"{k}: {v}" for k, v in HRP_HERC_RISK_MEASURES.items()]
        default_index = 0  # "vol" par défaut
    else:
        risk_measures = list(RISK_MEASURES_DICT.keys())
        risk_measure_names = [f"{k}: {v}" for k, v in RISK_MEASURES_DICT.items()]
        default_index = 0
    
    selected_risk_index = st.sidebar.selectbox(
        "Sélectionnez la mesure de risque",
        options=range(len(risk_measures)),
        format_func=lambda x: risk_measure_names[x],
        index=default_index
    )
    risk_measure = risk_measures[selected_risk_index]
    
    # Additional parameters
    st.sidebar.subheader("Paramètres Additionnels")
    risk_free_rate = st.sidebar.number_input(
        "Taux Sans Risque (%)",
        min_value=0.0,
        max_value=10.0,
        value=2.5,
        step=0.1
    ) / 100
    
    risk_aversion = st.sidebar.number_input(
        "Aversion au Risque (λ)",
        min_value=0.1,
        max_value=10.0,
        value=2.0,
        step=0.1,
        help="Utilisé pour le portefeuille d'utilité maximum"
    )
    
    # Uncertainty set parameter for Worst Case
    uncertainty_param = st.sidebar.number_input(
        "Paramètre d'Incertitude (ε)",
        min_value=0.0,
        max_value=1.0,
        value=0.5,
        step=0.05,
        help="Utilisé pour les modèles robustes"
    )
    
    # Button to run optimization
    run_optimization = st.sidebar.button("🚀 Optimiser le Portefeuille", type="primary")
    
    # Main content
    if run_optimization:
        if data_source == "Yahoo Finance":
            if len(tickers) < 2:
                st.error("Veuillez entrer au moins 2 symboles boursiers.")
                return
            
            with st.spinner("Téléchargement des données et optimisation du portefeuille..."):
                prices = download_data(tickers, start_date, end_date)
        
        else:
            if uploaded_file is None:
                st.error("Veuillez télécharger un fichier.")
                return
            
            with st.spinner("Lecture du fichier et optimisation du portefeuille..."):
                prices = read_uploaded_file(uploaded_file)
        
        if prices is not None and not prices.empty:
            st.success(f"✅ Données chargées avec succès pour {len(prices.columns)} actifs")
            
            # Show data preview
            with st.expander("📊 Aperçu des Données de Prix"):
                st.dataframe(prices.tail(10))
            
            # Calculer les rendements pour les statistiques
            returns = prices.pct_change().dropna()
            
            # === SECTION 1: STATISTIQUES DESCRIPTIVES (indépendantes de l'optimisation) ===
            st.header("📊 Analyse des Données")
            
            # Statistiques descriptives
            st.subheader("📈 Statistiques Descriptives des Actifs")
            desc_stats = get_descriptive_stats(prices)
            
            # Utiliser des gradients de couleur pour les tableaux
            st.dataframe(
                desc_stats.style.background_gradient(cmap='RdYlGn', subset=['Rendement Moyen (%)']),
                use_container_width=True
            )
            
            # Matrice de corrélation
            st.subheader("🔗 Matrice de Corrélation")
            fig_corr = plot_correlation_matrix(returns)
            st.plotly_chart(fig_corr, use_container_width=True)
            
            # Dendrogramme pour les modèles hiérarchiques
            if selected_model in ["Hierarchical Risk Parity (HRP)", 
                                 "Hierarchical Equal Risk Contribution (HERC)", 
                                 "Nested Clustered Optimization (NCO)"]:
                st.subheader("🌳 Dendrogramme (Clustering Hiérarchique)")
                fig_dendro = plot_dendrogram(returns, linkage='ward', codependence='pearson')
                if fig_dendro:
                    st.plotly_chart(fig_dendro, use_container_width=True)
            
            # Tableau de performance
            st.subheader("📊 Tableau de Performance et Indicateurs de Risque")
            
            # Créer un objet portfolio pour calculer les métriques
            port_temp = rp.Portfolio(returns=returns)
            port_temp.assets_stats(method_mu='hist', method_cov='hist')
            port_temp.rf = risk_free_rate
            
            perf_table = get_performance_table(prices, returns, port_temp)
            
            if perf_table is not None:
                # Appliquer des gradients de couleur
                styled_perf = perf_table.style.background_gradient(
                    cmap='RdYlGn', 
                    subset=['Rendement Annuel (%)', 'Ratio de Sharpe']
                ).background_gradient(
                    cmap='RdYlGn_r', 
                    subset=['Volatilité Annuelle (%)', 'Drawdown Maximum (%)', 'VaR 95% (%)', 'CVaR 95% (%)']
                )
                
                st.dataframe(styled_perf, use_container_width=True)
            
            st.markdown("---")
            
            # === SECTION 2: OPTIMISATION DU PORTEFEUILLE ===
            st.header("🎯 Résultats de l'Optimisation")
            
            with st.spinner("Optimisation du portefeuille en cours..."):
                weights, port, returns_calc = calculate_portfolio(
                    prices, 
                    selected_model, 
                    risk_measure, 
                    risk_free_rate, 
                    risk_aversion,
                    uncertainty_param
                )
            
            if weights is not None and port is not None:
                # Display results
                
                # Metrics
                metrics = calculate_metrics(weights, port)
                
                if metrics:
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric(
                            "Rendement Annuel Attendu",
                            f"{metrics['Rendement Annuel Attendu']:.2%}"
                        )
                    
                    with col2:
                        st.metric(
                            "Volatilité Annuelle",
                            f"{metrics['Volatilité Annuelle']:.2%}"
                        )
                    
                    with col3:
                        st.metric(
                            "Ratio de Sharpe",
                            f"{metrics['Ratio de Sharpe']:.2f}"
                        )
                
                # Portfolio weights
                st.subheader("💼 Poids du Portefeuille")
                weights_display = weights.copy()
                weights_display.columns = ['Poids']
                weights_display['Poids (%)'] = weights_display['Poids'] * 100
                weights_display = weights_display[weights_display['Poids'] > 0.001].sort_values('Poids', ascending=False)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.dataframe(
                        weights_display.style.format({'Poids': '{:.4f}', 'Poids (%)': '{:.2f}'}).background_gradient(cmap='Blues', subset=['Poids (%)']),
                        height=400
                    )
                
                with col2:
                    # Pie chart
                    fig_pie = plot_pie_chart(weights)
                    st.plotly_chart(fig_pie, use_container_width=True)
                
                # Bar chart
                st.subheader("📊 Composition du Portefeuille")
                fig_bar = plot_weights(weights)
                st.plotly_chart(fig_bar, use_container_width=True)
                
                # Efficient Frontier (seulement pour les modèles classiques)
                if selected_model not in ["Hierarchical Risk Parity (HRP)", 
                                         "Hierarchical Equal Risk Contribution (HERC)", 
                                         "Nested Clustered Optimization (NCO)"]:
                    st.subheader("📉 Frontière Efficiente")
                    fig_frontier = plot_efficient_frontier(port, weights, risk_measure)
                    if fig_frontier:
                        st.plotly_chart(fig_frontier, use_container_width=True)
                else:
                    st.info("ℹ️ La frontière efficiente n'est pas disponible pour les modèles hiérarchiques.")
                
                # Download weights as CSV
                csv = weights_display.to_csv()
                st.download_button(
                    label="📥 Télécharger les Poids du Portefeuille",
                    data=csv,
                    file_name=f"poids_portefeuille_{selected_model.replace(' ', '_')}.csv",
                    mime="text/csv"
                )
        else:
            st.error("Échec du chargement des données. Veuillez vérifier vos paramètres et réessayer.")
    else:
        # Display instructions
        st.info("👈 Configurez votre portefeuille dans la barre latérale et cliquez sur 'Optimiser le Portefeuille' pour commencer.")

# ============================================================================
# PAGE: À PROPOS
# ============================================================================
def show_about_page():
    st.title("📚 À Propos des Modèles d'Optimisation")
    
    st.markdown("""
    Cette page présente les fondements mathématiques et les objectifs de chaque modèle 
    d'optimisation disponible dans l'application.
    """)
    
    # Portefeuille de Rendement Maximum
    with st.expander("📈 Portefeuille de Rendement Maximum"):
        st.markdown("""
        ### Objectif
        Maximiser le rendement espéré du portefeuille sans contrainte explicite sur le risque.
        
        ### Formulation Mathématique
        
        $$
        \\begin{aligned}
        \\max_{w} \\quad & \\mu^T w \\\\
        \\text{s.t.} \\quad & w^T \\mathbf{1} = 1 \\\\
        & w \\geq 0
        \\end{aligned}
        $$
        
        Où :
        - $w$ : vecteur des poids du portefeuille
        - $\\mu$ : vecteur des rendements espérés
        - $\\mathbf{1}$ : vecteur de uns
        
        ### Caractéristiques
        - Convient aux investisseurs très tolérants au risque
        - Peut conduire à des portefeuilles très concentrés
        - Ne considère pas explicitement la diversification
        """)
    
    # Portefeuille de Risque Minimum
    with st.expander("🛡️ Portefeuille de Risque Minimum"):
        st.markdown("""
        ### Objectif
        Minimiser le risque du portefeuille mesuré par une fonction de risque $\\phi(w)$.
        
        ### Formulation Mathématique
        
        $$
        \\begin{aligned}
        \\min_{w} \\quad & \\phi(w) \\\\
        \\text{s.t.} \\quad & w^T \\mathbf{1} = 1 \\\\
        & w \\geq 0
        \\end{aligned}
        $$
        
        Pour la variance (MV), $\\phi(w) = w^T \\Sigma w$ où $\\Sigma$ est la matrice de covariance.
        
        ### Caractéristiques
        - Idéal pour les investisseurs averses au risque
        - Privilégie la préservation du capital
        - Peut avoir des rendements attendus faibles
        - La mesure de risque $\\phi$ peut être : Variance, CVaR, Drawdown Maximum, etc.
        """)
    
    # Portefeuille de Sharpe Maximum
    with st.expander("⚖️ Portefeuille de Sharpe Maximum"):
        st.markdown("""
        ### Objectif
        Maximiser le ratio de Sharpe, qui mesure le rendement excédentaire par unité de risque.
        
        ### Formulation Mathématique
        
        $$
        \\begin{aligned}
        \\max_{w} \\quad & \\frac{\\mu^T w - r_f}{\\sqrt{w^T \\Sigma w}} \\\\
        \\text{s.t.} \\quad & w^T \\mathbf{1} = 1 \\\\
        & w \\geq 0
        \\end{aligned}
        $$
        
        Où :
        - $r_f$ : taux sans risque
        - $\\Sigma$ : matrice de covariance des rendements
        
        ### Caractéristiques
        - Équilibre optimal entre rendement et risque
        - Convient à la plupart des investisseurs rationnels
        - Correspond au portefeuille tangent sur la frontière efficiente
        - Solution du modèle de Markowitz classique
        """)
    
    # Portefeuille d'Utilité Maximum
    with st.expander("🎯 Portefeuille d'Utilité Maximum"):
        st.markdown("""
        ### Objectif
        Maximiser une fonction d'utilité qui combine rendement et risque selon l'aversion au risque de l'investisseur.
        
        ### Formulation Mathématique
        
        $$
        \\begin{aligned}
        \\max_{w} \\quad & \\mu^T w - \\lambda \\phi(w) \\\\
        \\text{s.t.} \\quad & w^T \\mathbf{1} = 1 \\\\
        & w \\geq 0
        \\end{aligned}
        $$
        
        Où :
        - $\\lambda$ : coefficient d'aversion au risque ($\\lambda > 0$)
        - $\\phi(w)$ : fonction de risque
        
        ### Caractéristiques
        - Permet d'ajuster le compromis rendement-risque via $\\lambda$
        - $\\lambda$ élevé : plus d'aversion au risque, portefeuille plus conservateur
        - $\\lambda$ faible : moins d'aversion au risque, portefeuille plus agressif
        - Basé sur la théorie de l'utilité espérée
        """)
    
    # Portefeuille de Parité de Risque
    with st.expander("⚖️ Portefeuille de Parité de Risque (Risk Parity)"):
        st.markdown("""
        ### Objectif
        Allouer les poids de sorte que chaque actif contribue de manière égale au risque total du portefeuille.
        
        ### Formulation Mathématique
        
        Trouver $w$ tel que :
        
        $$
        RC_i = RC_j \\quad \\forall i, j
        $$
        
        Où la contribution au risque de l'actif $i$ est :
        
        $$
        RC_i = w_i \\frac{\\partial \\phi(w)}{\\partial w_i}
        $$
        
        Pour la variance : $RC_i = w_i (\\Sigma w)_i$
        
        ### Caractéristiques
        - Diversification optimale du risque entre les actifs
        - Ne dépend pas des rendements espérés (approche purement risque)
        - Chaque actif contribue $\\frac{1}{N}$ du risque total
        - Robuste aux erreurs d'estimation des rendements
        """)
    
    # Portefeuille de Parité de Risque Relaxée
    with st.expander("🔓 Portefeuille de Parité de Risque Relaxée"):
        st.markdown("""
        ### Objectif
        Variante du modèle de parité de risque avec des contraintes plus flexibles, permettant une allocation 
        proche de la parité de risque tout en incorporant d'autres considérations.
        
        ### Formulation Mathématique
        
        $$
        \\begin{aligned}
        \\min_{w} \\quad & \\sum_{i=1}^{N} \\left( RC_i - \\frac{1}{N}\\phi(w) \\right)^2 \\\\
        \\text{s.t.} \\quad & w^T \\mathbf{1} = 1 \\\\
        & w \\geq 0 \\\\
        & \\text{contraintes additionnelles}
        \\end{aligned}
        $$
        
        ### Caractéristiques
        - Plus flexible que la parité de risque stricte
        - Permet d'ajouter des contraintes de concentration, de rendement minimal, etc.
        - Recherche une solution proche de la parité de risque tout en respectant les contraintes
        """)
    
    # Portefeuilles Robustes
    with st.expander("🛡️ Portefeuilles Robustes (Worst Case Mean-Variance)"):
        st.markdown("""
        ### Objectif
        Optimiser le portefeuille en tenant compte de l'incertitude dans l'estimation des paramètres 
        (rendements espérés et matrice de covariance).
        
        ### Formulation Mathématique
        
        $$
        \\begin{aligned}
        \\max_{w} \\min_{\\mu \\in U_\\mu, \\Sigma \\in U_\\Sigma} \\quad & f(w, \\mu, \\Sigma) \\\\
        \\text{s.t.} \\quad & w^T \\mathbf{1} = 1 \\\\
        & w \\geq 0
        \\end{aligned}
        $$
        
        Où :
        - $U_\\mu$ : ensemble d'incertitude pour les rendements espérés
        - $U_\\Sigma$ : ensemble d'incertitude pour la matrice de covariance
        - $f(w, \\mu, \\Sigma)$ : fonction objectif (rendement, Sharpe, utilité, etc.)
        
        ### Ensembles d'Incertitude (Box)
        
        $$
        U_\\mu = \\{ \\mu : \\|\\mu - \\hat{\\mu}\\|_\\infty \\leq \\epsilon_\\mu \\}
        $$
        
        $$
        U_\\Sigma = \\{ \\Sigma : \\|\\Sigma - \\hat{\\Sigma}\\|_F \\leq \\epsilon_\\Sigma \\}
        $$
        
        Où $\\epsilon$ est le paramètre d'incertitude contrôlant la taille de l'ensemble.
        
        ### Caractéristiques
        - Protection contre les erreurs d'estimation
        - Solution optimale dans le pire scénario (approche pessimiste)
        - $\\epsilon$ élevé : plus de robustesse, portefeuilles plus conservateurs
        - $\\epsilon$ faible : moins de robustesse, proche de l'optimisation classique
        - 4 variantes : Rendement Max, Risque Min, Sharpe Max, Utilité Max
        """)
    
    # Modèles de Machine Learning
    st.markdown("---")
    st.header("🤖 Modèles de Machine Learning")
    
    # Hierarchical Risk Parity (HRP)
    with st.expander("📊 Hierarchical Risk Parity (HRP)"):
        st.markdown("""
        ### Objectif
        Allouer les poids du portefeuille en utilisant une approche hiérarchique basée sur le clustering 
        des actifs selon leur structure de corrélation, puis en appliquant la parité de risque naive.
        
        ### Méthodologie
        
        Le modèle HRP se décompose en trois étapes principales :
        
        **1. Regroupement Hiérarchique (Tree Clustering)**
        
        Utilise la matrice de distance basée sur les corrélations :
        
        $$
        d_{ij} = \\sqrt{\\frac{1 - \\rho_{ij}}{2}}
        $$
        
        où $\\rho_{ij}$ est la corrélation entre les actifs $i$ et $j$.
        
        **2. Ordonnancement Quasi-Diagonal (Quasi-Diagonalization)**
        
        Réorganise les actifs selon le dendrogramme pour former des clusters cohérents.
        
        **3. Allocation Récursive Bisectionnelle**
        
        Divise récursivement le portefeuille en deux groupes et alloue le capital inversement 
        proportionnel à la variance de chaque groupe :
        
        $$
        w_1 = \\frac{\\sigma_2^{-1}}{\\sigma_1^{-1} + \\sigma_2^{-1}}, \\quad w_2 = 1 - w_1
        $$
        
        ### Caractéristiques
        - ✅ Stable et robuste, peu sensible aux erreurs d'estimation
        - ✅ Ne nécessite pas l'inversion de la matrice de covariance
        - ✅ Peut utiliser 32 mesures de risque différentes
        - ✅ Préserve la structure de corrélation des actifs
        - ✅ Évite les poids négatifs sans contraintes explicites
        - ⚠️ Non optimal au sens de Markowitz
        - 📊 Particulièrement efficace avec des actifs fortement corrélés
        """)
    
    # Hierarchical Equal Risk Contribution (HERC)
    with st.expander("⚖️ Hierarchical Equal Risk Contribution (HERC)"):
        st.markdown("""
        ### Objectif
        Extension du modèle HRP qui alloue le capital de manière à ce que chaque cluster d'actifs 
        contribue de façon égale au risque total du portefeuille.
        
        ### Méthodologie
        
        HERC suit les mêmes étapes que HRP mais avec une allocation différente :
        
        **1-2. Tree Clustering et Quasi-Diagonalization**
        
        Identique à HRP.
        
        **3. Allocation par Contribution au Risque Égale**
        
        Au lieu d'inverser les variances, HERC alloue pour égaliser les contributions au risque :
        
        $$
        RC_i = w_i \\cdot \\sigma_i = \\frac{\\text{Risk Total}}{N_{clusters}}
        $$
        
        où $RC_i$ est la contribution au risque du cluster $i$.
        
        ### Différence avec HRP
        
        | Aspect | HRP | HERC |
        |--------|-----|------|
        | **Allocation** | Inverse de la variance | Contribution au risque égale |
        | **Objectif** | Diversification | Parité de risque par cluster |
        | **Concentration** | Peut être concentré | Plus équilibré |
        
        ### Caractéristiques
        - ✅ Combine clustering hiérarchique et parité de risque
        - ✅ Meilleure diversification que HRP
        - ✅ Contributions au risque équilibrées entre clusters
        - ✅ Peut utiliser 32 mesures de risque différentes
        - ✅ Robuste et stable
        - ⚠️ Calculs légèrement plus complexes que HRP
        - 📊 Idéal quand on veut équilibrer le risque entre secteurs/classes d'actifs
        """)
    
    # Nested Clustered Optimization (NCO)
    with st.expander("🎯 Nested Clustered Optimization (NCO)"):
        st.markdown("""
        ### Objectif
        Combiner l'approche hiérarchique de HRP/HERC avec l'optimisation classique de Markowitz 
        pour obtenir les avantages des deux méthodes.
        
        ### Méthodologie
        
        NCO utilise une approche en deux étapes :
        
        **1. Optimisation Intra-Cluster**
        
        Pour chaque cluster $C_k$ identifié par clustering hiérarchique, optimise localement :
        
        $$
        \\begin{aligned}
        \\max_{w_k} \\quad & \\text{Sharpe}(w_k) = \\frac{\\mu_k^T w_k - r_f}{\\sqrt{w_k^T \\Sigma_k w_k}} \\\\
        \\text{s.t.} \\quad & w_k^T \\mathbf{1} = 1, \\quad w_k \\geq 0
        \\end{aligned}
        $$
        
        où $\\mu_k$ et $\\Sigma_k$ sont limités aux actifs du cluster $C_k$.
        
        **2. Allocation Inter-Cluster**
        
        Alloue le capital entre les portefeuilles optimisés de chaque cluster :
        
        $$
        \\begin{aligned}
        \\max_{\\alpha} \\quad & \\text{Sharpe}(\\alpha) = \\frac{\\mu_c^T \\alpha - r_f}{\\sqrt{\\alpha^T \\Sigma_c \\alpha}} \\\\
        \\text{s.t.} \\quad & \\alpha^T \\mathbf{1} = 1, \\quad \\alpha \\geq 0
        \\end{aligned}
        $$
        
        où $\\mu_c$ et $\\Sigma_c$ sont calculés à partir des portefeuilles de chaque cluster.
        
        **3. Poids Final**
        
        $$
        w_i^{\\text{final}} = \\alpha_{k(i)} \\cdot w_i^{(k)}
        $$
        
        où $k(i)$ est le cluster auquel appartient l'actif $i$.
        
        ### Avantages par rapport à HRP/HERC
        
        | Caractéristique | NCO | HRP/HERC |
        |-----------------|-----|----------|
        | **Optimalité** | Optimisation Markowitz par cluster | Parité de risque naive |
        | **Performance** | Potentiellement supérieure | Plus conservative |
        | **Stabilité** | Moyenne | Élevée |
        | **Complexité** | Élevée | Faible |
        
        ### Caractéristiques
        - ✅ Combine robustesse du clustering et optimalité de Markowitz
        - ✅ Réduit le risque de sur-optimisation
        - ✅ Meilleure performance out-of-sample que Markowitz classique
        - ✅ Exploite la structure de corrélation des actifs
        - ⚠️ Plus complexe à calculer
        - ⚠️ Nécessite suffisamment d'actifs par cluster
        - 📊 Optimal quand les clusters sont bien définis (ex: secteurs, géographies)
        
        ### Quand Utiliser NCO ?
        
        - **Oui** : Portefeuille multi-secteurs ou multi-classes d'actifs
        - **Oui** : Besoin d'optimisation mais avec structure hiérarchique
        - **Oui** : Données historiques suffisantes par cluster
        - **Non** : Peu d'actifs (< 15-20)
        - **Non** : Clusters mal définis ou très corrélés
        """)
    
    # Mesures de Risque
    st.markdown("---")
    st.header("📊 Mesures de Risque")
    
    with st.expander("Voir toutes les mesures de risque"):
        st.markdown("""
        ### Variance (MV) - Écart-type
        $$\\phi(w) = \\sqrt{w^T \\Sigma w}$$
        Mesure classique de dispersion des rendements.
        
        ### Écart Absolu Moyen (MAD)
        $$\\phi(w) = E[|r_p - E[r_p]|]$$
        Moyenne des écarts absolus par rapport à la moyenne.
        
        ### Semi-Variance (MSV)
        $$\\phi(w) = E[\\min(r_p - E[r_p], 0)^2]$$
        Mesure uniquement la volatilité des rendements négatifs.
        
        ### Valeur à Risque Conditionnelle (CVaR)
        $$\\text{CVaR}_\\alpha(w) = E[r_p | r_p \\leq \\text{VaR}_\\alpha(w)]$$
        Moyenne des pertes au-delà du VaR (Expected Shortfall).
        
        ### Drawdown Maximum (MDD)
        $$\\text{MDD}(w) = \\max_{t} \\left( \\max_{s \\leq t} V_s - V_t \\right) / \\max_{s \\leq t} V_s$$
        Plus grande baisse depuis un pic historique.
        
        ### Drawdown Conditionnel à Risque (CDaR)
        $$\\text{CDaR}_\\alpha(w) = E[DD | DD \\geq \\text{DaR}_\\alpha]$$
        CVaR appliqué aux drawdowns.
        
        Et bien d'autres mesures spécialisées...
        """)
    
    # Les 32 mesures de risque pour HRP/HERC
    with st.expander("📋 Les 32 Mesures de Risque pour HRP et HERC"):
        st.markdown("""
        Les modèles HRP et HERC peuvent utiliser **32 mesures de risque différentes** pour la parité de risque naive, 
        offrant une flexibilité exceptionnelle.
        
        ### 🔵 1. Mesures de Dispersion (8 mesures)
        
        **Standard Deviation (vol)**
        $$\\sigma = \\sqrt{\\frac{1}{n}\\sum_{i=1}^{n}(r_i - \\bar{r})^2}$$
        Mesure classique de volatilité.
        
        **Variance**
        $$\\text{Var} = \\sigma^2$$
        Carré de l'écart-type.
        
        **Square Root Kurtosis (kurt)**
        $$\\text{Kurt}^{1/4} = \\left(\\frac{1}{n}\\sum_{i=1}^{n}\\frac{(r_i - \\bar{r})^4}{\\sigma^4}\\right)^{1/4}$$
        Mesure la "queue" de la distribution.
        
        **Mean Absolute Deviation (MAD)**
        $$\\text{MAD} = \\frac{1}{n}\\sum_{i=1}^{n}|r_i - \\bar{r}|$$
        Moyenne des écarts absolus.
        
        **Gini Mean Difference (GMD)**
        $$\\text{GMD} = \\frac{1}{n(n-1)}\\sum_{i=1}^{n}\\sum_{j=1}^{n}|r_i - r_j|$$
        Différence moyenne entre toutes les paires.
        
        **CVaR Range (cvrg)**
        $$\\text{CVaR Range} = \\text{CVaR}^+ - \\text{CVaR}^-$$
        Plage entre CVaR positif et négatif.
        
        **Tail Gini Range (tgrg)**
        Gini calculé sur les queues de distribution.
        
        **Range (rg)**
        $$\\text{Range} = \\max(r) - \\min(r)$$
        Différence entre max et min.
        
        ---
        
        ### 🔴 2. Mesures de Risque à la Baisse (10 mesures)
        
        **Semi Standard Deviation (semi)**
        $$\\text{SemiSD} = \\sqrt{\\frac{1}{n}\\sum_{r_i<0}r_i^2}$$
        Volatilité des rendements négatifs uniquement.
        
        **Square Root Semi Kurtosis (skurt)**
        Kurtosis calculée sur les rendements négatifs.
        
        **First Lower Partial Moment (flpm) - Omega Ratio**
        $$\\text{FLPM} = \\frac{1}{n}\\sum_{r_i<\\tau}(\\tau - r_i)$$
        Moyenne des shortfalls par rapport à un seuil $\\tau$.
        
        **Second Lower Partial Moment (slpm) - Sortino Ratio**
        $$\\text{SLPM} = \\sqrt{\\frac{1}{n}\\sum_{r_i<\\tau}(\\tau - r_i)^2}$$
        Racine carrée des écarts carrés négatifs.
        
        **Value at Risk (VaR)**
        $$\\text{VaR}_\\alpha = -\\inf\\{x : P(r \\leq x) \\geq \\alpha\\}$$
        Perte maximale avec probabilité $\\alpha$ (ex: 95%).
        
        **Conditional Value at Risk (CVaR)**
        $$\\text{CVaR}_\\alpha = E[r | r \\leq \\text{VaR}_\\alpha]$$
        Moyenne des pertes au-delà du VaR.
        
        **Entropic Value at Risk (EVaR)**
        $$\\text{EVaR}_\\alpha = \\inf_{z>0}\\left\\{z\\ln\\left(\\frac{1}{\\alpha}\\right) + z\\ln\\left(E[e^{-r/z}]\\right)\\right\\}$$
        Version entropique du VaR.
        
        **Relativistic Value at Risk (RLVaR)**
        Variante relativiste tenant compte de la distribution complète.
        
        **Tail Gini (tg)**
        $$\\text{TG} = \\frac{1}{n_\\alpha(n_\\alpha-1)}\\sum_{r_i \\leq \\text{VaR}}\\sum_{r_j \\leq \\text{VaR}}|r_i - r_j|$$
        Gini sur la queue de distribution.
        
        **Worst Realization (wr) - Minimax**
        $$\\text{WR} = \\min(r)$$
        Le pire rendement observé.
        
        ---
        
        ### 📉 3. Mesures de Drawdown (14 mesures)
        
        #### Rendements Composés (7 mesures)
        
        **Maximum Drawdown (mdd) - Calmar Ratio**
        $$\\text{MDD} = \\max_{t}\\left(\\frac{\\max_{s \\leq t}V_s - V_t}{\\max_{s \\leq t}V_s}\\right)$$
        Plus grande baisse depuis un pic.
        
        **Average Drawdown (add)**
        $$\\text{ADD} = \\frac{1}{T}\\sum_{t=1}^{T}\\text{DD}_t$$
        Moyenne de tous les drawdowns.
        
        **Ulcer Index (uci)**
        $$\\text{UCI} = \\sqrt{\\frac{1}{T}\\sum_{t=1}^{T}\\text{DD}_t^2}$$
        Racine carrée de la moyenne des drawdowns carrés.
        
        **Drawdown at Risk (dar)**
        $$\\text{DaR}_\\alpha = -\\inf\\{x : P(\\text{DD} \\leq x) \\geq \\alpha\\}$$
        VaR appliqué aux drawdowns.
        
        **Conditional Drawdown at Risk (cdar)**
        $$\\text{CDaR}_\\alpha = E[\\text{DD} | \\text{DD} \\geq \\text{DaR}_\\alpha]$$
        CVaR appliqué aux drawdowns.
        
        **Entropic Drawdown at Risk (edar)**
        EVaR appliqué aux drawdowns.
        
        **Relativistic Drawdown at Risk (rdar)**
        RLVaR appliqué aux drawdowns.
        
        #### Rendements Non Composés (7 mesures)
        
        Les mêmes 7 mesures calculées sur les rendements arithmétiques (non composés) :
        - **mdd_rel**, **add_rel**, **uci_rel**
        - **dar_rel**, **cdar_rel**, **edar_rel**, **rdar_rel**
        
        Utile pour les portefeuilles avec rééquilibrage fréquent.
        
        ---
        
        ### 📊 Tableau Récapitulatif
        
        | Catégorie | Nombre | Exemples Clés |
        |-----------|--------|---------------|
        | **Dispersion** | 8 | vol, variance, mad, gmd |
        | **Downside** | 10 | semi, var, cvar, evar |
        | **Drawdown Composé** | 7 | mdd, cdar, uci |
        | **Drawdown Non Composé** | 7 | mdd_rel, cdar_rel, uci_rel |
        | **TOTAL** | **32** | - |
        
        ### 💡 Recommandations
        
        **Pour la plupart des cas** : `vol` (Standard Deviation)
        - Simple et intuitif
        - Comparable à Markowitz
        
        **Pour risque asymétrique** : `cvar` ou `semi`
        - Mesure uniquement le risque de baisse
        - Mieux adapté aux rendements non-normaux
        
        **Pour gestion de drawdown** : `cdar` ou `mdd`
        - Focus sur les pertes cumulées
        - Pertinent pour allocation long-terme
        
        **Pour robustesse** : `mad` ou `gmd`
        - Moins sensibles aux valeurs extrêmes
        - Alternatives robustes à la variance
        """)
    
    # Théorie de Markowitz
    st.markdown("---")
    st.header("📐 Théorie Moderne du Portefeuille (Markowitz)")
    
    st.markdown("""
    ### Fondements
    
    La théorie moderne du portefeuille, développée par Harry Markowitz (Prix Nobel 1990), 
    repose sur les principes suivants :
    
    1. **Frontière Efficiente** : Ensemble des portefeuilles offrant le rendement maximum pour un 
       niveau de risque donné, ou le risque minimum pour un niveau de rendement donné.
    
    2. **Diversification** : Réduction du risque par la combinaison d'actifs dont les rendements 
       ne sont pas parfaitement corrélés.
    
    3. **Compromis Rendement-Risque** : Les investisseurs cherchent à maximiser le rendement 
       pour un niveau de risque acceptable, ou minimiser le risque pour un rendement cible.
    
    ### Hypothèses Clés
    
    - Les rendements suivent une distribution normale
    - Les investisseurs sont rationnels et averses au risque
    - Les marchés sont efficients
    - Pas de coûts de transaction ni d'impôts
    - Les investisseurs peuvent prêter et emprunter au taux sans risque
    
    ### Extensions et Améliorations
    
    Les modèles modernes (comme ceux de Riskfolio-Lib) étendent la théorie de Markowitz en :
    
    - Utilisant des mesures de risque alternatives (CVaR, Drawdown, etc.)
    - Incorporant la robustesse face à l'incertitude
    - Permettant des contraintes réalistes (concentration, secteur, ESG, etc.)
    - Utilisant des distributions non-normales
    """)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    ### 📖 Références
    
    **Théorie Classique**
    - Markowitz, H. (1952). "Portfolio Selection". The Journal of Finance.
    - Rockafellar, R. T., & Uryasev, S. (2000). "Optimization of conditional value-at-risk."
    - Maillard, S., Roncalli, T., & Teïletche, J. (2010). "The properties of equally weighted risk contribution portfolios."
    - Ben-Tal, A., & Nemirovski, A. (1998). "Robust convex optimization."
    
    **Modèles de Machine Learning**
    - López de Prado, M. (2016). "Building Diversified Portfolios that Outperform Out of Sample". Journal of Portfolio Management.
    - Raffinot, T. (2017). "Hierarchical Clustering-Based Asset Allocation". Journal of Portfolio Management.
    - López de Prado, M. (2020). "Machine Learning for Asset Managers". Cambridge University Press.
    - Raffinot, T. (2018). "The Hierarchical Equal Risk Contribution Portfolio". SSRN Working Paper.
    
    ### 🔗 Liens Utiles
    
    - [Documentation Riskfolio-Lib](https://riskfolio-lib.readthedocs.io/)
    - [Code source sur GitHub](https://github.com/dcajasn/Riskfolio-Lib)
    - [Article HRP - López de Prado](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2708678)
    - [Article HERC - Raffinot](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3237540)
    """)

# ============================================================================
# MAIN APPLICATION ROUTING
# ============================================================================

if st.session_state.page == "Accueil":
    show_home_page()
elif st.session_state.page == "Optimisation":
    show_optimization_page()
elif st.session_state.page == "À propos":
    show_about_page()
