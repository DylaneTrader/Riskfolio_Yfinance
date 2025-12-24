"""
Modèles d'optimisation hiérarchiques (Machine Learning)
"""

import riskfolio as rp
import streamlit as st


def optimize_hrp(returns, risk_measure, rf, linkage='ward', codependence='pearson', **kwargs):
    """
    Optimise le portefeuille avec Hierarchical Risk Parity (HRP)
    
    HRP utilise le clustering hiérarchique pour diviser le portefeuille en groupes
    d'actifs similaires, puis alloue les poids de manière récursive en respectant
    la structure hiérarchique.
    
    Parameters:
    -----------
    returns : pd.DataFrame
        Matrice des rendements historiques
    risk_measure : str
        Mesure de risque à utiliser (ex: 'MV', 'MAD', 'CVaR', etc.)
    rf : float
        Taux sans risque
    linkage : str
        Méthode de linkage pour le clustering ('ward', 'single', 'complete', 'average')
    codependence : str
        Méthode de calcul de codépendance ('pearson', 'spearman', 'kendall')
    
    Returns:
    --------
    tuple : (weights, portfolio_object, returns)
    """
    try:
        port = rp.HCPortfolio(returns=returns)
        port.assets_stats(method_mu='hist', method_cov='hist')
        port.rf = rf
        
        w = port.optimization(
            model='HRP',
            codependence=codependence,
            rm=risk_measure,
            rf=rf,
            linkage=linkage,
            max_k=10,
            leaf_order=True
        )
        
        return w, port, returns
    except Exception as e:
        st.error(f"Erreur dans optimize_hrp: {str(e)}")
        return None, None, None


def optimize_herc(returns, risk_measure, rf, linkage='ward', codependence='pearson', **kwargs):
    """
    Optimise le portefeuille avec Hierarchical Equal Risk Contribution (HERC)
    
    HERC combine le clustering hiérarchique avec le principe d'égale contribution au risque.
    Chaque cluster contribue de manière égale au risque total du portefeuille.
    
    Parameters:
    -----------
    returns : pd.DataFrame
        Matrice des rendements historiques
    risk_measure : str
        Mesure de risque à utiliser (ex: 'MV', 'MAD', 'CVaR', etc.)
    rf : float
        Taux sans risque
    linkage : str
        Méthode de linkage pour le clustering ('ward', 'single', 'complete', 'average')
    codependence : str
        Méthode de calcul de codépendance ('pearson', 'spearman', 'kendall')
    
    Returns:
    --------
    tuple : (weights, portfolio_object, returns)
    """
    try:
        port = rp.HCPortfolio(returns=returns)
        port.assets_stats(method_mu='hist', method_cov='hist')
        port.rf = rf
        
        w = port.optimization(
            model='HERC',
            codependence=codependence,
            rm=risk_measure,
            rf=rf,
            linkage=linkage,
            max_k=10,
            leaf_order=True
        )
        
        return w, port, returns
    except Exception as e:
        st.error(f"Erreur dans optimize_herc: {str(e)}")
        return None, None, None


def optimize_nco(returns, risk_measure, rf, obj='Sharpe', linkage='ward', codependence='pearson', **kwargs):
    """
    Optimise le portefeuille avec Nested Clustered Optimization (NCO)
    
    NCO est un processus en deux étapes :
    1. Clustering hiérarchique des actifs
    2. Optimisation intra-cluster et inter-cluster pour construire le portefeuille optimal
    
    Cette approche réduit l'instabilité des poids tout en permettant une optimisation
    plus sophistiquée que HRP ou HERC.
    
    Parameters:
    -----------
    returns : pd.DataFrame
        Matrice des rendements historiques
    risk_measure : str
        Mesure de risque à utiliser (ex: 'MV', 'MAD', 'CVaR', etc.)
    rf : float
        Taux sans risque
    obj : str
        Objectif d'optimisation ('Sharpe', 'MinRisk', 'MaxRet', 'Utility')
    linkage : str
        Méthode de linkage pour le clustering ('ward', 'single', 'complete', 'average')
    codependence : str
        Méthode de calcul de codépendance ('pearson', 'spearman', 'kendall')
    
    Returns:
    --------
    tuple : (weights, portfolio_object, returns)
    """
    try:
        port = rp.HCPortfolio(returns=returns)
        port.assets_stats(method_mu='hist', method_cov='hist')
        port.rf = rf
        
        w = port.optimization(
            model='NCO',
            codependence=codependence,
            rm=risk_measure,
            obj=obj,
            rf=rf,
            linkage=linkage,
            max_k=10,
            leaf_order=True
        )
        
        return w, port, returns
    except Exception as e:
        st.error(f"Erreur dans optimize_nco: {str(e)}")
        return None, None, None
