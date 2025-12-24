"""
Modèles d'optimisation classiques de portefeuille
"""

import riskfolio as rp
import streamlit as st


def optimize_max_return(returns, risk_measure, rf, **kwargs):
    """
    Optimise le portefeuille pour maximiser le rendement
    
    Parameters:
    -----------
    returns : pd.DataFrame
        Matrice des rendements historiques
    risk_measure : str
        Mesure de risque à utiliser
    rf : float
        Taux sans risque
    
    Returns:
    --------
    tuple : (weights, portfolio_object, returns)
    """
    try:
        port = rp.Portfolio(returns=returns)
        port.assets_stats(method_mu='hist', method_cov='hist')
        port.rf = rf
        
        w = port.optimization(model='Classic', rm=risk_measure, obj='MaxRet', rf=rf, l=0, hist=True)
        
        return w, port, returns
    except Exception as e:
        st.error(f"Erreur dans optimize_max_return: {str(e)}")
        return None, None, None


def optimize_min_risk(returns, risk_measure, rf, **kwargs):
    """
    Optimise le portefeuille pour minimiser le risque
    
    Parameters:
    -----------
    returns : pd.DataFrame
        Matrice des rendements historiques
    risk_measure : str
        Mesure de risque à utiliser
    rf : float
        Taux sans risque
    
    Returns:
    --------
    tuple : (weights, portfolio_object, returns)
    """
    try:
        port = rp.Portfolio(returns=returns)
        port.assets_stats(method_mu='hist', method_cov='hist')
        port.rf = rf
        
        w = port.optimization(model='Classic', rm=risk_measure, obj='MinRisk', rf=rf, l=0, hist=True)
        
        return w, port, returns
    except Exception as e:
        st.error(f"Erreur dans optimize_min_risk: {str(e)}")
        return None, None, None


def optimize_max_sharpe(returns, risk_measure, rf, **kwargs):
    """
    Optimise le portefeuille pour maximiser le ratio de Sharpe
    
    Parameters:
    -----------
    returns : pd.DataFrame
        Matrice des rendements historiques
    risk_measure : str
        Mesure de risque à utiliser
    rf : float
        Taux sans risque
    
    Returns:
    --------
    tuple : (weights, portfolio_object, returns)
    """
    try:
        port = rp.Portfolio(returns=returns)
        port.assets_stats(method_mu='hist', method_cov='hist')
        port.rf = rf
        
        w = port.optimization(model='Classic', rm=risk_measure, obj='Sharpe', rf=rf, l=0, hist=True)
        
        return w, port, returns
    except Exception as e:
        st.error(f"Erreur dans optimize_max_sharpe: {str(e)}")
        return None, None, None


def optimize_max_utility(returns, risk_measure, rf, risk_aversion=2.0, **kwargs):
    """
    Optimise le portefeuille pour maximiser l'utilité
    
    Parameters:
    -----------
    returns : pd.DataFrame
        Matrice des rendements historiques
    risk_measure : str
        Mesure de risque à utiliser
    rf : float
        Taux sans risque
    risk_aversion : float
        Coefficient d'aversion au risque (lambda)
    
    Returns:
    --------
    tuple : (weights, portfolio_object, returns)
    """
    try:
        port = rp.Portfolio(returns=returns)
        port.assets_stats(method_mu='hist', method_cov='hist')
        port.rf = rf
        
        w = port.optimization(model='Classic', rm=risk_measure, obj='Utility', rf=rf, l=risk_aversion, hist=True)
        
        return w, port, returns
    except Exception as e:
        st.error(f"Erreur dans optimize_max_utility: {str(e)}")
        return None, None, None


def optimize_risk_parity(returns, risk_measure, rf, **kwargs):
    """
    Optimise le portefeuille selon le principe de parité de risque
    
    Parameters:
    -----------
    returns : pd.DataFrame
        Matrice des rendements historiques
    risk_measure : str
        Mesure de risque à utiliser
    rf : float
        Taux sans risque
    
    Returns:
    --------
    tuple : (weights, portfolio_object, returns)
    """
    try:
        port = rp.Portfolio(returns=returns)
        port.assets_stats(method_mu='hist', method_cov='hist')
        port.rf = rf
        
        w = port.rp_optimization(model='Classic', rm=risk_measure, rf=rf, b=None, hist=True)
        
        return w, port, returns
    except Exception as e:
        st.error(f"Erreur dans optimize_risk_parity: {str(e)}")
        return None, None, None


def optimize_relaxed_risk_parity(returns, risk_measure, rf, **kwargs):
    """
    Optimise le portefeuille selon le principe de parité de risque relaxée
    
    Parameters:
    -----------
    returns : pd.DataFrame
        Matrice des rendements historiques
    risk_measure : str
        Mesure de risque à utiliser
    rf : float
        Taux sans risque
    
    Returns:
    --------
    tuple : (weights, portfolio_object, returns)
    """
    try:
        port = rp.Portfolio(returns=returns)
        port.assets_stats(method_mu='hist', method_cov='hist')
        port.rf = rf
        
        w = port.rrp_optimization(model='Classic', rm=risk_measure, rf=rf, b=None, hist=True)
        
        return w, port, returns
    except Exception as e:
        st.error(f"Erreur dans optimize_relaxed_risk_parity: {str(e)}")
        return None, None, None
