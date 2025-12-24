# Structure du Projet - Optimisation de Portefeuille

## 📁 Organisation des Fichiers

```
Riskfolio_Yfinance/
│
├── app.py                      # Application Streamlit principale
├── requirements.txt            # Dépendances Python
├── test_models.py             # Script de test automatisé des modèles
│
├── models/                     # Package des modèles d'optimisation
│   ├── __init__.py            # Exports du package
│   ├── classic_models.py      # Modèles classiques (6 modèles)
│   ├── robust_models.py       # Modèles robustes (4 modèles)
│   └── hierarchical_models.py # Modèles ML hiérarchiques (3 modèles)
│
└── docs/                       # Documentation (14 fichiers)
    ├── README.md
    ├── QUICKSTART.md
    ├── GUIDE_UTILISATION.md
    └── ...
```

## 🎯 Modèles Disponibles (13 Total)

### 1. Modèles Classiques (`models/classic_models.py`)
- **optimize_max_return()** - Portefeuille de Rendement Maximum
- **optimize_min_risk()** - Portefeuille de Risque Minimum
- **optimize_max_sharpe()** - Portefeuille de Sharpe Maximum
- **optimize_max_utility()** - Portefeuille d'Utilité Maximum
- **optimize_risk_parity()** - Portefeuille de Parité de Risque
- **optimize_relaxed_risk_parity()** - Portefeuille de Parité de Risque Relaxée

### 2. Modèles Robustes (`models/robust_models.py`)
- **optimize_robust_max_return()** - Robuste - Rendement Maximum
- **optimize_robust_min_risk()** - Robuste - Risque Minimum
- **optimize_robust_max_sharpe()** - Robuste - Sharpe Maximum
- **optimize_robust_max_utility()** - Robuste - Utilité Maximum

### 3. Modèles Hiérarchiques ML (`models/hierarchical_models.py`)
- **optimize_hrp()** - Hierarchical Risk Parity (HRP)
- **optimize_herc()** - Hierarchical Equal Risk Contribution (HERC)
- **optimize_nco()** - Nested Clustered Optimization (NCO)

## 🚀 Utilisation

### Lancer l'application
```bash
python -m streamlit run app.py
```

### Tester tous les modèles
```bash
python test_models.py
```

### Importer un modèle dans un script
```python
from models import optimize_hrp, optimize_max_sharpe
import pandas as pd

# Charger vos données
returns = pd.read_csv('returns.csv', index_col=0)

# Optimiser avec HRP
weights, port, returns_calc = optimize_hrp(
    returns=returns,
    risk_measure='vol',
    rf=0.025,
    linkage='ward',
    codependence='pearson'
)

# Optimiser avec Sharpe Maximum
weights2, port2, returns_calc2 = optimize_max_sharpe(
    returns=returns,
    risk_measure='MV',
    rf=0.025
)
```

## 📊 Mesures de Risque

### Mesures Classiques (13)
- MV, MAD, MSV, FLPM, SLPM, CVaR, EVaR, WR, MDD, ADD, CDaR, EDaR, UCI

### Mesures HRP/HERC (32)
Organisées en 4 catégories :
- **Dispersions** (8) : vol, MAD, MSV, FLPM, SLPM, VaR, CVaR, TG, EVaR
- **Downside** (10) : VaR, CVaR, TG, EVaR, RLVaR, WR, MDD, ADD, CDaR, UCI
- **Drawdowns Composés** (7) : MDD, ADD, CDaR, EDaR, RLDaR, UCI, DaR
- **Drawdowns Non-Composés** (7) : MDD_Rel, ADD_Rel, CDaR_Rel, etc.

## 🔧 Fonctionnalités Principales

### Interface Streamlit
- ✅ Navigation multi-page (Accueil, Optimisation, À propos)
- ✅ Import de données (Yahoo Finance, CSV, XLSX)
- ✅ Statistiques descriptives affichées AVANT optimisation
- ✅ Matrice de corrélation interactive
- ✅ Dendrogramme pour modèles hiérarchiques
- ✅ Tableau de performance avec gradients de couleur
- ✅ Visualisations interactives (Plotly)
- ✅ Frontière efficiente (modèles classiques uniquement)
- ✅ Export des résultats en CSV

### Graphiques Disponibles
- 📊 Poids du portefeuille (barre et camembert)
- 🔗 Matrice de corrélation (heatmap)
- 🌳 Dendrogramme (modèles hiérarchiques)
- 📉 Frontière efficiente (modèles classiques)

## 📝 Notes Importantes

### Modèles Hiérarchiques
- Utilisent `riskfolio.HCPortfolio` au lieu de `riskfolio.Portfolio`
- Ne supportent pas la frontière efficiente
- Affichent automatiquement le dendrogramme
- Utilisent les 32 mesures de risque HRP/HERC

### Statistiques Pré-Optimisation
Les éléments suivants sont calculés et affichés **AVANT** l'optimisation :
- Statistiques descriptives des actifs
- Matrice de corrélation
- Tableau de performance et indicateurs de risque
- Dendrogramme (pour modèles hiérarchiques)

### Tests Automatisés
Le script `test_models.py` :
- Teste les 13 modèles automatiquement
- Utilise des données réelles de Yahoo Finance
- Affiche un rapport détaillé de succès/échec
- Retourne un code d'erreur si un modèle échoue

## 🛠️ Développement

### Ajouter un nouveau modèle

1. Créer la fonction dans le fichier approprié (`models/`)
```python
def optimize_new_model(returns, risk_measure, rf, **kwargs):
    port = rp.Portfolio(returns=returns)
    port.assets_stats(method_mu='hist', method_cov='hist')
    port.rf = rf
    
    w = port.optimization(...)
    
    return w, port, returns
```

2. Ajouter l'export dans `models/__init__.py`
```python
from .classic_models import optimize_new_model

__all__ = [
    # ... existing exports
    'optimize_new_model'
]
```

3. Mettre à jour `app.py` pour inclure le modèle
```python
from models import optimize_new_model

model_functions = {
    # ... existing models
    "Nouveau Modèle": optimize_new_model
}
```

4. Ajouter un test dans `test_models.py`

## 📚 Documentation Complète

Consultez le dossier `docs/` pour la documentation détaillée :
- QUICKSTART.md - Guide de démarrage rapide
- GUIDE_UTILISATION.md - Guide d'utilisation complet
- GUIDE_SELECTION_MODELE.md - Aide au choix du modèle
- FORMAT_DONNEES.md - Format des données d'entrée
- Et plus encore...

## 🎓 Références

- **Riskfolio-Lib** : https://riskfolio-lib.readthedocs.io/
- **López de Prado (2016)** : Building Diversified Portfolios that Outperform Out-of-Sample
- **Raffinot (2017)** : Hierarchical Clustering-Based Asset Allocation
- **Markowitz (1952)** : Portfolio Selection
