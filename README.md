# 📊 Optimisation de Portefeuille avec Riskfolio-Lib

Application Streamlit complète pour l'optimisation de portefeuilles financiers avec Riskfolio-Lib, données Yahoo Finance, et visualisations interactives Plotly.

**Version:** 2.0.0 | **Langue:** Français | **Statut:** Production

## ✨ Fonctionnalités Principales

### 🎯 13 Modèles d'Optimisation

#### Modèles Classiques (6)
- **Rendement Maximum** - Maximise le rendement espéré
- **Risque Minimum** - Minimise le risque selon la mesure choisie
- **Sharpe Maximum** - Maximise le ratio risque/rendement
- **Utilité Maximum** - Optimise selon la fonction d'utilité
- **Parité de Risque** - Contribution égale de chaque actif au risque
- **Parité de Risque Relaxée** - Variante flexible de la parité de risque

#### Modèles Robustes (4)
- **Robuste - Rendement Maximum** - Optimisation robuste (Worst Case)
- **Robuste - Risque Minimum** - Minimisation robuste sous incertitude
- **Robuste - Sharpe Maximum** - Sharpe robuste
- **Robuste - Utilité Maximum** - Utilité robuste

#### Modèles ML Hiérarchiques (3)
- **HRP** (Hierarchical Risk Parity) - Clustering hiérarchique avec allocation récursive
- **HERC** (Hierarchical Equal Risk Contribution) - HRP avec contribution égale au risque
- **NCO** (Nested Clustered Optimization) - Optimisation imbriquée en deux étapes

### 📏 45 Mesures de Risque

#### 13 Mesures Classiques
- MV, MAD, MSV, CVaR, EVaR, WR, MDD, ADD, CDaR, EDaR, UCI, et plus

#### 32 Mesures HRP/HERC
- **Dispersions** (8): vol, MAD, MSV, FLPM, SLPM, VaR, CVaR, TG, EVaR
- **Downside** (10): VaR, CVaR, TG, EVaR, RLVaR, WR, MDD, ADD, CDaR, UCI
- **Drawdowns** (14): Composés et non-composés

### 📊 Visualisations Interactives
- **Statistiques pré-optimisation** - Affichées avant le calcul
- **Matrice de corrélation** - Heatmap interactive
- **Dendrogramme** - Clustering hiérarchique (HRP/HERC/NCO)
- **Graphiques de poids** - Barres et camembert
- **Frontière efficiente** - Combinaisons risque/rendement optimales
- **Tableau de performance** - Avec gradients de couleur

### 🗂️ Sources de Données (3)
1. **Yahoo Finance** - Téléchargement automatique
2. **Fichiers CSV** - Import de données personnalisées
3. **Fichiers Excel** - Support XLSX/XLS

---

## 🚀 Installation Rapide

### Prérequis
- Python 3.8+
- pip

### Étapes

```bash
# 1. Cloner le dépôt
git clone https://github.com/DylaneTrader/Riskfolio_Yfinance.git
cd Riskfolio_Yfinance

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Lancer l'application
python -m streamlit run app.py
```

L'application s'ouvre sur http://localhost:8501

**Guide détaillé:** [QUICKSTART.md](QUICKSTART.md)

---

## 📖 Utilisation

### Navigation (3 pages)

1. **🏠 Accueil** - Vue d'ensemble et statistiques
2. **📈 Optimisation** - Configuration et résultats
3. **📚 À propos** - Documentation mathématique

### Exemple Rapide

```python
# Dans l'interface Streamlit:
1. Page "Optimisation"
2. Source: Yahoo Finance
3. Symboles: AAPL, MSFT, GOOGL, AMZN, META
4. Modèle: "Hierarchical Risk Parity (HRP)"
5. Mesure de risque: "vol: Volatilité"
6. Cliquer "Optimiser"

# Résultats affichés:
- Statistiques descriptives
- Matrice de corrélation
- Dendrogramme du clustering
- Poids optimaux
- Métriques de performance
- Graphiques interactifs
```

---

## 🏗️ Architecture

### Structure du Projet

```
Riskfolio_Yfinance/
├── app.py                    # Application Streamlit
├── models/                   # Package de modèles
│   ├── __init__.py          # Exports
│   ├── classic_models.py    # 6 modèles classiques
│   ├── robust_models.py     # 4 modèles robustes
│   └── hierarchical_models.py # 3 modèles ML
├── test_models.py           # Tests automatisés
├── requirements.txt         # Dépendances
└── docs/                    # Documentation
    ├── README.md            # Ce fichier
    ├── QUICKSTART.md        # Guide de démarrage
    ├── STRUCTURE.md         # Architecture détaillée
    ├── TROUBLESHOOTING.md   # Dépannage
    └── CHANGELOG.md         # Historique
```

**Documentation complète:** [STRUCTURE.md](STRUCTURE.md)

---

## 🧪 Tests

### Validation Automatique

```bash
# Tester tous les 13 modèles
python test_models.py
```

### Vérification Rapide

```bash
# Importer les modules
python -c "from models import *; print('✅ OK')"

# Compiler l'application
python -m py_compile app.py
```

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [QUICKSTART.md](QUICKSTART.md) | Installation et première utilisation (5 min) |
| [STRUCTURE.md](STRUCTURE.md) | Architecture technique et modèles |
| [TROUBLESHOOTING.md](TROUBLESHOOTING.md) | Solutions aux erreurs courantes |
| [CHANGELOG.md](CHANGELOG.md) | Historique des versions |

---

## 🎓 Modèles Disponibles

### Choix Rapide par Profil

**Conservateur (faible risque)**
- Portefeuille de Risque Minimum
- Mesure: MV ou CVaR

