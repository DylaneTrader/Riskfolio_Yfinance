"""À propos : formulation mathématique des modèles et méthode du backtest."""
import streamlit as st

from portefeuille import backtest as B

st.title("📚 À Propos des Modèles d'Optimisation")

st.markdown("""
Cette page présente les fondements mathématiques et les objectifs de chaque modèle 
d'optimisation disponible dans l'application.
""")

# Portefeuille de Rendement Maximum
with st.expander("📈 Portefeuille de Rendement Maximum"):
    st.markdown("""
    ### Objectif
    Maximiser le rendement espéré du portefeuille sans contrainte explicite sur le risque.

    ### Formulation Mathématique

    $$
    \\begin{aligned}
    \\max_{w} \\quad & \\mu^T w \\\\
    \\text{s.t.} \\quad & w^T \\mathbf{1} = 1 \\\\
    & w \\geq 0
    \\end{aligned}
    $$

    Où :
    - $w$ : vecteur des poids du portefeuille
    - $\\mu$ : vecteur des rendements espérés
    - $\\mathbf{1}$ : vecteur de uns

    ### Caractéristiques
    - Convient aux investisseurs très tolérants au risque
    - Peut conduire à des portefeuilles très concentrés
    - Ne considère pas explicitement la diversification
    """)

# Portefeuille de Risque Minimum
with st.expander("🛡️ Portefeuille de Risque Minimum"):
    st.markdown("""
    ### Objectif
    Minimiser le risque du portefeuille mesuré par une fonction de risque $\\phi(w)$.

    ### Formulation Mathématique

    $$
    \\begin{aligned}
    \\min_{w} \\quad & \\phi(w) \\\\
    \\text{s.t.} \\quad & w^T \\mathbf{1} = 1 \\\\
    & w \\geq 0
    \\end{aligned}
    $$

    Pour la variance (MV), $\\phi(w) = w^T \\Sigma w$ où $\\Sigma$ est la matrice de covariance.

    ### Caractéristiques
    - Idéal pour les investisseurs averses au risque
    - Privilégie la préservation du capital
    - Peut avoir des rendements attendus faibles
    - La mesure de risque $\\phi$ peut être : Variance, CVaR, Drawdown Maximum, etc.
    """)

# Portefeuille de Sharpe Maximum
with st.expander("⚖️ Portefeuille de Sharpe Maximum"):
    st.markdown("""
    ### Objectif
    Maximiser le ratio de Sharpe, qui mesure le rendement excédentaire par unité de risque.

    ### Formulation Mathématique

    $$
    \\begin{aligned}
    \\max_{w} \\quad & \\frac{\\mu^T w - r_f}{\\sqrt{w^T \\Sigma w}} \\\\
    \\text{s.t.} \\quad & w^T \\mathbf{1} = 1 \\\\
    & w \\geq 0
    \\end{aligned}
    $$

    Où :
    - $r_f$ : taux sans risque
    - $\\Sigma$ : matrice de covariance des rendements

    ### Caractéristiques
    - Équilibre optimal entre rendement et risque
    - Convient à la plupart des investisseurs rationnels
    - Correspond au portefeuille tangent sur la frontière efficiente
    - Solution du modèle de Markowitz classique
    """)

# Portefeuille d'Utilité Maximum
with st.expander("🎯 Portefeuille d'Utilité Maximum"):
    st.markdown("""
    ### Objectif
    Maximiser une fonction d'utilité qui combine rendement et risque selon l'aversion au risque de l'investisseur.

    ### Formulation Mathématique

    $$
    \\begin{aligned}
    \\max_{w} \\quad & \\mu^T w - \\lambda \\phi(w) \\\\
    \\text{s.t.} \\quad & w^T \\mathbf{1} = 1 \\\\
    & w \\geq 0
    \\end{aligned}
    $$

    Où :
    - $\\lambda$ : coefficient d'aversion au risque ($\\lambda > 0$)
    - $\\phi(w)$ : fonction de risque

    ### Caractéristiques
    - Permet d'ajuster le compromis rendement-risque via $\\lambda$
    - $\\lambda$ élevé : plus d'aversion au risque, portefeuille plus conservateur
    - $\\lambda$ faible : moins d'aversion au risque, portefeuille plus agressif
    - Basé sur la théorie de l'utilité espérée
    """)

