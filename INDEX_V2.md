# 📚 Index de la Documentation - Optimisation de Portefeuille v2.0

## 🚀 Pour Commencer

### Démarrage Rapide
- **[QUICKSTART_V2.md](QUICKSTART_V2.md)** ⭐ - Installation et première utilisation (5 min)
- **[USAGE.md](USAGE.md)** - Guide d'utilisation de base

### Documentation Principale
- **[README.md](README.md)** - Vue d'ensemble du projet
- **[README_FR.md](README_FR.md)** - README en français
- **[README_GITHUB.md](README_GITHUB.md)** - README pour GitHub

---

## 📖 Guides Complets

### Utilisation
- **[GUIDE_UTILISATION.md](GUIDE_UTILISATION.md)** - Guide complet d'utilisation
- **[GUIDE_SELECTION_MODELE.md](GUIDE_SELECTION_MODELE.md)** - Aide au choix du modèle
- **[FORMAT_DONNEES.md](FORMAT_DONNEES.md)** - Format des fichiers d'import

### Navigation
- **[STRUCTURE_NAVIGATION.md](STRUCTURE_NAVIGATION.md)** - Structure de navigation de l'app
- **[STRUCTURE.md](STRUCTURE.md)** ⭐ - Architecture technique du projet

---

## 🔧 Technique et Développement

### Architecture
- **[STRUCTURE.md](STRUCTURE.md)** ⭐ - Organisation des fichiers, modèles, utilisation des modules
- **[MANIFESTE.md](MANIFESTE.md)** - Vision et objectifs du projet

### Code Source
```
models/
├── __init__.py              - Exports du package
├── classic_models.py        - 6 modèles classiques
├── robust_models.py         - 4 modèles robustes
└── hierarchical_models.py   - 3 modèles ML hiérarchiques
```

- **[app.py](app.py)** - Application Streamlit principale (~1,000 lignes)
- **[test_models.py](test_models.py)** - Tests automatisés des 13 modèles

---

## 🐛 Dépannage et Support

### Résolution de Problèmes
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** ⭐ - Guide de dépannage complet
  - 10+ erreurs courantes et solutions
  - Scripts de diagnostic
  - Checklist de validation

### Changements et Versions
- **[CHANGELOG_V2.md](CHANGELOG_V2.md)** ⭐ - Nouveautés version 2.0
  - Corrections majeures (HRP/HERC/NCO)
  - Nouvelles fonctionnalités
  - Guide de migration
- **[CHANGELOG.md](CHANGELOG.md)** - Historique complet des versions

---

## 📊 Récapitulatifs

### Synthèses
- **[RÉCAPITULATIF.md](RÉCAPITULATIF.md)** - Récapitulatif du projet
- **[RÉSUMÉ.md](RÉSUMÉ.md)** - Résumé exécutif
- **[INDEX.md](INDEX.md)** - Index de la documentation (ancienne version)

---

## 📁 Fichiers Annexes

### Données
- **[exemple_donnees.csv](exemple_donnees.csv)** - Exemple de fichier de données
- **[requirements.txt](requirements.txt)** - Dépendances Python

### Système
- **[.gitignore](.gitignore)** - Fichiers exclus de Git
- **[app_backup.py](app_backup.py)** - Sauvegarde de l'ancienne version

---

## 🎯 Documents par Cas d'Usage

### Je débute avec l'application
1. ✅ [QUICKSTART_V2.md](QUICKSTART_V2.md) - Installation (5 min)
2. ✅ [USAGE.md](USAGE.md) - Utilisation de base
3. ✅ [GUIDE_SELECTION_MODELE.md](GUIDE_SELECTION_MODELE.md) - Quel modèle choisir ?
4. ✅ Page "À propos" dans l'app - Explications mathématiques

### Je veux comprendre l'architecture
1. ✅ [STRUCTURE.md](STRUCTURE.md) - Architecture complète
2. ✅ [models/](models/) - Code source des modèles
3. ✅ [app.py](app.py) - Interface Streamlit

