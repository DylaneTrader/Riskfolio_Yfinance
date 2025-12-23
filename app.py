"""
Portfolio Optimization Application with Riskfolio-Lib, Plotly, and yfinance
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

warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Portfolio Optimization App",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title and description
st.title("📊 Portfolio Optimization with Riskfolio-Lib")
st.markdown("""
This application allows you to optimize portfolios using various optimization models:
- Maximum Return Portfolio
- Minimum Risk Portfolio
- Maximum Risk Adjusted Return Ratio Portfolio
- Maximum Utility Portfolio
- Risk Parity Portfolio
- Relaxed Risk Parity Portfolio
- Worst Case Mean Variance Portfolio Optimization
""")

# Sidebar for inputs
st.sidebar.header("Portfolio Configuration")

# Default tickers
default_tickers = "AAPL,MSFT,GOOGL,AMZN,TSLA,JPM,JNJ,V,PG,NVDA"
tickers_input = st.sidebar.text_area(
    "Enter Stock Tickers (comma-separated)",
    value=default_tickers,
    help="Enter stock tickers separated by commas"
)

# Parse tickers
tickers = [ticker.strip().upper() for ticker in tickers_input.split(",") if ticker.strip()]

# Date range selection
st.sidebar.subheader("Date Range")
end_date = st.sidebar.date_input(
    "End Date",
    value=datetime.now(),
    max_value=datetime.now()
)
start_date = st.sidebar.date_input(
    "Start Date",
    value=end_date - timedelta(days=365*2),
    max_value=end_date
)

# Portfolio optimization model selection
st.sidebar.subheader("Optimization Model")
optimization_models = [
    "Maximum Return Portfolio",
    "Minimum Risk Portfolio",
    "Maximum Risk Adjusted Return Ratio Portfolio",
    "Maximum Utility Portfolio",
    "Risk Parity Portfolio",
    "Relaxed Risk Parity Portfolio",
    "Worst Case Mean Variance - Maximum Return",
    "Worst Case Mean Variance - Minimum Risk",
    "Worst Case Mean Variance - Maximum Sharpe Ratio",
    "Worst Case Mean Variance - Maximum Utility"
]

selected_model = st.sidebar.selectbox(
    "Select Optimization Model",
    options=optimization_models
)

# Risk measure selection
risk_measures = ["MV", "MAD", "MSV", "FLPM", "SLPM", "CVaR", "EVaR", "WR", "MDD", "ADD", "CDaR", "UCI", "EDaR"]
risk_measure = st.sidebar.selectbox(
    "Risk Measure",
    options=risk_measures,
    index=0,
    help="MV: Standard Deviation, CVaR: Conditional Value at Risk, etc."
)

# Additional parameters
st.sidebar.subheader("Additional Parameters")
risk_free_rate = st.sidebar.number_input(
    "Risk-Free Rate (%)",
    min_value=0.0,
    max_value=10.0,
    value=2.5,
    step=0.1
) / 100

risk_aversion = st.sidebar.number_input(
    "Risk Aversion (λ)",
    min_value=0.1,
    max_value=10.0,
    value=2.0,
    step=0.1,
    help="Used for Maximum Utility Portfolio"
)

# Uncertainty set parameter for Worst Case
uncertainty_param = st.sidebar.number_input(
    "Uncertainty Parameter (ε)",
    min_value=0.0,
    max_value=1.0,
    value=0.5,
    step=0.05,
    help="Used for Worst Case Mean Variance models"
)

# Button to run optimization
run_optimization = st.sidebar.button("🚀 Optimize Portfolio", type="primary")

# Functions
@st.cache_data
def download_data(tickers, start_date, end_date):
    """Download historical price data from Yahoo Finance"""
    try:
        data = yf.download(tickers, start=start_date, end=end_date, progress=False)
        if isinstance(data.columns, pd.MultiIndex):
            prices = data['Adj Close']
        else:
            prices = data[['Adj Close']]
        
        # Clean data
        prices = prices.dropna(how='all')
        prices = prices.fillna(method='ffill').fillna(method='bfill')
        
        return prices
    except Exception as e:
        st.error(f"Error downloading data: {str(e)}")
        return None

def calculate_portfolio(prices, model, risk_measure, rf, risk_aversion, uncertainty):
    """Calculate optimal portfolio weights based on selected model"""
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
        
        if model == "Maximum Return Portfolio":
            w = port.optimization(model='Classic', rm=risk_measure, obj='MaxRet', rf=rf, l=0, hist=True)
            
        elif model == "Minimum Risk Portfolio":
            w = port.optimization(model='Classic', rm=risk_measure, obj='MinRisk', rf=rf, l=0, hist=True)
            
        elif model == "Maximum Risk Adjusted Return Ratio Portfolio":
            w = port.optimization(model='Classic', rm=risk_measure, obj='Sharpe', rf=rf, l=0, hist=True)
            
        elif model == "Maximum Utility Portfolio":
            w = port.optimization(model='Classic', rm=risk_measure, obj='Utility', rf=rf, l=risk_aversion, hist=True)
            
        elif model == "Risk Parity Portfolio":
            w = port.rp_optimization(model='Classic', rm=risk_measure, rf=rf, b=None, hist=True)
            
        elif model == "Relaxed Risk Parity Portfolio":
            # Relaxed risk parity with constraints
            w = port.rrp_optimization(model='Classic', rm=risk_measure, rf=rf, b=None, hist=True)
            
        elif model.startswith("Worst Case Mean Variance"):
            # Worst case optimization
            if "Maximum Return" in model:
                w = port.wc_optimization(model='Classic', rm=risk_measure, obj='MaxRet', rf=rf, l=0, Umu='box', Ucov='box', epsilon=uncertainty)
            elif "Minimum Risk" in model:
                w = port.wc_optimization(model='Classic', rm=risk_measure, obj='MinRisk', rf=rf, l=0, Umu='box', Ucov='box', epsilon=uncertainty)
            elif "Maximum Sharpe Ratio" in model:
                w = port.wc_optimization(model='Classic', rm=risk_measure, obj='Sharpe', rf=rf, l=0, Umu='box', Ucov='box', epsilon=uncertainty)
            elif "Maximum Utility" in model:
                w = port.wc_optimization(model='Classic', rm=risk_measure, obj='Utility', rf=rf, l=risk_aversion, Umu='box', Ucov='box', epsilon=uncertainty)
        
        if w is None or w.sum().sum() == 0:
            st.error("Optimization failed. Try different parameters.")
            return None, None
            
        return w, port
        
    except Exception as e:
        st.error(f"Error in optimization: {str(e)}")
        return None, None

def calculate_metrics(weights, port):
    """Calculate portfolio metrics"""
    try:
        metrics = {}
        
        # Expected return
        metrics['Expected Return (Annual)'] = (port.mu @ weights).iloc[0, 0] * 252
        
        # Volatility
        metrics['Volatility (Annual)'] = np.sqrt(weights.T @ port.cov @ weights).iloc[0, 0] * np.sqrt(252)
        
        # Sharpe Ratio
        if metrics['Volatility (Annual)'] > 0:
            metrics['Sharpe Ratio'] = (metrics['Expected Return (Annual)'] - port.rf) / metrics['Volatility (Annual)']
        else:
            metrics['Sharpe Ratio'] = 0
        
        return metrics
    except Exception as e:
        st.error(f"Error calculating metrics: {str(e)}")
        return None

def plot_weights(weights):
    """Plot portfolio weights as a bar chart"""
    weights_df = weights.copy()
    weights_df.columns = ['Weight']
    weights_df = weights_df[weights_df['Weight'] > 0.001].sort_values('Weight', ascending=False)
    
    fig = go.Figure(data=[
        go.Bar(
            x=weights_df.index,
            y=weights_df['Weight'] * 100,
            marker_color='indianred'
        )
    ])
    
    fig.update_layout(
        title="Portfolio Weights",
        xaxis_title="Assets",
        yaxis_title="Weight (%)",
        height=400,
        showlegend=False
    )
    
    return fig

def plot_pie_chart(weights):
    """Plot portfolio weights as a pie chart"""
    weights_df = weights.copy()
    weights_df.columns = ['Weight']
    weights_df = weights_df[weights_df['Weight'] > 0.001]
    
    fig = go.Figure(data=[go.Pie(
        labels=weights_df.index,
        values=weights_df['Weight'],
        hole=.3
    )])
    
    fig.update_layout(
        title="Portfolio Allocation",
        height=400
    )
    
    return fig

def plot_efficient_frontier(port, weights, risk_measure):
    """Plot efficient frontier"""
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
            name='Efficient Frontier',
            line=dict(color='blue', width=2)
        ))
        
        # Current portfolio
        fig.add_trace(go.Scatter(
            x=[current_vol],
            y=[current_ret],
            mode='markers',
            name='Selected Portfolio',
            marker=dict(color='red', size=12, symbol='star')
        ))
        
        fig.update_layout(
            title="Efficient Frontier",
            xaxis_title="Risk (Volatility)",
            yaxis_title="Expected Return",
            height=500,
            showlegend=True
        )
        
        return fig
    except Exception as e:
        st.warning(f"Could not plot efficient frontier: {str(e)}")
        return None

# Main application logic
if run_optimization:
    if len(tickers) < 2:
        st.error("Please enter at least 2 stock tickers.")
    else:
        with st.spinner("Downloading data and optimizing portfolio..."):
            # Download data
            prices = download_data(tickers, start_date, end_date)
            
            if prices is not None and not prices.empty:
                st.success(f"✅ Successfully downloaded data for {len(prices.columns)} assets")
                
                # Show data preview
                with st.expander("📊 View Price Data"):
                    st.dataframe(prices.tail(10))
                
                # Calculate optimal portfolio
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
                    st.header("📈 Optimization Results")
                    
                    # Metrics
                    metrics = calculate_metrics(weights, port)
                    
                    if metrics:
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.metric(
                                "Expected Annual Return",
                                f"{metrics['Expected Return (Annual)']:.2%}"
                            )
                        
                        with col2:
                            st.metric(
                                "Annual Volatility",
                                f"{metrics['Volatility (Annual)']:.2%}"
                            )
                        
                        with col3:
                            st.metric(
                                "Sharpe Ratio",
                                f"{metrics['Sharpe Ratio']:.2f}"
                            )
                    
                    # Portfolio weights
                    st.subheader("Portfolio Weights")
                    weights_display = weights.copy()
                    weights_display.columns = ['Weight']
                    weights_display['Weight (%)'] = weights_display['Weight'] * 100
                    weights_display = weights_display[weights_display['Weight'] > 0.001].sort_values('Weight', ascending=False)
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.dataframe(
                            weights_display.style.format({'Weight': '{:.4f}', 'Weight (%)': '{:.2f}'}),
                            height=400
                        )
                    
                    with col2:
                        # Pie chart
                        fig_pie = plot_pie_chart(weights)
                        st.plotly_chart(fig_pie, use_container_width=True)
                    
                    # Bar chart
                    st.subheader("Portfolio Composition")
                    fig_bar = plot_weights(weights)
                    st.plotly_chart(fig_bar, use_container_width=True)
                    
                    # Efficient Frontier
                    st.subheader("Efficient Frontier")
                    fig_frontier = plot_efficient_frontier(port, weights, risk_measure)
                    if fig_frontier:
                        st.plotly_chart(fig_frontier, use_container_width=True)
                    
                    # Download weights as CSV
                    csv = weights_display.to_csv()
                    st.download_button(
                        label="📥 Download Portfolio Weights",
                        data=csv,
                        file_name=f"portfolio_weights_{selected_model.replace(' ', '_')}.csv",
                        mime="text/csv"
                    )
            else:
                st.error("Failed to download data. Please check your tickers and try again.")
else:
    # Display instructions
    st.info("👈 Configure your portfolio in the sidebar and click 'Optimize Portfolio' to get started.")
    
    # Display sample information
    st.header("📚 About the Optimization Models")
    
    with st.expander("Maximum Return Portfolio"):
        st.write("""
        Maximizes the expected return of the portfolio without considering risk.
        This model is suitable for highly risk-tolerant investors.
        """)
    
    with st.expander("Minimum Risk Portfolio"):
        st.write("""
        Minimizes the portfolio risk based on the selected risk measure.
        This is suitable for risk-averse investors seeking capital preservation.
        """)
    
    with st.expander("Maximum Risk Adjusted Return Ratio Portfolio (Sharpe)"):
        st.write("""
        Maximizes the Sharpe ratio, which is the excess return per unit of risk.
        This balances return and risk optimally for most investors.
        """)
    
    with st.expander("Maximum Utility Portfolio"):
        st.write("""
        Maximizes investor utility based on a risk aversion parameter (λ).
        Higher λ values indicate greater risk aversion.
        """)
    
    with st.expander("Risk Parity Portfolio"):
        st.write("""
        Allocates portfolio weights so that each asset contributes equally to portfolio risk.
        This approach diversifies risk contributions across assets.
        """)
    
    with st.expander("Relaxed Risk Parity Portfolio"):
        st.write("""
        A variant of risk parity that allows for more flexible constraints
        while still targeting equal risk contributions.
        """)
    
    with st.expander("Worst Case Mean Variance Portfolio"):
        st.write("""
        Robust optimization that accounts for uncertainty in the estimates of returns and covariances.
        The uncertainty parameter (ε) controls the size of the uncertainty set.
        Suitable when you want protection against estimation errors.
        """)

# Footer
st.markdown("---")
st.markdown("""
**Data Source:** Yahoo Finance via yfinance  
**Optimization Library:** Riskfolio-Lib  
**Visualization:** Plotly  
""")
