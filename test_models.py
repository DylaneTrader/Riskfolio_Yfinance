"""
Script de test pour valider tous les modèles d'optimisation
"""

import sys
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta

# Import des modèles
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

def test_model(model_name, optimize_func, returns, **kwargs):
    """Test un modèle d'optimisation"""
    print(f"\n{'='*60}")
    print(f"Test: {model_name}")
    print('='*60)
    
    try:
        w, port, returns_calc = optimize_func(returns=returns, **kwargs)
        
        if w is not None and w.sum().sum() > 0:
            print(f"✅ {model_name} - SUCCESS")
            print(f"   Nombre d'actifs avec poids > 0: {(w > 0.001).sum().sum()}")
            print(f"   Somme des poids: {w.sum().sum():.4f}")
            print(f"   Poids max: {w.max().max():.4f}")
            print(f"   Poids min (>0): {w[w > 0].min().min():.4f}")
            return True
        else:
            print(f"❌ {model_name} - FAILED: Pas de poids calculés")
            return False
            
    except Exception as e:
        print(f"❌ {model_name} - ERROR: {str(e)}")
        return False

def main():
    """Fonction principale de test"""
    print("\n" + "="*60)
    print("TEST DE TOUS LES MODÈLES D'OPTIMISATION")
    print("="*60)
    
    # Télécharger des données de test
    print("\nTéléchargement des données de test...")
    tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'TSLA', 'NVDA', 'JPM']
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365*2)
    
    try:
        data = yf.download(tickers, start=start_date, end=end_date, progress=False)
        prices = data['Close']
        prices = prices.dropna(how='all').ffill().bfill()
        returns = prices.pct_change().dropna()
        print(f"✅ Données téléchargées: {len(prices)} jours, {len(prices.columns)} actifs")
    except Exception as e:
        print(f"❌ Erreur lors du téléchargement: {str(e)}")
        return
    
    # Paramètres communs
    rf = 0.025
    risk_aversion = 2.0
    uncertainty = 0.5
    
    # Compteur de succès
    results = {}
    
    # === MODÈLES CLASSIQUES ===
    print("\n" + "="*60)
    print("MODÈLES CLASSIQUES")
    print("="*60)
    
    tests = [
        ("Portefeuille de Rendement Maximum", optimize_max_return, {'risk_measure': 'MV', 'rf': rf}),
        ("Portefeuille de Risque Minimum", optimize_min_risk, {'risk_measure': 'MV', 'rf': rf}),
        ("Portefeuille de Sharpe Maximum", optimize_max_sharpe, {'risk_measure': 'MV', 'rf': rf}),
        ("Portefeuille d'Utilité Maximum", optimize_max_utility, {'risk_measure': 'MV', 'rf': rf, 'risk_aversion': risk_aversion}),
        ("Portefeuille de Parité de Risque", optimize_risk_parity, {'risk_measure': 'MV', 'rf': rf}),
        ("Portefeuille de Parité de Risque Relaxée", optimize_relaxed_risk_parity, {'risk_measure': 'MV', 'rf': rf}),
    ]
    
    for name, func, params in tests:
        results[name] = test_model(name, func, returns, **params)
    
    # === MODÈLES ROBUSTES ===
    print("\n" + "="*60)
    print("MODÈLES ROBUSTES (WORST CASE)")
    print("="*60)
    
    robust_tests = [
        ("Portefeuille Robuste - Rendement Maximum", optimize_robust_max_return, 
         {'risk_measure': 'MV', 'rf': rf, 'uncertainty': uncertainty}),
        ("Portefeuille Robuste - Risque Minimum", optimize_robust_min_risk, 
         {'risk_measure': 'MV', 'rf': rf, 'uncertainty': uncertainty}),
        ("Portefeuille Robuste - Sharpe Maximum", optimize_robust_max_sharpe, 
         {'risk_measure': 'MV', 'rf': rf, 'uncertainty': uncertainty}),
        ("Portefeuille Robuste - Utilité Maximum", optimize_robust_max_utility, 
         {'risk_measure': 'MV', 'rf': rf, 'risk_aversion': risk_aversion, 'uncertainty': uncertainty}),
    ]
    
    for name, func, params in robust_tests:
        results[name] = test_model(name, func, returns, **params)
    
    # === MODÈLES HIÉRARCHIQUES (MACHINE LEARNING) ===
    print("\n" + "="*60)
    print("MODÈLES HIÉRARCHIQUES (MACHINE LEARNING)")
    print("="*60)
    
    hierarchical_tests = [
        ("Hierarchical Risk Parity (HRP)", optimize_hrp, 
         {'risk_measure': 'vol', 'rf': rf, 'linkage': 'ward', 'codependence': 'pearson'}),
        ("Hierarchical Equal Risk Contribution (HERC)", optimize_herc, 
         {'risk_measure': 'vol', 'rf': rf, 'linkage': 'ward', 'codependence': 'pearson'}),
        ("Nested Clustered Optimization (NCO)", optimize_nco, 
         {'risk_measure': 'vol', 'rf': rf, 'obj': 'Sharpe', 'linkage': 'ward', 'codependence': 'pearson'}),
    ]
    
    for name, func, params in hierarchical_tests:
        results[name] = test_model(name, func, returns, **params)
    
    # === RÉSUMÉ ===
    print("\n" + "="*60)
    print("RÉSUMÉ DES TESTS")
    print("="*60)
    
    total = len(results)
    success = sum(results.values())
    failed = total - success
    
    print(f"\nTotal de modèles testés: {total}")
    print(f"✅ Succès: {success}")
    print(f"❌ Échecs: {failed}")
    print(f"Taux de réussite: {success/total*100:.1f}%")
    
    print("\nDétails:")
    for name, result in results.items():
        status = "✅ OK" if result else "❌ FAILED"
        print(f"  {status} - {name}")
    
    if failed > 0:
        print("\n⚠️ Certains modèles ont échoué. Vérifiez les messages d'erreur ci-dessus.")
        sys.exit(1)
    else:
        print("\n🎉 Tous les modèles fonctionnent correctement!")
        sys.exit(0)

if __name__ == "__main__":
    main()
