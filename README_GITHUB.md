# 📊 Application d'Optimisation de Portefeuille

> Application web interactive pour l'optimisation de portefeuille financier utilisant Riskfolio-Lib, avec interface en français, support multi-sources et documentation mathématique complète.

[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Educational-green.svg)]()

---

## 🎯 Fonctionnalités

### 📱 Interface Multi-Pages
- **Accueil** : Présentation et guide de démarrage
- **Optimisation** : Configuration et analyse complète
- **À propos** : Documentation mathématique détaillée

### 📊 Sources de Données
- ✅ **Yahoo Finance** : Téléchargement automatique
- ✅ **CSV** : Import de fichiers personnalisés
- ✅ **Excel** : Support XLSX/XLS

### 🧮 Modèles d'Optimisation (10)
1. Portefeuille de Rendement Maximum
2. Portefeuille de Risque Minimum
3. **Portefeuille de Sharpe Maximum** ⭐ (Recommandé)
4. Portefeuille d'Utilité Maximum
5. Portefeuille de Parité de Risque
6. Portefeuille de Parité de Risque Relaxée
7-10. Portefeuilles Robustes (4 variantes)

### 📉 Mesures de Risque (13)
- **MV** : Variance (Écart-type)
- **CVaR** : Valeur à Risque Conditionnelle
- **MDD** : Drawdown Maximum
- **CDaR** : Drawdown Conditionnel à Risque
- Et 9 autres mesures...

### 📈 Analyses Avancées
- ✅ Statistiques descriptives avec gradients de couleurs
- ✅ Matrice de corrélation interactive
- ✅ Tableau de performance (Rendement, Volatilité, Sharpe, Drawdown, VaR, CVaR)
- ✅ Frontière efficiente
- ✅ Visualisations Plotly interactives

---

## 🚀 Installation & Démarrage

### Installation Rapide
```bash
# Cloner le dépôt
git clone https://github.com/votre-username/Riskfolio_Yfinance.git
cd Riskfolio_Yfinance

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application
streamlit run app.py
```

L'application s'ouvrira automatiquement dans votre navigateur à `http://localhost:8501`

### Prérequis
- Python 3.8+
- pip

---

## 📸 Captures d'Écran

