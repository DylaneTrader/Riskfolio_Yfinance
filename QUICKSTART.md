# 🚀 Guide de Démarrage Rapide

## Installation et Lancement en 3 Minutes

### Étape 1: Vérifier Python (30 secondes)

```bash
# Vérifier la version de Python (3.8+ requis)
python --version
```

Si Python n'est pas installé : [Télécharger Python](https://www.python.org/downloads/)

---

### Étape 2: Installer les Dépendances (1 minute)

```bash
# Se placer dans le dossier du projet
cd c:\Users\Surface\Documents\Riskfolio_Yfinance

# Installer les dépendances
pip install -r requirements.txt
```

**Dépendances principales:**
- streamlit ≥1.28.0
- riskfolio-lib ≥5.0.0
- yfinance ≥0.2.31
- plotly ≥5.17.0
- pandas, numpy, scipy

---

### Étape 3: Lancer l'Application (30 secondes)

```bash
# Lancer Streamlit
python -m streamlit run app.py
```

L'application s'ouvrira automatiquement dans votre navigateur à l'adresse :
- **Local:** http://localhost:8501
- **Réseau:** http://192.168.x.x:8501

---

## 📊 Première Utilisation

### Navigation

L'application comporte **3 pages** accessibles via la barre latérale :

1. **🏠 Accueil** - Vue d'ensemble et statistiques
2. **📈 Optimisation** - Construire et optimiser un portefeuille
3. **📚 À propos** - Documentation mathématique des modèles

---

### Créer Votre Premier Portefeuille (2 minutes)

#### Option 1: Avec Yahoo Finance (Recommandé pour débuter)

1. Aller sur la page **"Optimisation"**
2. Source de données: **"Yahoo Finance"**
3. Entrer des symboles (ex: `AAPL, MSFT, GOOGL, AMZN, META`)
4. Choisir la période (ex: 2 ans)
5. Sélectionner un modèle: **"Portefeuille de Sharpe Maximum"**
6. Mesure de risque: **"MV: Variance"**
7. Cliquer sur **"🚀 Optimiser le Portefeuille"**

**Résultats affichés:**
- ✅ Statistiques descriptives des actifs
- ✅ Matrice de corrélation
- ✅ Tableau de performance
- ✅ Poids optimaux du portefeuille
- ✅ Métriques (rendement, volatilité, Sharpe)
- ✅ Graphiques interactifs
- ✅ Frontière efficiente

#### Option 2: Avec un Fichier CSV/XLSX

1. Préparer un fichier avec:
   - Dates en première colonne (index)
   - Prix de clôture pour chaque actif en colonnes
   - Format : `Date, AAPL, MSFT, GOOGL`

2. Source de données: **"Import de Fichier (CSV/XLSX)"**
3. Télécharger votre fichier
4. Suivre les mêmes étapes que l'option 1

---

## 🎯 Tester les Modèles Hiérarchiques (ML)

### HRP - Hierarchical Risk Parity

**Quand l'utiliser:** Pour une diversification stable basée sur le clustering

```
1. Modèle: "Hierarchical Risk Parity (HRP)"
2. Mesure de risque: "vol: Volatilité" (ou autres mesures HRP/HERC)
3. Paramètres par défaut OK
4. Optimiser
```

**Ce que vous verrez:**
- 🌳 **Dendrogramme** montrant le clustering des actifs
- 💼 Poids du portefeuille basés sur la structure hiérarchique
- 📊 Statistiques de performance

### HERC - Hierarchical Equal Risk Contribution

**Quand l'utiliser:** Pour égaliser la contribution au risque par cluster

```
1. Modèle: "Hierarchical Equal Risk Contribution (HERC)"
2. Mesure de risque: "MDD: Drawdown Maximum" (excellente avec HERC)
3. Optimiser
```

### NCO - Nested Clustered Optimization

**Quand l'utiliser:** Pour une optimisation sophistiquée avec clustering

```
1. Modèle: "Nested Clustered Optimization (NCO)"
2. Mesure de risque: "CVaR: Conditional Value at Risk"
3. Optimiser
```

---

## 🔍 Explorer les 13 Modèles

### Modèles Classiques (6)

| Modèle | Objectif | Quand l'utiliser |
|--------|----------|------------------|
| **Rendement Maximum** | Maximiser le rendement | Forte tolérance au risque |
| **Risque Minimum** | Minimiser la volatilité | Faible tolérance au risque |
| **Sharpe Maximum** | Meilleur ratio risque/rendement | **Recommandé par défaut** |
| **Utilité Maximum** | Équilibre personnalisé | Ajuster λ selon préférence |
| **Parité de Risque** | Égaliser les contributions | Diversification équilibrée |
| **Parité Risque Relaxée** | Parité avec contraintes | Version flexible |

### Modèles Robustes (4)

Ajoutent **"Robuste -"** aux objectifs classiques.

**Quand les utiliser:** Données incertaines ou volatiles

**Paramètre clé:** ε (epsilon) = 0.3 à 0.5 recommandé

