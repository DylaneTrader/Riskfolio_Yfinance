# Guide de Dépannage - Optimisation de Portefeuille

## 🐛 Erreurs Courantes et Solutions

### 1. Erreur: `'Portfolio' object has no attribute 'hrp_optimization'`

**Cause:** Les modèles hiérarchiques (HRP, HERC, NCO) nécessitent `HCPortfolio`, pas `Portfolio`.

**Solution:** Cette erreur a été corrigée. Les modèles hiérarchiques utilisent maintenant correctement `rp.HCPortfolio`.

```python
# ❌ Incorrect
port = rp.Portfolio(returns=returns)
w = port.hrp_optimization(...)

# ✅ Correct
port = rp.HCPortfolio(returns=returns)
w = port.optimization(model='HRP', ...)
```

---

### 2. Erreur: Import des modèles échoue

**Cause:** Le dossier `models/` n'est pas dans le PYTHONPATH ou `__init__.py` est manquant.

**Solution:**
```bash
# Vérifier que vous êtes dans le bon dossier
cd c:\Users\Surface\Documents\Riskfolio_Yfinance

# Vérifier que models/ existe
ls models/

# Tester l'import
python -c "from models import optimize_hrp; print('OK')"
```

---

### 3. L'optimisation retourne des poids nuls

**Causes possibles:**
- Contraintes trop restrictives
- Mesure de risque incompatible avec le modèle
- Données insuffisantes ou de mauvaise qualité

**Solutions:**
1. Vérifier les données :
```python
returns = prices.pct_change().dropna()
print(f"Shape: {returns.shape}")
print(f"NaN: {returns.isna().sum().sum()}")
print(f"Periode: {returns.index[0]} to {returns.index[-1]}")
```

2. Essayer une mesure de risque différente
3. Augmenter la période de données (min. 252 jours recommandé)

---

### 4. Erreur: "Optimization failed" pour modèles robustes

**Cause:** Le paramètre d'incertitude `epsilon` est trop élevé.

**Solution:**
- Réduire `epsilon` entre 0.1 et 0.5
- Valeur recommandée : 0.3 à 0.4

```python
# Trop élevé
uncertainty = 0.9  # ❌

# Recommandé
uncertainty = 0.4  # ✅
```

---

### 5. Le dendrogramme ne s'affiche pas

**Cause:** Module `scipy` manquant ou version incompatible.

**Solution:**
```bash
pip install scipy>=1.9.0
```

---

### 6. Erreur de mémoire avec frontière efficiente

**Cause:** Trop de points calculés pour la frontière efficiente.

**Solution:** La frontière efficiente est maintenant désactivée pour les modèles hiérarchiques (HRP, HERC, NCO) car elle n'est pas applicable.

Pour les modèles classiques, réduire le nombre de points :
```python
# Dans app.py, fonction plot_efficient_frontier()
points = 30  # au lieu de 50
```

---

### 7. Streamlit ne démarre pas

**Erreur:** `streamlit: command not found`

**Solution:**
```bash
# Utiliser le module Python
python -m streamlit run app.py

# Ou installer streamlit globalement
pip install streamlit
```

---

### 8. Les statistiques ne s'affichent pas avant l'optimisation

**Cause:** Ancienne version du code.

**Solution:** Cette fonctionnalité est maintenant implémentée. Les statistiques descriptives, la matrice de corrélation, et le tableau de performance s'affichent automatiquement après le chargement des données et AVANT l'optimisation.

---

### 9. Erreur: "calculate_portfolio() takes 2 positional arguments but 3 were given"

**Cause:** Ancienne signature de la fonction.

**Solution:** La fonction retourne maintenant 3 valeurs :
```python
# ✅ Correct
weights, port, returns_calc = calculate_portfolio(...)

# ❌ Incorrect (ancienne version)
weights, port = calculate_portfolio(...)
```

---

### 10. Les mesures de risque HRP/HERC ne sont pas disponibles

**Cause:** Ancien dictionnaire de mesures.

**Solution:** Le dictionnaire `HRP_HERC_RISK_MEASURES` avec 32 mesures est maintenant disponible. L'interface sélectionne automatiquement les bonnes mesures selon le modèle.

