import streamlit as st
import pandas as pd

# Titre de la page
st.title("Présentation des données climatiques")

# Chargement du CSV
@st.cache_data
def load_data():
    df = pd.read_csv("csv/meteo_aix.csv")  # Modifiez le chemin si nécessaire
    return df

df = load_data()

st.markdown("""
Ce jeu de données météorologiques a été collecté via [Open-Meteo](https://open-meteo.com/) pour la ville d’**Aix-en-Provence**.
Les données sont horodatées et contiennent différentes mesures atmosphériques et climatiques.
""")

# Aperçu des données
st.subheader("Aperçu du jeu de données")
st.dataframe(df.head())

# Nombre de lignes et colonnes
st.markdown(f"**Dimensions du dataset :** {df.shape[0]} lignes × {df.shape[1]} colonnes")

# Description des variables
st.subheader("Description des variables")

data_description = {
    "date": "Date de l'observation",
    "temperature_2m": "Température de l’air à 2 mètres du sol (°C)",
    "pressure_msl": "Pression atmosphérique au niveau de la mer (hPa)",
    "surface_pressure": "Pression atmosphérique à la surface (hPa)",
    "wind_speed_100m": "Vitesse du vent à 100 mètres (km/h)",
    "wind_speed_10m": "Vitesse du vent à 10 mètres (km/h)",
    "wind_direction_10m": "Direction du vent à 10 mètres (°)",
    "wind_direction_100m": "Direction du vent à 100 mètres (°)",
    "apparent_temperature": "Température ressentie (°C)",
    "cloud_cover": "Couverture nuageuse totale (%)",
    "rain": "Pluie de la dernière heure (mm)",
    "cloud_cover_low": "Couverture nuageuse basse (jusqu'à 3 km) (%)",
    "cloud_cover_mid": "Couverture nuageuse moyenne (3 à 8 km) (%)",
    "cloud_cover_high": "Couverture nuageuse haute (plus de 8 km) (%)",
    "snowfall": "Chute de neige sur les 15 dernières minutes (cm)",
    "precipitation": "Précipitations totales de la dernière heure (mm)",
    "relative_humidity_2m": "Humidité relative à 2 mètres du sol (%)"
}

# Affichage de la description sous forme de tableau
desc_df = pd.DataFrame(list(data_description.items()), columns=["Variable", "Description"])
st.dataframe(desc_df)

# Optionnel : Informations générales
st.subheader("Informations générales")
st.markdown("""
- **Période couverte :** {} à {}
- **Source :** Open-Meteo
""".format(df['date'].min(), df['date'].max()))

# Matrice de corrélation
st.subheader("Matrice de corrélation")

# On ne garde que les variables numériques pour la corrélation
num_df = df.select_dtypes(include='number')
corr_matrix = num_df.corr()

st.dataframe(corr_matrix)

# Optionnel : Affichage graphique de la matrice de corrélation
import matplotlib.pyplot as plt
import seaborn as sns

st.write("Visualisation graphique de la matrice de corrélation :")
fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
st.pyplot(fig)