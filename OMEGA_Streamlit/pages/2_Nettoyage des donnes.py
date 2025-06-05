import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Nettoyage des données", layout="wide")
st.title(" Nettoyage & Prétraitement des données météo")

# --- Chargement des données brutes ---
@st.cache_data
def load_raw_data():
    df = pd.read_csv("csv/meteo_aix.csv", parse_dates=["date"])
    df = df.sort_values("date")
    return df

df_raw = load_raw_data()

# --- Introduction pédagogique ---
st.markdown("""
##  Description du prétraitement appliqué

Avant toute modélisation, il est crucial d'assurer la qualité des données. Voici les étapes appliquées :

- **Tri chronologique** des données par date.
- **Détection des valeurs manquantes** dans chaque variable.
- **Remplissage des valeurs manquantes** :
    - Si la distribution est **symétrique**, on utilise la **moyenne**.
    - Si la distribution est **asymétrique**, on utilise la **médiane** (plus robuste aux valeurs extrêmes).
- Pas de suppression de lignes pour préserver la continuité temporelle.

""")

# --- Affichage des données brutes ---
st.subheader("Aperçu des données brutes")
st.dataframe(df_raw.head(5))

# --- Analyse des valeurs manquantes ---
st.subheader("🔍 Valeurs manquantes (avant nettoyage)")
na_counts = df_raw.isna().sum()
total_missing = na_counts.sum()

if total_missing == 0:
    st.success("Aucune valeur manquante détectée dans ce jeu de données. ")
else:
    st.warning("Certaines colonnes contiennent des valeurs manquantes :")
    st.write(na_counts[na_counts > 0])

# --- Fonction de nettoyage ---
@st.cache_data
def clean_data(df):
    df_clean = df.copy()
    cleaning_log = []

    for col in df_clean.columns:
        if col == "date":
            continue

        if df_clean[col].isnull().sum() > 0:
            skew = df_clean[col].skew()
            if abs(skew) < 1:
                strategy = "moyenne"
                fill_value = df_clean[col].mean()
            else:
                strategy = "médiane"
                fill_value = df_clean[col].median()

            df_clean[col] = df_clean[col].fillna(fill_value)
            cleaning_log.append(f"{col} → Remplacé par la {strategy}")

    return df_clean, cleaning_log

df_cleaned, cleaning_steps = clean_data(df_raw)

# --- Résumé des opérations ---
st.subheader(" Opérations de nettoyage appliquées")
if cleaning_steps:
    for step in cleaning_steps:
        st.markdown(f"- {step}")
else:
    st.markdown("Aucun remplacement nécessaire. Les données étaient déjà complètes.")

# --- Aperçu des données propres ---
st.subheader("Aperçu des données après nettoyage")
st.dataframe(df_cleaned.head(5))
