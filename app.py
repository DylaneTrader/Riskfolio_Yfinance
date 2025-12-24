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

# Dictionnaire de traduction des mesures de risque
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
    """Calcule les poids optimaux du portefeuille selon le modèle sélectionné"""
    try:
        # Calculate returns
        returns = prices.pct_change().dropna()
        
        # Create portfolio object
        port = rp.Portfolio(returns=returns)
        
        # Calculate mean and covariance
        method_mu = 'hist'  # Historical mean
        method_cov = 'hist'  # Historical covariance
        
        port.assets_stats(method_mu=method_mu, method_cov=method_cov)
        
        # Set risk-free rate
        port.rf = rf
        
        # Optimize based on selected model
        w = None
        
        if model == "Portefeuille de Rendement Maximum":
            w = port.optimization(model='Classic', rm=risk_measure, obj='MaxRet', rf=rf, l=0, hist=True)
            
        elif model == "Portefeuille de Risque Minimum":
            w = port.optimization(model='Classic', rm=risk_measure, obj='MinRisk', rf=rf, l=0, hist=True)
            
        elif model == "Portefeuille de Sharpe Maximum":
            w = port.optimization(model='Classic', rm=risk_measure, obj='Sharpe', rf=rf, l=0, hist=True)
            
        elif model == "Portefeuille d'Utilité Maximum":
            w = port.optimization(model='Classic', rm=risk_measure, obj='Utility', rf=rf, l=risk_aversion, hist=True)
            
        elif model == "Portefeuille de Parité de Risque":
            w = port.rp_optimization(model='Classic', rm=risk_measure, rf=rf, b=None, hist=True)
            
        elif model == "Portefeuille de Parité de Risque Relaxée":
            # Relaxed risk parity with constraints
            w = port.rrp_optimization(model='Classic', rm=risk_measure, rf=rf, b=None, hist=True)
            
        elif model.startswith("Portefeuille Robuste"):
            # Worst case optimization
            if "Rendement Maximum" in model:
                w = port.wc_optimization(model='Classic', rm=risk_measure, obj='MaxRet', rf=rf, l=0, Umu='box', Ucov='box', epsilon=uncertainty)
            elif "Risque Minimum" in model:
                w = port.wc_optimization(model='Classic', rm=risk_measure, obj='MinRisk', rf=rf, l=0, Umu='box', Ucov='box', epsilon=uncertainty)
            elif "Sharpe Maximum" in model:
                w = port.wc_optimization(model='Classic', rm=risk_measure, obj='Sharpe', rf=rf, l=0, Umu='box', Ucov='box', epsilon=uncertainty)
            elif "Utilité Maximum" in model:
                w = port.wc_optimization(model='Classic', rm=risk_measure, obj='Utility', rf=rf, l=risk_aversion, Umu='box', Ucov='box', epsilon=uncertainty)
        
        if w is None or w.sum().sum() == 0:
            st.error("L'optimisation a échoué. Essayez différents paramètres.")
            return None, None
            
        return w, port
        
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

# ============================================================================
# PAGE: ACCUEIL
# ============================================================================
def show_home_page():
    st.title("📊 Optimisation de Portefeuille avec Riskfolio-Lib")
    
    st.markdown("""
    ## Bienvenue dans l'Application d'Optimisation de Portefeuille
    
    Cette application vous permet d'optimiser des portefeuilles financiers en utilisant diverses 
    méthodes quantitatives avancées basées sur la bibliothèque **Riskfolio-Lib**.
    
    ### 🎯 Fonctionnalités Principales
    
    - **Multiples Modèles d'Optimisation**: Choisissez parmi 10 modèles différents
    - **Mesures de Risque Variées**: 13 mesures de risque disponibles
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
        st.info("**10** Modèles d'Optimisation")
    
    with col2:
        st.info("**13** Mesures de Risque")
    
    with col3:
        st.info("**3** Sources de Données")
    
    st.markdown("---")
    
    st.markdown("""
    ### 📚 Modèles Disponibles
    
    - Portefeuille de Rendement Maximum
    - Portefeuille de Risque Minimum
    - Portefeuille de Sharpe Maximum
    - Portefeuille d'Utilité Maximum
    - Portefeuille de Parité de Risque
    - Portefeuille de Parité de Risque Relaxée
    - Portefeuilles Robustes (4 variantes)
    
    ### 🔍 Mesures de Risque
    
    Variance, CVaR, Drawdown Maximum, et bien d'autres...
    
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
        "Portefeuille Robuste - Utilité Maximum"
    ]
    
    selected_model = st.sidebar.selectbox(
        "Sélectionnez le modèle d'optimisation",
        options=optimization_models
    )
    
    # Risk measure selection
    st.sidebar.subheader("Mesure de Risque")
    risk_measures = list(RISK_MEASURES_DICT.keys())
    risk_measure_names = [f"{k}: {v}" for k, v in RISK_MEASURES_DICT.items()]
    
    selected_risk_index = st.sidebar.selectbox(
        "Sélectionnez la mesure de risque",
        options=range(len(risk_measures)),
        format_func=lambda x: risk_measure_names[x],
        index=0
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
            returns = prices.pct_change().dropna()
            fig_corr = plot_correlation_matrix(returns)
            st.plotly_chart(fig_corr, use_container_width=True)
            
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
            
            # Calculate optimal portfolio
            st.header("🎯 Résultats de l'Optimisation")
            
            weights, port = calculate_portfolio(
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
                
                # Efficient Frontier
                st.subheader("📉 Frontière Efficiente")
                fig_frontier = plot_efficient_frontier(port, weights, risk_measure)
                if fig_frontier:
                    st.plotly_chart(fig_frontier, use_container_width=True)
                
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
    
    - Markowitz, H. (1952). "Portfolio Selection". The Journal of Finance.
    - Rockafellar, R. T., & Uryasev, S. (2000). "Optimization of conditional value-at-risk."
    - Maillard, S., Roncalli, T., & Teïletche, J. (2010). "The properties of equally weighted risk contribution portfolios."
    - Ben-Tal, A., & Nemirovski, A. (1998). "Robust convex optimization."
    
    ### 🔗 Liens Utiles
    
    - [Documentation Riskfolio-Lib](https://riskfolio-lib.readthedocs.io/)
    - [Code source sur GitHub](https://github.com/dcajasn/Riskfolio-Lib)
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
