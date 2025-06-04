import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import timedelta

# --- Titre ---
st.title("Prévisions météo Aix-en-Provence")

# --- Chargement des données météo ---
@st.cache_data
def load_data():
    df = pd.read_csv("OMEGA_Streamlit/csv/meteo_aix.csv", parse_dates=["date"])
    df = df.sort_values("date")
    return df

df = load_data()

# --- Affichage des données récentes ---
st.subheader("Données météo récentes")
st.dataframe(df.tail(10))

# --- Sélection de la colonne à prédire ---
col_temp = st.selectbox("Choisissez la colonne à prédire :", ["temperature_2m"], key="col_temp")
col_hum = "relative_humidity_2m"
col_press = "surface_pressure"

# --- Affichage des dernières valeurs ---
st.subheader("Dernières valeurs d'humidité et pression")
last_row = df.iloc[-1]
st.metric("Humidité (%)", f"{last_row[col_hum]:.1f}")
st.metric("Pression au sol (hPa)", f"{last_row[col_press]:.1f}")

# --- Chargement des prévisions pré-calculées ---
@st.cache_data
def load_forecast_data():
    pred = pd.read_csv("OMEGA_Streamlit/csv/pred_24h.csv", index_col=0, parse_dates=True).squeeze()
    conf = pd.read_csv("OMEGA_Streamlit/csv/conf_24h.csv", index_col=0, parse_dates=True)
    return pred, conf

st.subheader("Prévision température sur 24h")
serie_temp = df.set_index("date")[col_temp]

# --- Chargement des prévisions SARIMA ---
pred_24h, conf_24h = load_forecast_data()

# --- Génération des dates futures ---
last_date = serie_temp.index[-1]
future_dates_24h = [last_date + timedelta(hours=i + 1) for i in range(24)]

# --- Affichage du graphique ---
def plot_forecast(history, future_dates, forecast, confidence):
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(history[-48:], label="Historique (48h)")
    ax.plot(future_dates, forecast, label="Prévision 24h", color="red")
    ax.fill_between(future_dates, confidence.iloc[:, 0], confidence.iloc[:, 1],
                    color="pink", alpha=0.3)
    ax.set_xlabel("Date")
    ax.set_ylabel("Température (°C)")
    ax.legend()
    st.pyplot(fig)
    plt.close(fig)

plot_forecast(serie_temp, future_dates_24h, pred_24h, conf_24h)

# --- Info utilisateur ---
st.info(
    "Les prévisions SARIMA sont pré-calculées pour accélérer l'affichage.\n"
    "Un script externe met à jour ces fichiers tous les jours.\n\n"
    "Colonnes attendues dans le CSV : `date`, `temperature_2m`, `relative_humidity_2m`, `surface_pressure`."
)
