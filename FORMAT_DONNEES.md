# Instructions pour créer votre fichier de données

## Format requis

Votre fichier CSV ou Excel doit avoir la structure suivante :

### Structure
- **Première colonne (Index)** : Dates au format YYYY-MM-DD
- **Colonnes suivantes** : Un symbole d'actif par colonne
- **Valeurs** : Prix de clôture (nombres décimaux)

### Exemple

| Date       | AAPL   | MSFT   | GOOGL  | AMZN  |
|------------|--------|--------|--------|-------|
| 2023-01-03 | 125.07 | 239.58 | 88.59  | 84.00 |
| 2023-01-04 | 126.36 | 232.04 | 89.68  | 84.20 |
| 2023-01-05 | 125.02 | 232.90 | 89.72  | 84.67 |
| ...        | ...    | ...    | ...    | ...   |

## Fichiers d'exemple

Un fichier `exemple_donnees.csv` est fourni comme modèle.

## Conseils

### Pour CSV
1. Utilisez des virgules (`,`) comme séparateur
2. Première ligne = noms des colonnes (Date, symboles des actifs)
3. Encodage UTF-8 recommandé

### Pour Excel (XLSX)
1. Première feuille du classeur
2. Première colonne = dates
3. Colonnes suivantes = prix des actifs
4. Pas de cellules fusionnées
5. Pas de formules, uniquement des valeurs

## Sources de données possibles

### Yahoo Finance
Téléchargez manuellement :
1. Allez sur finance.yahoo.com
2. Recherchez un symbole
3. Onglet "Historical Data"
4. Téléchargez le CSV
5. Répétez pour chaque actif
6. Fusionnez les colonnes dans un seul fichier

### Bloomberg Terminal
Si vous avez accès :
1. Utilisez BDH (Bloomberg Data History)
2. Exportez vers Excel
3. Formatez selon le template ci-dessus

### Autres sources
- Investing.com
- Alpha Vantage
- Quandl
- API de votre courtier

## Validation

Avant d'importer, vérifiez :
- ✅ Pas de cellules vides (ou utilisez ffill)
- ✅ Dates dans un ordre chronologique
- ✅ Format de date cohérent
- ✅ Valeurs numériques (pas de texte)
- ✅ Même nombre de lignes pour tous les actifs
- ✅ Au moins 2 actifs (colonnes)
- ✅ Au moins 30 jours de données (recommandé : 1-2 ans)

## Dépannage

### "Erreur lors de la lecture du fichier"
- Vérifiez l'encodage (UTF-8)
- Vérifiez le format des dates
- Assurez-vous qu'il n'y a pas de caractères spéciaux

### "Optimisation échouée"
- Vérifiez qu'il y a suffisamment de données historiques
- Assurez-vous qu'il n'y a pas que des valeurs constantes
- Vérifiez que les prix sont positifs

### "Données manquantes"
- Utilisez Forward Fill (ffill) pour combler les trous
- Ou supprimez les lignes avec données manquantes
- L'application fait du ffill/bfill automatiquement

## Exemple complet

Voir le fichier `exemple_donnees.csv` fourni avec l'application.

Ce fichier contient 30 jours de données pour 5 actifs tech (AAPL, MSFT, GOOGL, AMZN, TSLA).

Vous pouvez l'utiliser directement pour tester l'application !
