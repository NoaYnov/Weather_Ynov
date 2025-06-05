import streamlit as st

# Configuration de la page
st.set_page_config(page_title="WeatherForYnov", layout="centered")

# Titre principal
st.title("WeatherForYnov - Prévision Météorologique")

# Introduction
st.markdown("""
**WeatherForYnov** est un projet fictif développé pour analyser des données climatiques historiques et fournir des prévisions météorologiques précises à l’aide de techniques de machine learning.

Cette application se concentre sur les données météorologiques d’**Aix-en-Provence**, issues de la plateforme **Open-Meteo**.
""")

# Objectifs du projet
st.subheader("Objectifs")

st.markdown("""
- Collecter et préparer les données climatiques (température, humidité, vent, etc.)
- Explorer les tendances à l’aide de visualisations statistiques
- Développer un modèle prédictif basé sur **SARIMA**
- Visualiser les résultats avec des graphiques interactifs
- Proposer une interface simple pour consulter les prévisions météo
""")

# Données utilisées
st.subheader("Données météorologiques")

st.markdown("""
Les données incluent :
- Température (réelle et ressentie)
- Pression atmosphérique
- Vitesse et direction du vent
- Humidité relative
- Couverture nuageuse
- Précipitations (pluie et neige)

Source : [Open-Meteo](https://open-meteo.com/) – Région : **Aix-en-Provence**
""")

# Technologies utilisées
st.subheader("Technologies")

st.markdown("""
- Python : Pandas, NumPy, Matplotlib, Seaborn
- Modélisation : SARIMA (via statsmodels)
- Visualisation : Plotly, Dash (ou Streamlit pour l’interface)
- Interface utilisateur : Streamlit
""")

# Footer ou note
st.markdown("---")
st.markdown("Projet réalisé dans le cadre d’un exercice pédagogique autour du machine learning et de la data science appliquée à la météo.")