---

## 🔍 Diagnostic Rapide

### Vérifier que tout fonctionne

```bash
# 1. Tester l'import des modules
python -c "from models import *; print('✅ Modules OK')"

# 2. Tester la compilation
python -m py_compile app.py
echo "✅ Syntaxe OK"

# 3. Tester tous les modèles
python test_models.py

# 4. Lancer l'application
python -m streamlit run app.py
```

---

## 📊 Vérifier les Données

### Script de diagnostic des données

```python
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta

# Télécharger des données de test
tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META']
end_date = datetime.now()
start_date = end_date - timedelta(days=365*2)

data = yf.download(tickers, start=start_date, end=end_date)
prices = data['Close']

# Diagnostic
print(f"Shape: {prices.shape}")
print(f"Période: {prices.index[0]} à {prices.index[-1]}")
print(f"Jours: {len(prices)}")
print(f"NaN par colonne:\n{prices.isna().sum()}")
print(f"\nStatistiques:\n{prices.describe()}")

# Vérifier les rendements
returns = prices.pct_change().dropna()
print(f"\nRendements shape: {returns.shape}")
print(f"Rendements NaN: {returns.isna().sum().sum()}")
print(f"Rendements mean:\n{returns.mean()}")
print(f"Rendements std:\n{returns.std()}")
```

---

## 🎯 Tests Spécifiques par Modèle

### Test HRP
```python
from models import optimize_hrp
import yfinance as yf

# Données
prices = yf.download(['AAPL', 'MSFT', 'GOOGL'], period='2y')['Close']
returns = prices.pct_change().dropna()

# Test
w, port, ret = optimize_hrp(
    returns=returns,
    risk_measure='vol',  # Mesure HRP/HERC
    rf=0.025,
    linkage='ward',
    codependence='pearson'
)

print(f"Poids:\n{w}")
```

### Test Modèle Classique
```python
from models import optimize_max_sharpe
import yfinance as yf

# Données
prices = yf.download(['AAPL', 'MSFT', 'GOOGL'], period='2y')['Close']
returns = prices.pct_change().dropna()

# Test
w, port, ret = optimize_max_sharpe(
    returns=returns,
    risk_measure='MV',  # Mesure classique
    rf=0.025
)

print(f"Poids:\n{w}")
```

---

## 📞 Support Supplémentaire

Si le problème persiste :

1. **Vérifier les versions:**
```bash
python --version  # Python 3.8+
pip list | grep -i "streamlit\|riskfolio\|pandas\|numpy"
```

2. **Réinstaller les dépendances:**
```bash
pip install -r requirements.txt --upgrade
```

3. **Vérifier la structure:**
```bash
ls -la models/
cat models/__init__.py
```

4. **Consulter les logs:**
   - Streamlit affiche les erreurs dans le terminal
   - Utiliser `try/except` pour capturer les erreurs détaillées

---

## 🔄 Commandes Utiles

```bash
# Redémarrer Streamlit
Ctrl+C  # Arrêter
python -m streamlit run app.py  # Relancer

# Vider le cache Streamlit
python -m streamlit cache clear

# Tester un modèle spécifique
python -c "from models import optimize_hrp; print(optimize_hrp.__doc__)"

# Vérifier Riskfolio-Lib
python -c "import riskfolio as rp; print(rp.__version__)"
```

---

## ✅ Checklist de Validation

- [ ] Python 3.8+ installé
- [ ] Toutes les dépendances installées (`pip install -r requirements.txt`)
- [ ] Dossier `models/` existe avec les 3 fichiers .py + `__init__.py`
- [ ] `python -c "from models import *"` fonctionne
- [ ] `python -m py_compile app.py` sans erreur
- [ ] `python test_models.py` tous les tests passent
- [ ] `python -m streamlit run app.py` démarre l'application
- [ ] Les données Yahoo Finance se téléchargent correctement
- [ ] Les statistiques s'affichent avant l'optimisation
- [ ] Le dendrogramme s'affiche pour HRP/HERC/NCO
- [ ] Tous les 13 modèles s'exécutent sans erreur