# Portefeuille de Parité de Risque
with st.expander("⚖️ Portefeuille de Parité de Risque (Risk Parity)"):
    st.markdown("""
    ### Objectif
    Allouer les poids de sorte que chaque actif contribue de manière égale au risque total du portefeuille.

    ### Formulation Mathématique

    Trouver $w$ tel que :

    $$
    RC_i = RC_j \\quad \\forall i, j
    $$

    Où la contribution au risque de l'actif $i$ est :

    $$
    RC_i = w_i \\frac{\\partial \\phi(w)}{\\partial w_i}
    $$

    Pour la variance : $RC_i = w_i (\\Sigma w)_i$

    ### Caractéristiques
    - Diversification optimale du risque entre les actifs
    - Ne dépend pas des rendements espérés (approche purement risque)
    - Chaque actif contribue $\\frac{1}{N}$ du risque total
    - Robuste aux erreurs d'estimation des rendements
    """)

# Portefeuille de Parité de Risque Relaxée
with st.expander("🔓 Portefeuille de Parité de Risque Relaxée"):
    st.markdown("""
    ### Objectif
    Variante du modèle de parité de risque avec des contraintes plus flexibles, permettant une allocation 
    proche de la parité de risque tout en incorporant d'autres considérations.

    ### Formulation Mathématique

    $$
    \\begin{aligned}
    \\min_{w} \\quad & \\sum_{i=1}^{N} \\left( RC_i - \\frac{1}{N}\\phi(w) \\right)^2 \\\\
    \\text{s.t.} \\quad & w^T \\mathbf{1} = 1 \\\\
    & w \\geq 0 \\\\
    & \\text{contraintes additionnelles}
    \\end{aligned}
    $$

    ### Caractéristiques
    - Plus flexible que la parité de risque stricte
    - Permet d'ajouter des contraintes de concentration, de rendement minimal, etc.
    - Recherche une solution proche de la parité de risque tout en respectant les contraintes
    """)

# Portefeuilles Robustes
with st.expander("🛡️ Portefeuilles Robustes (Worst Case Mean-Variance)"):
    st.markdown("""
    ### Objectif
    Optimiser le portefeuille en tenant compte de l'incertitude dans l'estimation des paramètres 
    (rendements espérés et matrice de covariance).

    ### Formulation Mathématique

    $$
    \\begin{aligned}
    \\max_{w} \\min_{\\mu \\in U_\\mu, \\Sigma \\in U_\\Sigma} \\quad & f(w, \\mu, \\Sigma) \\\\
    \\text{s.t.} \\quad & w^T \\mathbf{1} = 1 \\\\
    & w \\geq 0
    \\end{aligned}
    $$

    Où :
    - $U_\\mu$ : ensemble d'incertitude pour les rendements espérés
    - $U_\\Sigma$ : ensemble d'incertitude pour la matrice de covariance
    - $f(w, \\mu, \\Sigma)$ : fonction objectif (rendement, Sharpe, utilité, etc.)

    ### Ensembles d'Incertitude (Box)

    $$
    U_\\mu = \\{ \\mu : \\|\\mu - \\hat{\\mu}\\|_\\infty \\leq \\epsilon_\\mu \\}
    $$

    $$
    U_\\Sigma = \\{ \\Sigma : \\|\\Sigma - \\hat{\\Sigma}\\|_F \\leq \\epsilon_\\Sigma \\}
    $$

    Où $\\epsilon$ est le paramètre d'incertitude contrôlant la taille de l'ensemble.

    ### Caractéristiques
    - Protection contre les erreurs d'estimation
    - Solution optimale dans le pire scénario (approche pessimiste)
    - $\\epsilon$ élevé : plus de robustesse, portefeuilles plus conservateurs
    - $\\epsilon$ faible : moins de robustesse, proche de l'optimisation classique
    - 4 variantes : Rendement Max, Risque Min, Sharpe Max, Utilité Max
    """)

# Modèles de Machine Learning
st.markdown("---")
st.header("🤖 Modèles de Machine Learning")