### Page Accueil
![Page Accueil](https://via.placeholder.com/800x400?text=Page+Accueil)

### Page Optimisation
![Page Optimisation](https://via.placeholder.com/800x400?text=Page+Optimisation)

### Résultats
![Résultats](https://via.placeholder.com/800x400?text=R%C3%A9sultats+d%27Optimisation)

---

## 📚 Documentation

### Guides Utilisateur
- 📖 [**QUICKSTART.md**](QUICKSTART.md) - Démarrage en 5 minutes
- 📖 [**GUIDE_UTILISATION.md**](GUIDE_UTILISATION.md) - Guide complet (30 min)
- 📖 [**GUIDE_SELECTION_MODELE.md**](GUIDE_SELECTION_MODELE.md) - Quel modèle choisir ?
- 📖 [**FORMAT_DONNEES.md**](FORMAT_DONNEES.md) - Format des fichiers CSV/XLSX

### Documentation Technique
- 🔧 [**README_FR.md**](README_FR.md) - Documentation technique détaillée
- 🔧 [**CHANGELOG.md**](CHANGELOG.md) - Historique des modifications
- 🔧 [**RÉCAPITULATIF.md**](RÉCAPITULATIF.md) - Résumé des fonctionnalités

### Navigation
- 🗺️ [**INDEX.md**](INDEX.md) - Index de tous les fichiers
- 🗺️ [**STRUCTURE_NAVIGATION.md**](STRUCTURE_NAVIGATION.md) - Structure de l'app
- 🗺️ [**MANIFESTE.md**](MANIFESTE.md) - Manifeste complet du projet

---

## 💡 Utilisation Rapide

### 1. Premier Portefeuille (3 minutes)
```
1. Lancez l'application : streamlit run app.py
2. Cliquez sur "Optimisation" dans la sidebar
3. Laissez les paramètres par défaut
4. Cliquez sur "🚀 Optimiser le Portefeuille"
5. Explorez les résultats !
```

### 2. Import de Vos Données
```
1. Préparez un fichier CSV/XLSX (voir FORMAT_DONNEES.md)
2. Ou utilisez exemple_donnees.csv fourni
3. Page Optimisation → "Importer un fichier"
4. Sélectionnez votre fichier
5. Configurez et optimisez !
```

### 3. Choix du Modèle
```
Pour 80% des utilisateurs, utilisez :
- Modèle : Portefeuille de Sharpe Maximum
- Mesure : MV (Variance)
- Période : 2-3 ans de données

Voir GUIDE_SELECTION_MODELE.md pour plus de détails
```

---

## 🛠️ Technologies

| Catégorie | Technologie | Version |
|-----------|-------------|---------|
| **Interface** | Streamlit | ≥ 1.28.0 |
| **Optimisation** | Riskfolio-Lib | ≥ 5.0.0 |
| **Données** | yfinance | ≥ 0.2.31 |
| **Visualisation** | Plotly | ≥ 5.17.0 |
| **Data Science** | Pandas | ≥ 2.0.0 |
| **Data Science** | NumPy | ≥ 1.24.0 |
| **Calcul** | SciPy | ≥ 1.11.0 |
| **Excel** | openpyxl | ≥ 3.1.0 |

---

## 📊 Structure du Projet

```
Riskfolio_Yfinance/
│
├── 📱 Application
│   ├── app.py                    # Application principale (999 lignes)
│   └── requirements.txt          # Dépendances
│
├── 📚 Documentation Utilisateur
│   ├── QUICKSTART.md             # Démarrage rapide
│   ├── GUIDE_UTILISATION.md      # Guide complet
│   ├── GUIDE_SELECTION_MODELE.md # Choix du modèle
│   └── FORMAT_DONNEES.md         # Format des fichiers
│
├── 📖 Documentation Technique
│   ├── README_FR.md              # README français
│   ├── CHANGELOG.md              # Historique
│   └── RÉCAPITULATIF.md          # Résumé détaillé
│
├── 🗺️ Navigation
│   ├── INDEX.md                  # Index des fichiers
│   ├── STRUCTURE_NAVIGATION.md   # Structure visuelle
│   └── MANIFESTE.md              # Manifeste du projet
│
└── 📊 Données
    └── exemple_donnees.csv       # Fichier exemple
```

---

## 🎓 Exemples d'Utilisation

### Investisseur Conservateur
```python
Modèle : Portefeuille de Risque Minimum
Mesure : CVaR (Valeur à Risque Conditionnelle)
Taux sans risque : 3%
```

### Investisseur Équilibré (Recommandé)
```python
Modèle : Portefeuille de Sharpe Maximum
Mesure : MV (Variance)
Taux sans risque : 2.5%
```

### Investisseur Dynamique
```python
Modèle : Portefeuille d'Utilité Maximum
Mesure : MV (Variance)
Aversion au risque (λ) : 1.0
```

---

## 🔬 Modèles Mathématiques

Tous les modèles sont expliqués mathématiquement dans la page **"À propos"** de l'application :

### Portefeuille de Sharpe Maximum
```math
max_{w} \frac{\mu^T w - r_f}{\sqrt{w^T \Sigma w}}
s.t. w^T \mathbf{1} = 1, w \geq 0
```

### Portefeuille de Parité de Risque
```math
RC_i = RC_j \quad \forall i,j
RC_i = w_i \frac{\partial \phi(w)}{\partial w_i}
```

Consultez la page "À propos" pour toutes les formulations mathématiques.

---

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
- Signaler des bugs
- Proposer des fonctionnalités
- Améliorer la documentation
- Soumettre des pull requests

---

## 📝 Licence

Projet à des fins éducatives et de recherche.

---

## 📚 Références Académiques

- **Markowitz, H.** (1952). "Portfolio Selection". *The Journal of Finance*.
- **Rockafellar, R. T., & Uryasev, S.** (2000). "Optimization of conditional value-at-risk."
- **Maillard, S., Roncalli, T., & Teïletche, J.** (2010). "The properties of equally weighted risk contribution portfolios."
- **Ben-Tal, A., & Nemirovski, A.** (1998). "Robust convex optimization."

---

## 🔗 Liens Utiles

- [Documentation Riskfolio-Lib](https://riskfolio-lib.readthedocs.io/)
- [Code Source Riskfolio-Lib](https://github.com/dcajasn/Riskfolio-Lib)
- [Documentation Streamlit](https://docs.streamlit.io/)
- [Documentation Plotly](https://plotly.com/python/)

---

## 👥 Profils d'Investisseurs

| Profil | Modèle Recommandé | Mesure de Risque |
|--------|-------------------|------------------|
| 🛡️ Très Conservateur | Risque Minimum | CVaR |
| 🏦 Conservateur | Risque Minimum | MV |
| ⚖️ Équilibré | Sharpe Maximum ⭐ | MV |
| 🚀 Dynamique | Utilité Maximum | MV |
| 🎯 Diversification | Parité de Risque | MV |
| 🔬 Analytique | Robuste - Sharpe | CVaR |

---

## 📞 Support

- 📖 Consultez la [documentation complète](INDEX.md)
- 🐛 Signalez les bugs via les Issues GitHub
- 💬 Questions ? Ouvrez une Discussion

---

## ⭐ Remerciements

Cette application utilise la bibliothèque **Riskfolio-Lib** développée par Dany Cajas.
Merci à toute la communauté open-source !

---

## 📈 Statistiques du Projet

- **18 fichiers** au total
- **~158 KB** de code et documentation
- **999 lignes** de code Python
- **10 fichiers** de documentation Markdown
- **100%** en français

---

**🎉 Application prête à l'emploi ! Bon investissement ! 📊💼**

*Pour démarrer rapidement, consultez [QUICKSTART.md](QUICKSTART.md)*
