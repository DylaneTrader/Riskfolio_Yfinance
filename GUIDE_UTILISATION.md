# Guide d'Utilisation - Application d'Optimisation de Portefeuille

## Table des Matières
1. [Démarrage Rapide](#démarrage-rapide)
2. [Navigation](#navigation)
3. [Page Optimisation](#page-optimisation)
4. [Interprétation des Résultats](#interprétation-des-résultats)
5. [Conseils et Bonnes Pratiques](#conseils-et-bonnes-pratiques)

## Démarrage Rapide

### Installation
```bash
pip install -r requirements.txt
streamlit run app.py
```

### Premier Portefeuille
1. Allez sur la page "Optimisation"
2. Laissez les symboles par défaut (AAPL, MSFT, etc.)
3. Cliquez sur "🚀 Optimiser le Portefeuille"
4. Explorez les résultats !

## Navigation

L'application comporte trois pages principales :

### 🏠 Accueil
Page d'accueil avec présentation générale et guide de démarrage.

### ⚙️ Optimisation
Page principale pour configurer et optimiser votre portefeuille.

### 📚 À propos
Documentation complète avec formulations mathématiques des modèles.

## Page Optimisation

### 1. Choix de la Source de Données

#### Option A : Yahoo Finance
- **Avantage** : Téléchargement automatique, données à jour
- **Configuration** :
  - Entrez les symboles boursiers séparés par des virgules
  - Choisissez la période (date de début et fin)
  
Exemples de symboles :
- Actions US : AAPL, MSFT, GOOGL, AMZN, TSLA
- Actions françaises : MC.PA, OR.PA, AI.PA, SAN.PA
- ETF : SPY, QQQ, IWM, EFA, EEM

#### Option B : Import de Fichier
- **Formats supportés** : CSV, XLSX, XLS
- **Structure requise** :
  - Index : Dates
  - Colonnes : Symboles des actifs
  - Valeurs : Prix de clôture

### 2. Sélection du Modèle d'Optimisation

#### Modèles de Base

**Portefeuille de Rendement Maximum**
- Maximise le rendement espéré
- Convient aux investisseurs très tolérants au risque
- Peut produire des portefeuilles concentrés

**Portefeuille de Risque Minimum**
- Minimise le risque (selon la mesure choisie)
- Idéal pour les investisseurs conservateurs
- Privilégie la stabilité et la préservation du capital

**Portefeuille de Sharpe Maximum** ⭐ RECOMMANDÉ
- Équilibre optimal rendement/risque
- Convient à la majorité des investisseurs
- Maximise le rendement par unité de risque

**Portefeuille d'Utilité Maximum**
- Personnalisable selon votre aversion au risque (λ)
- λ élevé → plus conservateur
- λ faible → plus agressif

#### Modèles Avancés

**Portefeuille de Parité de Risque**
- Chaque actif contribue également au risque total
- Excellente diversification
- Indépendant des rendements espérés

**Portefeuilles Robustes**
- Protection contre l'incertitude des estimations
- Recommandé si vous doutez de la précision des données
- Paramètre ε contrôle le niveau de robustesse

### 3. Mesures de Risque

Choisissez comment le risque est mesuré :

- **Variance (MV)** : Mesure classique, facile à interpréter
- **CVaR (5%)** : Mesure les pertes extrêmes (queue de distribution)
- **Drawdown Maximum (MDD)** : Plus grande baisse depuis un pic
- **Semi-Variance (MSV)** : Mesure uniquement la volatilité à la baisse

💡 **Recommandation** : Commencez avec MV (Variance), puis explorez CVaR et MDD.

### 4. Paramètres Additionnels

**Taux Sans Risque**
- Rendement d'un placement sans risque (ex: obligations d'État)
- Utilisé pour calculer le ratio de Sharpe
- Valeur typique : 2-4% pour les économies développées

**Aversion au Risque (λ)**
- Pour le modèle d'utilité maximum
- λ = 2 : aversion au risque modérée (valeur par défaut)
- λ > 3 : très conservateur
- λ < 1 : agressif

**Paramètre d'Incertitude (ε)**
- Pour les modèles robustes
- ε = 0 : pas de robustesse (modèle classique)
- ε = 0.5 : robustesse modérée (recommandé)
- ε = 1 : robustesse maximale

## Interprétation des Résultats

### Statistiques Descriptives
Tableau présentant pour chaque actif :
- **Rendement Moyen** : Performance historique annualisée
- **Volatilité** : Risque (écart-type) annualisé
- **Min/Max** : Rendements extrêmes observés
- **Skewness** : Asymétrie de la distribution (>0 : rendements positifs plus fréquents)
- **Kurtosis** : "Épaisseur" des queues de distribution (>3 : plus d'événements extrêmes)

🎨 Les cellules sont colorées : vert = favorable, rouge = défavorable

### Matrice de Corrélation
- Valeurs proches de 1 : actifs très corrélés (bougent ensemble)
- Valeurs proches de -1 : actifs anti-corrélés (diversification forte)
- Valeurs proches de 0 : mouvements indépendants

💡 **Conseil** : Cherchez des actifs peu corrélés pour une meilleure diversification.

### Tableau de Performance
Indicateurs clés pour chaque actif :
- **Rendement Annuel** : Performance moyenne sur un an
- **Volatilité** : Risque mesuré par l'écart-type
- **Ratio de Sharpe** : Rendement ajusté du risque (>1 = bon, >2 = excellent)
- **Drawdown Maximum** : Plus grande perte depuis un pic
- **VaR 95%** : Perte maximale dans 95% des cas
- **CVaR 95%** : Perte moyenne des 5% pires cas

### Métriques du Portefeuille Optimisé

**Rendement Annuel Attendu**
- Rendement espéré du portefeuille sur un an
- Basé sur les performances historiques

**Volatilité Annuelle**
- Risque du portefeuille (écart-type des rendements)
- Plus faible = plus stable

**Ratio de Sharpe**
- Mesure du rendement ajusté du risque
- Interprétation :
  - < 0 : Mauvais (rendement inférieur au taux sans risque)
  - 0-1 : Acceptable
  - 1-2 : Bon
  - 2-3 : Très bon
  - \> 3 : Excellent

### Poids du Portefeuille

**Tableau des Poids**
- Affiche la répartition optimale du capital
- Somme des poids = 100%
- Poids très faibles (<0.1%) peuvent être ignorés en pratique

**Diagramme Circulaire**
- Visualisation rapide de l'allocation
- Utile pour identifier les positions dominantes

**Graphique à Barres**
- Comparaison visuelle des poids
- Facilite l'identification de la concentration

### Frontière Efficiente

Graphique montrant :
- **Ligne bleue** : Ensemble des portefeuilles optimaux
- **Étoile rouge** : Votre portefeuille sélectionné
- **Axe X** : Risque (volatilité)
- **Axe Y** : Rendement attendu

💡 **Lecture** : 
- Points à gauche = moins risqués
- Points en haut = plus rentables
- Portefeuilles sur la frontière = optimaux (pas de meilleure alternative)

## Conseils et Bonnes Pratiques

### 1. Choix du Modèle

**Pour débuter** : Portefeuille de Sharpe Maximum (MV)
- Bon compromis rendement/risque
- Facile à comprendre et interpréter

**Pour investisseurs conservateurs** : Portefeuille de Risque Minimum (MV ou CVaR)
- Minimise les pertes potentielles
- Stabilité maximale

**Pour diversification optimale** : Parité de Risque
- Pas de pari sur les rendements futurs
- Équilibre les contributions au risque

**Pour données incertaines** : Portefeuille Robuste - Sharpe Maximum
- Protection contre les erreurs d'estimation
- Plus stable dans le temps

### 2. Période Historique

**Courte (1 an)** :
- ✅ Plus réactive aux conditions actuelles
- ❌ Plus sensible aux événements ponctuels

**Moyenne (2-3 ans)** : ⭐ RECOMMANDÉ
- ✅ Équilibre entre réactivité et stabilité
- ✅ Capture différents régimes de marché

**Longue (5+ ans)** :
- ✅ Très stable
- ❌ Peut ne pas refléter les conditions actuelles

### 3. Nombre d'Actifs

**5-10 actifs** : ⭐ RECOMMANDÉ
- Diversification suffisante
- Facile à gérer
- Résultats stables

**10-20 actifs** :
- Très bonne diversification
- Peut être complexe à gérer

**20+ actifs** :
- Sur-diversification possible
- Coûts de transaction importants
- Poids individuels très faibles

### 4. Rééquilibrage

- **Fréquence recommandée** : Trimestrielle ou semestrielle
- **Seuil de rééquilibrage** : Si un poids dévie de >5% de sa cible
- **Considérations** : Coûts de transaction, implications fiscales

### 5. Validation

Avant d'implémenter un portefeuille :
1. ✅ Vérifiez que les poids sont réalistes
2. ✅ Comparez les métriques avec un benchmark
3. ✅ Testez plusieurs modèles et mesures de risque
4. ✅ Considérez vos contraintes personnelles (fiscalité, liquidité)
5. ✅ Consultez un conseiller financier si nécessaire

### 6. Limites et Avertissements

⚠️ **Important** :
- Les performances passées ne garantissent pas les performances futures
- Les modèles sont basés sur des hypothèses simplificatrices
- Considérez toujours vos objectifs personnels et votre horizon d'investissement
- Cette application est un outil d'aide à la décision, pas un conseil en investissement

### 7. Optimisations Avancées

Pour aller plus loin :
- Testez différentes mesures de risque pour le même modèle
- Comparez les résultats avec et sans robustesse
- Analysez la sensibilité aux paramètres (λ, ε)
- Exportez les résultats pour suivi et backtesting

## Support et Questions

Pour plus d'informations :
- Consultez la page "À propos" pour les détails mathématiques
- [Documentation Riskfolio-Lib](https://riskfolio-lib.readthedocs.io/)
- [Théorie Moderne du Portefeuille](https://en.wikipedia.org/wiki/Modern_portfolio_theory)

---

**Bon investissement ! 📊💼**