# Hierarchical Risk Parity (HRP)
with st.expander("📊 Hierarchical Risk Parity (HRP)"):
    st.markdown("""
    ### Objectif
    Allouer les poids du portefeuille en utilisant une approche hiérarchique basée sur le clustering 
    des actifs selon leur structure de corrélation, puis en appliquant la parité de risque naive.

    ### Méthodologie

    Le modèle HRP se décompose en trois étapes principales :

    **1. Regroupement Hiérarchique (Tree Clustering)**

    Utilise la matrice de distance basée sur les corrélations :

    $$
    d_{ij} = \\sqrt{\\frac{1 - \\rho_{ij}}{2}}
    $$

    où $\\rho_{ij}$ est la corrélation entre les actifs $i$ et $j$.

    **2. Ordonnancement Quasi-Diagonal (Quasi-Diagonalization)**

    Réorganise les actifs selon le dendrogramme pour former des clusters cohérents.

    **3. Allocation Récursive Bisectionnelle**

    Divise récursivement le portefeuille en deux groupes et alloue le capital inversement 
    proportionnel à la variance de chaque groupe :

    $$
    w_1 = \\frac{\\sigma_2^{-1}}{\\sigma_1^{-1} + \\sigma_2^{-1}}, \\quad w_2 = 1 - w_1
    $$

    ### Caractéristiques
    - ✅ Stable et robuste, peu sensible aux erreurs d'estimation
    - ✅ Ne nécessite pas l'inversion de la matrice de covariance
    - ✅ Peut utiliser 32 mesures de risque différentes
    - ✅ Préserve la structure de corrélation des actifs
    - ✅ Évite les poids négatifs sans contraintes explicites
    - ⚠️ Non optimal au sens de Markowitz
    - 📊 Particulièrement efficace avec des actifs fortement corrélés
    """)

# Hierarchical Equal Risk Contribution (HERC)
with st.expander("⚖️ Hierarchical Equal Risk Contribution (HERC)"):
    st.markdown("""
    ### Objectif
    Extension du modèle HRP qui alloue le capital de manière à ce que chaque cluster d'actifs 
    contribue de façon égale au risque total du portefeuille.

    ### Méthodologie

    HERC suit les mêmes étapes que HRP mais avec une allocation différente :

    **1-2. Tree Clustering et Quasi-Diagonalization**

    Identique à HRP.

    **3. Allocation par Contribution au Risque Égale**

    Au lieu d'inverser les variances, HERC alloue pour égaliser les contributions au risque :

    $$
    RC_i = w_i \\cdot \\sigma_i = \\frac{\\text{Risk Total}}{N_{clusters}}
    $$

    où $RC_i$ est la contribution au risque du cluster $i$.

    ### Différence avec HRP

    | Aspect | HRP | HERC |
    |--------|-----|------|
    | **Allocation** | Inverse de la variance | Contribution au risque égale |
    | **Objectif** | Diversification | Parité de risque par cluster |
    | **Concentration** | Peut être concentré | Plus équilibré |

    ### Caractéristiques
    - ✅ Combine clustering hiérarchique et parité de risque
    - ✅ Meilleure diversification que HRP
    - ✅ Contributions au risque équilibrées entre clusters
    - ✅ Peut utiliser 32 mesures de risque différentes
    - ✅ Robuste et stable
    - ⚠️ Calculs légèrement plus complexes que HRP
    - 📊 Idéal quand on veut équilibrer le risque entre secteurs/classes d'actifs
    """)

