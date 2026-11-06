# Riskfolio

Application Streamlit d'allocation de portefeuille (Riskfolio-Lib) et de **backtest réaliste** sur deux
marchés : la **BRVM** et le **marché américain** (Yahoo Finance). Thème et structure de BRVM Analytics.

## Pages

| Page | Contenu |
|---|---|
| Accueil | Règles d'exécution de chaque marché, liste des modèles |
| Optimisation | Univers, période, modèle et mesure de risque ; poids, corrélations, classification, frontière |
| Backtest | Allocation recalculée à chaque rééquilibrage et exécutée aux règles du marché, comparée aux poids égaux, à la même allocation sans frictions et à l'indice |
| À propos | Formulation des 13 modèles, méthode du backtest |

## Données

| Marché | Dépôt de données | Indice de référence |
|---|---|---|
| BRVM | `DylaneTrader/Scraper-BRVM` | BRVM Composite (indice de cours) |
| États-Unis | `DylaneTrader/Scraper-FinanceMatrix` (Yahoo Finance) | S&P 500 dividendes réinvestis |

Les cours, volumes, indices et dividendes sont lus par le module `lecture_donnees` de chaque dépôt : divisions
du nominal appliquées, dividendes contrôlés contre les cours, nets d'impôt (IRVM sur la BRVM, retenue de 15 %
aux États-Unis). Un fichier CSV ou Excel de cours peut aussi servir à l'optimisation.

- **En local** : un clone de chaque dépôt dans `private/` ou à côté de ce dépôt (`BRVM_DATA_DIR`, `FM_DATA_DIR`
  pour un autre dossier).
- **Sur Streamlit Cloud** : secrets `SCRAPER_BRVM_TOKEN` et `SCRAPER_FM_TOKEN`, jetons GitHub à accès
  « Contents » en lecture seule, chacun limité à son dépôt. L'application télécharge les seuls fichiers utiles
  dans un dossier temporaire et les renouvelle toutes les 6 heures. Aucune donnée n'est écrite dans ce dépôt.

## Règles du backtest

| | BRVM | États-Unis |
|---|---|---|
| Exécution | clôture de la séance suivante, si le titre s'échange | idem |
| Règlement-livraison | J+2 | J+1 |
| Frais par achat et par vente | 1 % | 0,1 % |
| Part du volume de la séance | 20 % au plus | 20 % au plus |
| Provision d'un ordre d'achat | cours + 7,5 % (limite de séance) | cours |

Quantités entières, ni découvert ni levier ; une vente ne finance un achat qu'une fois réglée ; dividendes
versés sur les titres détenus la veille du détachement. Ce sont les règles des moteurs de stratégies de BRVM
Analytics et de FinanceMatrix. Aucune décision n'utilise de donnée postérieure à sa date.

## Lancer

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Tests

```bash
python -m pytest tests -q
```

Les tests de lecture et de parcours des pages s'exécutent quand les deux clones sont présents.