**Équilibré (risque modéré)**
- Portefeuille de Sharpe Maximum
- HRP ou HERC
- Mesure: MV ou vol

**Agressif (rendement élevé)**
- Portefeuille d'Utilité Maximum (λ faible)
- NCO
- Mesure: CVaR ou EVaR

**Plus de détails:** Consultez la page "À propos" dans l'application

---

## 🔧 Dépendances Principales

```
streamlit >= 1.28.0       # Interface web
riskfolio-lib >= 5.0.0    # Optimisation
yfinance >= 0.2.31        # Données financières
plotly >= 5.17.0          # Visualisations
pandas >= 1.5.0           # Manipulation de données
numpy >= 1.24.0           # Calculs numériques
scipy >= 1.9.0            # Clustering hiérarchique
openpyxl >= 3.1.0         # Support Excel
```

---

## 🐛 Dépannage

### Problèmes Courants

**Erreur: "streamlit: command not found"**
```bash
python -m streamlit run app.py
```

**Erreur d'optimisation**
- Vérifier la qualité des données (min. 252 jours recommandé)
- Essayer une autre mesure de risque
- Réduire le paramètre d'incertitude (ε) pour les modèles robustes

**Guide complet:** [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

---

## 🆕 Nouveautés Version 2.0

### Corrections
- ✅ **HRP/HERC/NCO fonctionnels** - Utilisation correcte de HCPortfolio
- ✅ **Architecture modulaire** - Package models/ séparé

### Nouvelles Fonctionnalités
- ✅ **Dendrogramme** - Visualisation du clustering hiérarchique
- ✅ **Statistiques pré-optimisation** - Analyse avant calcul
- ✅ **32 mesures HRP/HERC** - Sélection automatique
- ✅ **Tests automatisés** - Validation des 13 modèles

**Détails complets:** [CHANGELOG.md](CHANGELOG.md)

---

## 📊 Exemples de Portefeuilles

### Portefeuille Tech
```
Actifs: AAPL, MSFT, GOOGL, NVDA, AMD
Modèle: Sharpe Maximum
Mesure: MV
```

### Portefeuille Diversifié  
```
Actifs: SPY, TLT, GLD, VNQ, EEM, VWO, BND, DBC
Modèle: HRP
Mesure: vol
```

### Portefeuille Sectoriel
```
Actifs: XLF, XLE, XLK, XLV, XLI, XLY, XLP, XLU
Modèle: HERC
Mesure: MDD
```

---

## 🤝 Contributions

Les contributions sont les bienvenues ! Pour ajouter un nouveau modèle :

1. Créer la fonction dans le fichier approprié (`models/`)
2. Ajouter l'export dans `models/__init__.py`
3. Mettre à jour le dictionnaire dans `app.py`
4. Ajouter un test dans `test_models.py`

**Guide:** [STRUCTURE.md](STRUCTURE.md) - Section "Développement"

---

## 📄 Licence

Ce projet utilise les bibliothèques open-source suivantes :
- Riskfolio-Lib (BSD License)
- Streamlit (Apache 2.0)
- Plotly (MIT License)

---

## 🙏 Remerciements

- **Riskfolio-Lib** - Bibliothèque d'optimisation
- **Streamlit** - Framework d'interface
- **Communauté Python** - Outils (pandas, numpy, plotly, scipy)

### Références Académiques
- Markowitz (1952) - Portfolio Selection
- López de Prado (2016) - Building Diversified Portfolios (HRP)
- Raffinot (2017) - Hierarchical Clustering-Based Asset Allocation (HERC)

---

## 📞 Support

**Documentation:** Consultez les guides dans le dossier docs/  
**Problèmes:** [TROUBLESHOOTING.md](TROUBLESHOOTING.md)  
**GitHub:** [Issues](https://github.com/DylaneTrader/Riskfolio_Yfinance/issues)

---

**Version:** 2.0.0 | **Date:** Décembre 2025 | **Statut:** ✅ Production Ready
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`.

## How to Use

1. **Configure Portfolio Settings** (Sidebar):
   - Enter stock tickers (comma-separated, e.g., AAPL,MSFT,GOOGL)
   - Select date range for historical data
   - Choose optimization model
   - Select risk measure
   - Set risk-free rate and other parameters

2. **Optimize Portfolio**:
   - Click the "Optimize Portfolio" button
   - Wait for data download and optimization to complete

3. **View Results**:
   - Portfolio performance metrics (expected return, volatility, Sharpe ratio)
   - Portfolio weights table
   - Visual representations (pie chart, bar chart)
   - Efficient frontier plot
   - Download optimized weights as CSV

## Requirements

- Python 3.8+
- streamlit >= 1.28.0
- riskfolio-lib >= 5.0.0
- yfinance >= 0.2.31
- plotly >= 5.17.0
- pandas >= 2.0.0
- numpy >= 1.24.0
- scipy >= 1.11.0

## Technologies

- **Streamlit**: Web application framework
- **Riskfolio-Lib**: Portfolio optimization library
- **yfinance**: Yahoo Finance data API
- **Plotly**: Interactive visualization library
- **Pandas/NumPy**: Data manipulation and numerical computing

## Example Portfolio

Default tickers include major US stocks:
- AAPL (Apple)
- MSFT (Microsoft)
- GOOGL (Google)
- AMZN (Amazon)
- TSLA (Tesla)
- JPM (JPMorgan Chase)
- JNJ (Johnson & Johnson)
- V (Visa)
- PG (Procter & Gamble)
- NVDA (NVIDIA)

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Disclaimer

This application is for educational and research purposes only. It should not be considered as financial advice. Always consult with a qualified financial advisor before making investment decisions.