# Nested Clustered Optimization (NCO)
with st.expander("🎯 Nested Clustered Optimization (NCO)"):
    st.markdown("""
    ### Objectif
    Combiner l'approche hiérarchique de HRP/HERC avec l'optimisation classique de Markowitz 
    pour obtenir les avantages des deux méthodes.

    ### Méthodologie

    NCO utilise une approche en deux étapes :

    **1. Optimisation Intra-Cluster**

    Pour chaque cluster $C_k$ identifié par clustering hiérarchique, optimise localement :

    $$
    \\begin{aligned}
    \\max_{w_k} \\quad & \\text{Sharpe}(w_k) = \\frac{\\mu_k^T w_k - r_f}{\\sqrt{w_k^T \\Sigma_k w_k}} \\\\
    \\text{s.t.} \\quad & w_k^T \\mathbf{1} = 1, \\quad w_k \\geq 0
    \\end{aligned}
    $$

    où $\\mu_k$ et $\\Sigma_k$ sont limités aux actifs du cluster $C_k$.

    **2. Allocation Inter-Cluster**

    Alloue le capital entre les portefeuilles optimisés de chaque cluster :

    $$
    \\begin{aligned}
    \\max_{\\alpha} \\quad & \\text{Sharpe}(\\alpha) = \\frac{\\mu_c^T \\alpha - r_f}{\\sqrt{\\alpha^T \\Sigma_c \\alpha}} \\\\
    \\text{s.t.} \\quad & \\alpha^T \\mathbf{1} = 1, \\quad \\alpha \\geq 0
    \\end{aligned}
    $$

    où $\\mu_c$ et $\\Sigma_c$ sont calculés à partir des portefeuilles de chaque cluster.

    **3. Poids Final**

    $$
    w_i^{\\text{final}} = \\alpha_{k(i)} \\cdot w_i^{(k)}
    $$

    où $k(i)$ est le cluster auquel appartient l'actif $i$.

    ### Avantages par rapport à HRP/HERC

    | Caractéristique | NCO | HRP/HERC |
    |-----------------|-----|----------|
    | **Optimalité** | Optimisation Markowitz par cluster | Parité de risque naive |
    | **Performance** | Potentiellement supérieure | Plus conservative |
    | **Stabilité** | Moyenne | Élevée |
    | **Complexité** | Élevée | Faible |

    ### Caractéristiques
    - ✅ Combine robustesse du clustering et optimalité de Markowitz
    - ✅ Réduit le risque de sur-optimisation
    - ✅ Meilleure performance out-of-sample que Markowitz classique
    - ✅ Exploite la structure de corrélation des actifs
    - ⚠️ Plus complexe à calculer
    - ⚠️ Nécessite suffisamment d'actifs par cluster
    - 📊 Optimal quand les clusters sont bien définis (ex: secteurs, géographies)

    ### Quand Utiliser NCO ?

    - **Oui** : Portefeuille multi-secteurs ou multi-classes d'actifs
    - **Oui** : Besoin d'optimisation mais avec structure hiérarchique
    - **Oui** : Données historiques suffisantes par cluster
    - **Non** : Peu d'actifs (< 15-20)
    - **Non** : Clusters mal définis ou très corrélés
    """)

# Mesures de Risque
st.markdown("---")
st.header("📊 Mesures de Risque")

with st.expander("Voir toutes les mesures de risque"):
    st.markdown("""
    ### Variance (MV) - Écart-type
    $$\\phi(w) = \\sqrt{w^T \\Sigma w}$$
    Mesure classique de dispersion des rendements.

    ### Écart Absolu Moyen (MAD)
    $$\\phi(w) = E[|r_p - E[r_p]|]$$
    Moyenne des écarts absolus par rapport à la moyenne.

    ### Semi-Variance (MSV)
    $$\\phi(w) = E[\\min(r_p - E[r_p], 0)^2]$$
    Mesure uniquement la volatilité des rendements négatifs.

    ### Valeur à Risque Conditionnelle (CVaR)
    $$\\text{CVaR}_\\alpha(w) = E[r_p | r_p \\leq \\text{VaR}_\\alpha(w)]$$
    Moyenne des pertes au-delà du VaR (Expected Shortfall).

    ### Drawdown Maximum (MDD)
    $$\\text{MDD}(w) = \\max_{t} \\left( \\max_{s \\leq t} V_s - V_t \\right) / \\max_{s \\leq t} V_s$$
    Plus grande baisse depuis un pic historique.

    ### Drawdown Conditionnel à Risque (CDaR)
    $$\\text{CDaR}_\\alpha(w) = E[DD | DD \\geq \\text{DaR}_\\alpha]$$
    CVaR appliqué aux drawdowns.

    Et bien d'autres mesures spécialisées...
    """)

