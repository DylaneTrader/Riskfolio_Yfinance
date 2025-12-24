# Application d'Optimisation de Portefeuille

Application Streamlit pour l'optimisation de portefeuille financier utilisant Riskfolio-Lib, avec support multi-sources de données et explications mathématiques complètes.

## 🎯 Fonctionnalités

- **Navigation Multi-Pages** : Accueil, Optimisation, À propos
- **Sources de Données Multiples** :
  - Yahoo Finance (téléchargement automatique)
  - Import CSV
  - Import Excel (XLSX/XLS)
  
- **10 Modèles d'Optimisation** :
  - Portefeuille de Rendement Maximum
  - Portefeuille de Risque Minimum
  - Portefeuille de Sharpe Maximum
  - Portefeuille d'Utilité Maximum
  - Portefeuille de Parité de Risque
  - Portefeuille de Parité de Risque Relaxée
  - 4 variantes de Portefeuilles Robustes (Worst Case Mean-Variance)

- **13 Mesures de Risque** :
  - Variance (MV)
  - Écart Absolu Moyen (MAD)
  - Semi-Variance (MSV)
  - CVaR, EVaR, CDaR, EDaR
  - Drawdown Maximum (MDD), Drawdown Moyen (ADD)
  - Et plus encore...

- **Analyses Avancées** :
  - Statistiques descriptives des actifs
  - Tableaux de performance avec gradients de couleur
  - Matrice de corrélation interactive
  - Frontière efficiente
  - Visualisations interactives (Plotly)

- **Documentation Complète** :
  - Explications mathématiques détaillées
  - Formulations des modèles
  - Références académiques

## 📦 Installation

```bash
pip install -r requirements.txt
```

## 🚀 Utilisation

```bash
streamlit run app.py
```

L'application sera accessible à l'adresse : http://localhost:8501

## 📊 Structure de l'Application

### Page Accueil
- Présentation générale
- Vue d'ensemble des fonctionnalités
- Guide de démarrage rapide

### Page Optimisation
- Configuration du portefeuille
- Choix de la source de données
- Sélection du modèle d'optimisation
- Paramètres de risque explicites
- Résultats détaillés avec visualisations

### Page À propos
- Explications mathématiques complètes
- Formulations des modèles
- Théorie moderne du portefeuille
- Références et liens utiles

## 📈 Format des Fichiers d'Import

### CSV/Excel
Les fichiers doivent avoir le format suivant :
- **Index** : Dates (format datetime)
- **Colonnes** : Symboles des actifs
- **Valeurs** : Prix de clôture

Exemple :
```
Date,AAPL,MSFT,GOOGL
2023-01-01,150.5,245.2,95.3
2023-01-02,152.1,247.8,96.1
...
```

## 🛠️ Technologies Utilisées

- **Streamlit** : Interface web interactive
- **Riskfolio-Lib** : Optimisation de portefeuille
- **yfinance** : Téléchargement de données financières
- **Plotly** : Visualisations interactives
- **Pandas/Numpy** : Manipulation de données
- **openpyxl** : Lecture de fichiers Excel

## 📚 Références

- Markowitz, H. (1952). "Portfolio Selection". The Journal of Finance.
- [Documentation Riskfolio-Lib](https://riskfolio-lib.readthedocs.io/)
- [Code source Riskfolio-Lib](https://github.com/dcajasn/Riskfolio-Lib)

## 📝 Licence

Projet à des fins éducatives et de recherche.
