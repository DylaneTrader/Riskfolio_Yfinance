# 🚀 Démarrage Rapide

## Installation (1 minute)

```bash
# 1. Installer les dépendances
pip install -r requirements.txt

# 2. Lancer l'application
streamlit run app.py
```

L'application s'ouvrira automatiquement dans votre navigateur à l'adresse : `http://localhost:8501`

## Premier Portefeuille (3 minutes)

### Étape 1 : Navigation
Dans la barre latérale, vous êtes sur la page **"Accueil"** par défaut.
Cliquez sur **"Optimisation"**.

### Étape 2 : Configuration de Base
Laissez les paramètres par défaut :
- Source : Yahoo Finance
- Symboles : AAPL,MSFT,GOOGL,AMZN,TSLA,JPM,JNJ,V,PG,NVDA
- Dates : 2 dernières années
- Modèle : **Portefeuille de Sharpe Maximum** ⭐
- Mesure de risque : **MV: Variance (Écart-type)**

### Étape 3 : Optimiser
Cliquez sur le bouton **"🚀 Optimiser le Portefeuille"**

### Étape 4 : Explorer les Résultats
Vous verrez :
1. **Statistiques descriptives** - Performance de chaque actif
2. **Matrice de corrélation** - Relations entre actifs
3. **Tableau de performance** - Indicateurs de risque
4. **Métriques du portefeuille** - Rendement, Volatilité, Sharpe
5. **Poids optimaux** - Répartition recommandée
6. **Visualisations** - Graphiques interactifs
7. **Frontière efficiente** - Votre portefeuille sur la courbe optimale

## Scénarios d'Utilisation

### 🛡️ Investisseur Conservateur
```
Modèle : Portefeuille de Risque Minimum
Mesure de risque : CVaR: Valeur à Risque Conditionnelle
Taux sans risque : 3%
```

### 🚀 Investisseur Agressif
```
Modèle : Portefeuille de Rendement Maximum
Mesure de risque : MV: Variance
Taux sans risque : 2%
```

### ⚖️ Investisseur Équilibré (Recommandé)
```
Modèle : Portefeuille de Sharpe Maximum
Mesure de risque : MV: Variance
Taux sans risque : 2.5%
```

### 🎯 Diversification Optimale
```
Modèle : Portefeuille de Parité de Risque
Mesure de risque : MV: Variance
```

### 🛡️ Protection contre l'Incertitude
```
Modèle : Portefeuille Robuste - Sharpe Maximum
Mesure de risque : CVaR
Paramètre d'incertitude : 0.5
```

## Import de Vos Données

### Option 1 : Yahoo Finance
1. Entrez vos symboles séparés par des virgules
2. Exemples :
   - Actions US : `AAPL,MSFT,TSLA,NVDA`
   - Actions FR : `MC.PA,OR.PA,AI.PA,SAN.PA`
   - ETF : `SPY,QQQ,IWM,EFA`
   - Mix : `AAPL,MSFT,SPY,GLD,TLT`

### Option 2 : Fichier CSV/Excel
1. Sélectionnez "Importer un fichier"
2. Préparez votre fichier selon le format :
   ```
   Date,Actif1,Actif2,Actif3
   2023-01-01,100.5,200.3,150.7
   2023-01-02,101.2,199.8,151.2
   ...
   ```
3. Utilisez `exemple_donnees.csv` comme modèle
4. Cliquez sur "Browse files" et sélectionnez votre fichier

## Comprendre les Résultats

### Métriques Principales

**Rendement Annuel Attendu : 15.5%**
→ Votre portefeuille devrait rapporter ~15.5% par an (basé sur l'historique)

**Volatilité Annuelle : 20.3%**
→ Fluctuation typique des rendements (risque)

**Ratio de Sharpe : 1.85**
→ Rendement par unité de risque
- < 1 : Acceptable
- 1-2 : Bon ✅
- 2-3 : Très bon 🌟
- \> 3 : Excellent 💎

### Poids du Portefeuille

```
AAPL : 25.3%  → Investissez 25.3% de votre capital dans Apple
MSFT : 22.1%  → 22.1% dans Microsoft
GOOGL : 18.7% → etc.
...
```

**Total = 100%**

### Frontière Efficiente

- **Ligne bleue** : Tous les portefeuilles optimaux possibles
- **Étoile rouge** : Votre portefeuille sélectionné
- Plus à gauche = moins risqué
- Plus en haut = plus rentable

## Conseils Rapides

### ✅ Bonnes Pratiques
- Utilisez au moins 5-10 actifs différents
- Minimum 1 an de données historiques (2-3 ans recommandé)
- Commencez avec le modèle "Sharpe Maximum"
- Testez plusieurs modèles et comparez
- Exportez les résultats (bouton "Télécharger")

### ⚠️ À Éviter
- Moins de 2 actifs (pas de diversification)
- Moins de 6 mois de données (pas assez représentatif)
- Ignorer la corrélation entre actifs
- Utiliser un seul modèle sans comparaison

### 🎓 Pour Aller Plus Loin
1. Lisez la page **"À propos"** pour comprendre les mathématiques
2. Consultez le **"GUIDE_UTILISATION.md"** pour les détails
3. Expérimentez avec différentes mesures de risque
4. Comparez plusieurs périodes historiques

## Aide

### Problèmes Courants

**"Échec du téléchargement des données"**
→ Vérifiez les symboles boursiers (doivent être valides sur Yahoo Finance)

**"L'optimisation a échoué"**
→ Essayez avec plus d'actifs ou une période différente

**"Données manquantes"**
→ Normal, l'application remplit automatiquement les trous

### Support
- 📖 `GUIDE_UTILISATION.md` - Guide complet
- 📊 `FORMAT_DONNEES.md` - Format des fichiers
- 📚 Page "À propos" - Documentation mathématique

## Prochaines Étapes

1. ✅ Créez votre premier portefeuille (3 min)
2. 📊 Comparez plusieurs modèles (10 min)
3. 📁 Importez vos propres données (15 min)
4. 📚 Lisez les explications mathématiques (30 min)
5. 🎯 Optimisez votre stratégie d'investissement !

---

**Bon investissement ! 📈💼**

*Cette application est un outil d'aide à la décision. Consultez toujours un conseiller financier professionnel avant de prendre des décisions d'investissement.*