### J'ai une erreur
1. ✅ [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Solutions aux erreurs courantes
2. ✅ [test_models.py](test_models.py) - Tester tous les modèles
3. ✅ [CHANGELOG_V2.md](CHANGELOG_V2.md) - Vérifier si c'est corrigé

### Je veux développer/étendre
1. ✅ [STRUCTURE.md](STRUCTURE.md) - Architecture et guide d'ajout de modèles
2. ✅ [models/](models/) - Exemples de code
3. ✅ [test_models.py](test_models.py) - Framework de tests

### Je veux importer mes données
1. ✅ [FORMAT_DONNEES.md](FORMAT_DONNEES.md) - Format requis
2. ✅ [exemple_donnees.csv](exemple_donnees.csv) - Exemple de fichier
3. ✅ [GUIDE_UTILISATION.md](GUIDE_UTILISATION.md) - Procédure d'import

---

## 📚 Documentation dans l'Application

### Page "À propos"
L'application contient une documentation mathématique complète accessible via le menu :

**Contenu:**
- 📖 Vue d'ensemble de l'optimisation de portefeuille
- 🔢 Formulations mathématiques des 13 modèles
- 📊 Explication des 45 mesures de risque (13 + 32)
- 🌳 Détails sur les modèles hiérarchiques (HRP, HERC, NCO)
- 📚 Références bibliographiques

**Sections:**
1. Introduction à l'optimisation de portefeuille
2. Modèles classiques (6 modèles)
3. Modèles robustes (4 modèles)
4. Modèles ML hiérarchiques (3 modèles)
5. 32 mesures de risque HRP/HERC détaillées
6. Références académiques

---

## 🔍 Recherche par Mot-Clé

### HRP / HERC / NCO
- [QUICKSTART_V2.md](QUICKSTART_V2.md) - Section "Modèles Hiérarchiques"
- [STRUCTURE.md](STRUCTURE.md) - Section "Modèles Hiérarchiques ML"
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Erreur HRP corrigée
- [CHANGELOG_V2.md](CHANGELOG_V2.md) - Correction complète
- [models/hierarchical_models.py](models/hierarchical_models.py) - Code source

### Dendrogramme
- [CHANGELOG_V2.md](CHANGELOG_V2.md) - Section "Ajout du Dendrogramme"
- [QUICKSTART_V2.md](QUICKSTART_V2.md) - Graphique automatique
- [app.py](app.py) - Fonction `plot_dendrogram()`

### Statistiques Pré-Optimisation
- [CHANGELOG_V2.md](CHANGELOG_V2.md) - Section "Restructuration de l'Interface"
- [QUICKSTART_V2.md](QUICKSTART_V2.md) - Section "Comprendre les Résultats"
- [app.py](app.py) - Section "ANALYSE DES DONNÉES"

### Mesures de Risque (45 total)
- [STRUCTURE.md](STRUCTURE.md) - Section "Mesures de Risque"
- [app.py](app.py) - Dictionnaires `RISK_MEASURES_DICT` et `HRP_HERC_RISK_MEASURES`
- Page "À propos" dans l'app - Documentation complète

### Tests
- [test_models.py](test_models.py) - Tests automatisés
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Scripts de diagnostic
- [STRUCTURE.md](STRUCTURE.md) - Section "Tests Automatisés"

---

## 📦 Dépendances

### Fichiers de Configuration
- **[requirements.txt](requirements.txt)** - Liste des packages Python requis

### Packages Principaux
```
streamlit >= 1.28.0      # Interface web
riskfolio-lib >= 5.0.0   # Optimisation de portefeuille
yfinance >= 0.2.31       # Téléchargement de données
plotly >= 5.17.0         # Visualisations interactives
pandas >= 1.5.0          # Manipulation de données
numpy >= 1.24.0          # Calculs numériques
scipy >= 1.9.0           # Clustering hiérarchique
openpyxl >= 3.1.0        # Lecture de fichiers Excel
```

---

## 🎓 Ressources Académiques

### Références Citées
Voir [CHANGELOG_V2.md](CHANGELOG_V2.md) section "Remerciements" et la page "À propos" de l'application.

**Principaux auteurs:**
- Harry Markowitz (1952) - Théorie moderne du portefeuille
- Marcos López de Prado (2016) - HRP
- Thomas Raffinot (2017) - HERC
- Philippe Artzner et al. (1999) - Mesures de risque cohérentes

---

## 📈 Statistiques du Projet

### Version Actuelle: 2.0.0

**Code:**
- ~1,500 lignes de Python
- 4 modules (app.py + 3 dans models/)
- 13 modèles d'optimisation
- 45 mesures de risque
- 8 types de visualisations

**Documentation:**
- 20+ fichiers markdown
- ~10,000 lignes de documentation
- 3 langues (principalement français)

**Fonctionnalités:**
- ✅ 3 pages (Accueil, Optimisation, À propos)
- ✅ 3 sources de données (Yahoo, CSV, XLSX)
- ✅ 13 modèles (6 classiques + 4 robustes + 3 ML)
- ✅ 45 mesures de risque
- ✅ Tests automatisés
- ✅ Architecture modulaire

---

## 🆕 Nouveautés Version 2.0

### Highlights
- ✅ **Correction HRP/HERC/NCO** - Modèles ML fonctionnels
- ✅ **Dendrogramme** - Visualisation du clustering
- ✅ **Statistiques avant optimisation** - Analyse des données en amont
- ✅ **Architecture modulaire** - Package models/
- ✅ **32 mesures de risque HRP/HERC** - Sélection automatique
- ✅ **Documentation enrichie** - 4 nouveaux guides

**Détails complets:** [CHANGELOG_V2.md](CHANGELOG_V2.md)

---

## 💡 Conseils de Lecture

### Parcours Débutant (30 min)
1. [QUICKSTART_V2.md](QUICKSTART_V2.md) - 5 min
2. [USAGE.md](USAGE.md) - 10 min
3. [GUIDE_SELECTION_MODELE.md](GUIDE_SELECTION_MODELE.md) - 10 min
4. Lancer l'app et explorer - 5 min

### Parcours Utilisateur Avancé (1h)
1. [GUIDE_UTILISATION.md](GUIDE_UTILISATION.md) - 20 min
2. [FORMAT_DONNEES.md](FORMAT_DONNEES.md) - 10 min
3. Page "À propos" dans l'app - 20 min
4. Expérimentation avec différents modèles - 10 min

### Parcours Développeur (2h)
1. [STRUCTURE.md](STRUCTURE.md) - 30 min
2. [models/](models/) - Lecture du code - 30 min
3. [test_models.py](test_models.py) - 15 min
4. [CHANGELOG_V2.md](CHANGELOG_V2.md) - 15 min
5. Expérimentation - 30 min

---

## 📞 Support

### En Cas de Problème

1. **Consulter d'abord:** [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
2. **Tester:** `python test_models.py`
3. **Vérifier:** [CHANGELOG_V2.md](CHANGELOG_V2.md) si déjà corrigé

### Contribuer

Voir [STRUCTURE.md](STRUCTURE.md) section "Développement" pour ajouter des fonctionnalités.

---

## ✅ Checklist de Démarrage

- [ ] Python 3.8+ installé
- [ ] Dépendances installées (`pip install -r requirements.txt`)
- [ ] Documentation lue : [QUICKSTART_V2.md](QUICKSTART_V2.md)
- [ ] Application lancée : `python -m streamlit run app.py`
- [ ] Premier portefeuille créé (Yahoo Finance)
- [ ] Modèle hiérarchique testé (HRP/HERC/NCO)
- [ ] Dendrogramme visualisé
- [ ] Export CSV réalisé

---

**Date de dernière mise à jour:** 24 Décembre 2025  
**Version:** 2.0.0  
**Statut:** ✅ Production