# Les 32 mesures de risque pour HRP/HERC
with st.expander("📋 Les 32 Mesures de Risque pour HRP et HERC"):
    st.markdown("""
    Les modèles HRP et HERC peuvent utiliser **32 mesures de risque différentes** pour la parité de risque naive, 
    offrant une flexibilité exceptionnelle.

    ### 🔵 1. Mesures de Dispersion (8 mesures)

    **Standard Deviation (vol)**
    $$\\sigma = \\sqrt{\\frac{1}{n}\\sum_{i=1}^{n}(r_i - \\bar{r})^2}$$
    Mesure classique de volatilité.

    **Variance**
    $$\\text{Var} = \\sigma^2$$
    Carré de l'écart-type.

    **Square Root Kurtosis (kurt)**
    $$\\text{Kurt}^{1/4} = \\left(\\frac{1}{n}\\sum_{i=1}^{n}\\frac{(r_i - \\bar{r})^4}{\\sigma^4}\\right)^{1/4}$$
    Mesure la "queue" de la distribution.

    **Mean Absolute Deviation (MAD)**
    $$\\text{MAD} = \\frac{1}{n}\\sum_{i=1}^{n}|r_i - \\bar{r}|$$
    Moyenne des écarts absolus.

    **Gini Mean Difference (GMD)**
    $$\\text{GMD} = \\frac{1}{n(n-1)}\\sum_{i=1}^{n}\\sum_{j=1}^{n}|r_i - r_j|$$
    Différence moyenne entre toutes les paires.

    **CVaR Range (cvrg)**
    $$\\text{CVaR Range} = \\text{CVaR}^+ - \\text{CVaR}^-$$
    Plage entre CVaR positif et négatif.

    **Tail Gini Range (tgrg)**
    Gini calculé sur les queues de distribution.

    **Range (rg)**
    $$\\text{Range} = \\max(r) - \\min(r)$$
    Différence entre max et min.

    ---

    ### 🔴 2. Mesures de Risque à la Baisse (10 mesures)

    **Semi Standard Deviation (semi)**
    $$\\text{SemiSD} = \\sqrt{\\frac{1}{n}\\sum_{r_i<0}r_i^2}$$
    Volatilité des rendements négatifs uniquement.

    **Square Root Semi Kurtosis (skurt)**
    Kurtosis calculée sur les rendements négatifs.

    **First Lower Partial Moment (flpm) - Omega Ratio**
    $$\\text{FLPM} = \\frac{1}{n}\\sum_{r_i<\\tau}(\\tau - r_i)$$
    Moyenne des shortfalls par rapport à un seuil $\\tau$.

    **Second Lower Partial Moment (slpm) - Sortino Ratio**
    $$\\text{SLPM} = \\sqrt{\\frac{1}{n}\\sum_{r_i<\\tau}(\\tau - r_i)^2}$$
    Racine carrée des écarts carrés négatifs.

    **Value at Risk (VaR)**
    $$\\text{VaR}_\\alpha = -\\inf\\{x : P(r \\leq x) \\geq \\alpha\\}$$
    Perte maximale avec probabilité $\\alpha$ (ex: 95%).

    **Conditional Value at Risk (CVaR)**
    $$\\text{CVaR}_\\alpha = E[r | r \\leq \\text{VaR}_\\alpha]$$
    Moyenne des pertes au-delà du VaR.

    **Entropic Value at Risk (EVaR)**
    $$\\text{EVaR}_\\alpha = \\inf_{z>0}\\left\\{z\\ln\\left(\\frac{1}{\\alpha}\\right) + z\\ln\\left(E[e^{-r/z}]\\right)\\right\\}$$
    Version entropique du VaR.

    **Relativistic Value at Risk (RLVaR)**
    Variante relativiste tenant compte de la distribution complète.

    **Tail Gini (tg)**
    $$\\text{TG} = \\frac{1}{n_\\alpha(n_\\alpha-1)}\\sum_{r_i \\leq \\text{VaR}}\\sum_{r_j \\leq \\text{VaR}}|r_i - r_j|$$
    Gini sur la queue de distribution.

    **Worst Realization (wr) - Minimax**
    $$\\text{WR} = \\min(r)$$
    Le pire rendement observé.

    ---

    ### 📉 3. Mesures de Drawdown (14 mesures)

    #### Rendements Composés (7 mesures)

    **Maximum Drawdown (mdd) - Calmar Ratio**
    $$\\text{MDD} = \\max_{t}\\left(\\frac{\\max_{s \\leq t}V_s - V_t}{\\max_{s \\leq t}V_s}\\right)$$
    Plus grande baisse depuis un pic.

    **Average Drawdown (add)**
    $$\\text{ADD} = \\frac{1}{T}\\sum_{t=1}^{T}\\text{DD}_t$$
    Moyenne de tous les drawdowns.

    **Ulcer Index (uci)**
    $$\\text{UCI} = \\sqrt{\\frac{1}{T}\\sum_{t=1}^{T}\\text{DD}_t^2}$$
    Racine carrée de la moyenne des drawdowns carrés.

    **Drawdown at Risk (dar)**
    $$\\text{DaR}_\\alpha = -\\inf\\{x : P(\\text{DD} \\leq x) \\geq \\alpha\\}$$
    VaR appliqué aux drawdowns.

    **Conditional Drawdown at Risk (cdar)**
    $$\\text{CDaR}_\\alpha = E[\\text{DD} | \\text{DD} \\geq \\text{DaR}_\\alpha]$$
    CVaR appliqué aux drawdowns.

    **Entropic Drawdown at Risk (edar)**
    EVaR appliqué aux drawdowns.

    **Relativistic Drawdown at Risk (rdar)**
    RLVaR appliqué aux drawdowns.

    #### Rendements Non Composés (7 mesures)

    Les mêmes 7 mesures calculées sur les rendements arithmétiques (non composés) :
    - **mdd_rel**, **add_rel**, **uci_rel**
    - **dar_rel**, **cdar_rel**, **edar_rel**, **rdar_rel**

    Utile pour les portefeuilles avec rééquilibrage fréquent.

    ---

    ### 📊 Tableau Récapitulatif

    | Catégorie | Nombre | Exemples Clés |
    |-----------|--------|---------------|
    | **Dispersion** | 8 | vol, variance, mad, gmd |
    | **Downside** | 10 | semi, var, cvar, evar |
    | **Drawdown Composé** | 7 | mdd, cdar, uci |
    | **Drawdown Non Composé** | 7 | mdd_rel, cdar_rel, uci_rel |
    | **TOTAL** | **32** | - |

    ### 💡 Recommandations

    **Pour la plupart des cas** : `vol` (Standard Deviation)
    - Simple et intuitif
    - Comparable à Markowitz

    **Pour risque asymétrique** : `cvar` ou `semi`
    - Mesure uniquement le risque de baisse
    - Mieux adapté aux rendements non-normaux

    **Pour gestion de drawdown** : `cdar` ou `mdd`
    - Focus sur les pertes cumulées
    - Pertinent pour allocation long-terme

    **Pour robustesse** : `mad` ou `gmd`
    - Moins sensibles aux valeurs extrêmes
    - Alternatives robustes à la variance
    """)

