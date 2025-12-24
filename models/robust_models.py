"""
Modèles d'optimisation robustes (Worst Case)
"""

import riskfolio as rp
import streamlit as st


def optimize_robust_max_return(returns, risk_measure, rf, uncertainty=0.5, **kwargs):
    """
    Optimise le portefeuille robuste pour maximiser le rendement (Worst Case)
    
    Parameters:
    -----------
    returns : pd.DataFrame
        Matrice des rendements historiques
    risk_measure : str
        Mesure de risque à utiliser
    rf : float
        Taux sans risque
    uncertainty : float
        Paramètre d'incertitude epsilon
    
    Returns:
    --------
    tuple : (weights, portfolio_object, returns)
    """
    try:
        port = rp.Portfolio(returns=returns)
        port.assets_stats(method_mu='hist', method_cov='hist')
        port.rf = rf
        
        w = port.wc_optimization(
            model='Classic', 
            rm=risk_measure, 
            obj='MaxRet', 
            rf=rf, 
            l=0, 
            Umu='box', 
            Ucov='box', 
            epsilon=uncertainty
        )
        
        return w, port, returns
    except Exception as e:
        st.error(f"Erreur dans optimize_robust_max_return: {str(e)}")
        return None, None, None


def optimize_robust_min_risk(returns, risk_measure, rf, uncertainty=0.5, **kwargs):
    """
    Optimise le portefeuille robuste pour minimiser le risque (Worst Case)
    
    Parameters:
    -----------
    returns : pd.DataFrame
        Matrice des rendements historiques
    risk_measure : str
        Mesure de risque à utiliser
    rf : float
        Taux sans risque
    uncertainty : float
        Paramètre d'incertitude epsilon
    
    Returns:
    --------
    tuple : (weights, portfolio_object, returns)
    """
    try:
        port = rp.Portfolio(returns=returns)
        port.assets_stats(method_mu='hist', method_cov='hist')
        port.rf = rf
        
        w = port.wc_optimization(
            model='Classic', 
            rm=risk_measure, 
            obj='MinRisk', 
            rf=rf, 
            l=0, 
            Umu='box', 
            Ucov='box', 
            epsilon=uncertainty
        )
        
        return w, port, returns
    except Exception as e:
        st.error(f"Erreur dans optimize_robust_min_risk: {str(e)}")
        return None, None, None


def optimize_robust_max_sharpe(returns, risk_measure, rf, uncertainty=0.5, **kwargs):
    """
    Optimise le portefeuille robuste pour maximiser le ratio de Sharpe (Worst Case)
    
    Parameters:
    -----------
    returns : pd.DataFrame
        Matrice des rendements historiques
    risk_measure : str
        Mesure de risque à utiliser
    rf : float
        Taux sans risque
    uncertainty : float
        Paramètre d'incertitude epsilon
    
    Returns:
    --------
    tuple : (weights, portfolio_object, returns)
    """
    try:
        port = rp.Portfolio(returns=returns)
        port.assets_stats(method_mu='hist', method_cov='hist')
        port.rf = rf
        
        w = port.wc_optimization(
            model='Classic', 
            rm=risk_measure, 
            obj='Sharpe', 
            rf=rf, 
            l=0, 
            Umu='box', 
            Ucov='box', 
            epsilon=uncertainty
        )
        
        return w, port, returns
    except Exception as e:
        st.error(f"Erreur dans optimize_robust_max_sharpe: {str(e)}")
        return None, None, None


def optimize_robust_max_utility(returns, risk_measure, rf, risk_aversion=2.0, uncertainty=0.5, **kwargs):
    """
    Optimise le portefeuille robuste pour maximiser l'utilité (Worst Case)
    
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
    uncertainty : float
        Paramètre d'incertitude epsilon
    
    Returns:
    --------
    tuple : (weights, portfolio_object, returns)
    """
    try:
        port = rp.Portfolio(returns=returns)
        port.assets_stats(method_mu='hist', method_cov='hist')
        port.rf = rf
        
        w = port.wc_optimization(
            model='Classic', 
            rm=risk_measure, 
            obj='Utility', 
            rf=rf, 
            l=risk_aversion, 
            Umu='box', 
            Ucov='box', 
            epsilon=uncertainty
        )
        
        return w, port, returns
    except Exception as e:
        st.error(f"Erreur dans optimize_robust_max_utility: {str(e)}")
        return None, None, None