### Modèles ML Hiérarchiques (3)

| Modèle | Description | Complexité |
|--------|-------------|------------|
| **HRP** | Clustering + allocation récursive | Faible |
| **HERC** | HRP + égalité de contribution | Moyenne |
| **NCO** | Clustering + optimisation 2 étapes | Élevée |

---

## 📈 Comprendre les Résultats

### Métriques Principales

1. **Rendement Annuel Attendu**
   - Rendement espéré sur 1 an (basé sur historique)
   - Plus élevé = plus de gains potentiels

2. **Volatilité Annuelle**
   - Mesure du risque (écart-type des rendements)
   - Plus faible = moins de fluctuations

3. **Ratio de Sharpe**
   - Rendement par unité de risque
   - **> 1 = bon**, **> 2 = excellent**

### Graphiques

- **Poids du Portefeuille** - Tableau et camembert
- **Composition** - Graphique en barres
- **Matrice de Corrélation** - Dépendances entre actifs
- **Dendrogramme** - Structure hiérarchique (HRP/HERC/NCO)
- **Frontière Efficiente** - Combinaisons risque/rendement optimales

---

## 💡 Conseils Pratiques

### Pour Débuter

1. ✅ Commencer avec **Yahoo Finance** et 5-8 actifs
2. ✅ Utiliser **"Sharpe Maximum"** comme premier modèle
3. ✅ Mesure de risque **"MV"** (variance) est la plus standard
4. ✅ Période de 2 ans minimum recommandée

### Choix du Modèle

**Profil conservateur:**
- Portefeuille de Risque Minimum
- Mesure: MV, MAD ou CVaR

**Profil équilibré:**
- Portefeuille de Sharpe Maximum
- HRP ou HERC
- Mesure: MV ou vol

**Profil agressif:**
- Portefeuille d'Utilité Maximum (λ faible)
- NCO
- Mesure: CVaR ou EVaR

### Données de Qualité

✅ **Bon:**
- Au moins 252 jours de données (1 an de trading)
- 5-20 actifs
- Données complètes (peu de NaN)

❌ **À éviter:**
- Moins de 100 jours
- Plus de 50 actifs (sauf HRP/HERC/NCO)
- Actifs avec historique limité

---

## 🧪 Validation Rapide

### Tester que Tout Fonctionne

```bash
# Test 1: Importer les modèles
python -c "from models import *; print('✅ OK')"

# Test 2: Compiler l'app
python -m py_compile app.py && echo "✅ OK"

# Test 3: Lancer les tests automatiques (optionnel, ~2 minutes)
python test_models.py

# Test 4: Lancer l'application
python -m streamlit run app.py
```

---

## 🆘 Aide Rapide

### Erreur Commune

**"Portfolio object has no attribute hrp_optimization"**
→ ✅ **Déjà corrigé dans cette version !**

**"streamlit: command not found"**
→ Utiliser: `python -m streamlit run app.py`

**"Optimization failed"**
→ Vérifier les données (NaN, période trop courte)

**Plus d'aide:** Consulter [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

---

## 📚 Aller Plus Loin

### Documentation Complète

- **[STRUCTURE.md](STRUCTURE.md)** - Architecture du projet
- **[GUIDE_UTILISATION.md](GUIDE_UTILISATION.md)** - Guide détaillé
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Dépannage
- **[CHANGELOG_V2.md](CHANGELOG_V2.md)** - Nouveautés v2.0

### Page "À propos" de l'App

Contient les formulations mathématiques complètes de chaque modèle avec :
- Fonctions objectives
- Contraintes
- Explications des 32 mesures de risque HRP/HERC
- Références bibliographiques

---

## 🎯 Exemples de Portefeuilles

### Portefeuille Tech (Exemple 1)

```
Actifs: AAPL, MSFT, GOOGL, NVDA, AMD
Période: 2 ans
Modèle: Sharpe Maximum
Mesure: MV
Taux sans risque: 2.5%
```

### Portefeuille Diversifié (Exemple 2)

```
Actifs: SPY, TLT, GLD, VNQ, EEM, VWO, BND, DBC
Période: 3 ans
Modèle: HRP
Mesure: vol
Linkage: ward
```

### Portefeuille Sectoriel (Exemple 3)

```
Actifs: XLF, XLE, XLK, XLV, XLI, XLY, XLP, XLU
Période: 2 ans
Modèle: HERC
Mesure: MDD
```

---

## ✨ Prochaines Étapes

1. ✅ Lancer l'application
2. ✅ Créer votre premier portefeuille avec Yahoo Finance
3. ✅ Essayer les 3 modèles ML (HRP, HERC, NCO)
4. ✅ Comparer plusieurs stratégies
5. ✅ Explorer les 45 mesures de risque
6. ✅ Exporter les résultats en CSV
7. ✅ Consulter la page "À propos" pour approfondir

---

**Temps total: ~5 minutes pour être opérationnel !** 🚀

**Besoin d'aide ?** Consultez [TROUBLESHOOTING.md](TROUBLESHOOTING.md) ou la documentation complète.