# Théorie de Markowitz
st.markdown("---")
st.header("📐 Théorie Moderne du Portefeuille (Markowitz)")

st.markdown("""
### Fondements

La théorie moderne du portefeuille, développée par Harry Markowitz (Prix Nobel 1990), 
repose sur les principes suivants :

1. **Frontière Efficiente** : Ensemble des portefeuilles offrant le rendement maximum pour un 
   niveau de risque donné, ou le risque minimum pour un niveau de rendement donné.

2. **Diversification** : Réduction du risque par la combinaison d'actifs dont les rendements 
   ne sont pas parfaitement corrélés.

3. **Compromis Rendement-Risque** : Les investisseurs cherchent à maximiser le rendement 
   pour un niveau de risque acceptable, ou minimiser le risque pour un rendement cible.

### Hypothèses Clés

- Les rendements suivent une distribution normale
- Les investisseurs sont rationnels et averses au risque
- Les marchés sont efficients
- Pas de coûts de transaction ni d'impôts
- Les investisseurs peuvent prêter et emprunter au taux sans risque

### Extensions et Améliorations

Les modèles modernes (comme ceux de Riskfolio-Lib) étendent la théorie de Markowitz en :

- Utilisant des mesures de risque alternatives (CVaR, Drawdown, etc.)
- Incorporant la robustesse face à l'incertitude
- Permettant des contraintes réalistes (concentration, secteur, ESG, etc.)
- Utilisant des distributions non-normales
""")

# Footer
st.markdown("---")
st.markdown("""
### 📖 Références

**Théorie Classique**
- Markowitz, H. (1952). "Portfolio Selection". The Journal of Finance.
- Rockafellar, R. T., & Uryasev, S. (2000). "Optimization of conditional value-at-risk."
- Maillard, S., Roncalli, T., & Teïletche, J. (2010). "The properties of equally weighted risk contribution portfolios."
- Ben-Tal, A., & Nemirovski, A. (1998). "Robust convex optimization."

**Modèles de Machine Learning**
- López de Prado, M. (2016). "Building Diversified Portfolios that Outperform Out of Sample". Journal of Portfolio Management.
- Raffinot, T. (2017). "Hierarchical Clustering-Based Asset Allocation". Journal of Portfolio Management.
- López de Prado, M. (2020). "Machine Learning for Asset Managers". Cambridge University Press.
- Raffinot, T. (2018). "The Hierarchical Equal Risk Contribution Portfolio". SSRN Working Paper.

### 🔗 Liens Utiles

- [Documentation Riskfolio-Lib](https://riskfolio-lib.readthedocs.io/)
- [Code source sur GitHub](https://github.com/dcajasn/Riskfolio-Lib)
- [Article HRP - López de Prado](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2708678)
- [Article HERC - Raffinot](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3237540)
""")

st.divider()
st.header("🧪 Méthode du backtest")
st.markdown(B.__doc__.split("\n", 2)[2])
