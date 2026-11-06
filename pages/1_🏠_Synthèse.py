"""Accueil : ce que fait l'application, les deux marchés et leurs règles d'exécution."""
import pandas as pd
import streamlit as st

from portefeuille import marches as M
from portefeuille import optimisation as O

st.title("🏠 Riskfolio")
st.markdown("Allocation de portefeuille avec Riskfolio-Lib et **backtest réaliste** sur deux marchés : la "
            "**BRVM** et le **marché américain** (Yahoo Finance). Les données viennent des dépôts de données "
            "de BRVM Analytics et de FinanceMatrix, avec leurs règles de lecture : divisions du nominal "
            "appliquées, dividendes contrôlés contre les cours et nets d'impôt.")

c1, c2, c3 = st.columns(3)
c1.page_link("pages/2_📈_Optimisation.py", label="Optimiser une allocation", icon="📈")
c2.page_link("pages/3_🧪_Backtest.py", label="Tester une allocation dans le passé", icon="🧪")
c3.page_link("pages/4_ℹ️_À_propos.py", label="Modèles et méthode", icon="ℹ️")

st.subheader("Règles d'exécution du backtest")
lignes = []
for m in M.MARCHES.values():
    r = m.regles
    lignes.append({
        "Marché": m.nom,
        "Référence": m.nom_reference,
        "Exécution": "clôture de la séance suivante, si le titre s'échange",
        "Règlement-livraison": f"J+{r.reglement}",
        "Frais par opération": f"{r.frais * 100:g} %".replace(".", ","),
        "Part du volume de la séance": f"{r.participation * 100:g} % au plus",
        "Provision d'achat": f"cours + {r.marge_provision * 100:g} %".replace(".", ",") if r.marge_provision else "cours",
        "Dividendes": r.impot_dividendes,
    })
st.dataframe(pd.DataFrame(lignes).set_index("Marché").T, use_container_width=True)
st.caption("Mêmes règles que les moteurs de stratégies de BRVM Analytics et de FinanceMatrix. Sur la BRVM, la "
           "provision couvre la limite de variation de séance (7,5 %) ; la participation limitée rend compte de "
           "la faible liquidité de nombreux titres.")

st.subheader(f"{len(O.MODELES)} modèles d'allocation")
st.dataframe(pd.DataFrame([{"Modèle": n, "Famille": m.famille.replace("_", " ").capitalize(),
                            "Principe": m.description} for n, m in O.MODELES.items()]).set_index("Modèle"),
             use_container_width=True)
