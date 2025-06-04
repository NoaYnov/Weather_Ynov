import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import timedelta

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

st.subheader("Dernières valeurs d'humidité et pression")
last_row = df.iloc[-1]
st.metric("Humidité (%)", f"{last_row[col_hum]:.1f}")
st.metric("Pression au sol (hPa)", f"{last_row[col_press]:.1f}")

# --- Chargement des prévisions SARIMA pré-calculées ---
@st.cache_data
def load_forecast_data():
    pred = pd.read_csv("OMEGA_Streamlit/csv/pred_24h.csv", index_col=0, parse_dates=True).squeeze()
    conf = pd.read_csv("OMEGA_Streamlit/csv/conf_24h.csv", index_col=0, parse_dates=True)
    return pred, conf

st.subheader("Prévision température sur 24h")
serie_temp = df.set_index("date")[col_temp]

# --- Prédictions ---
pred_24h, conf_24h = load_forecast_data()

# --- Déduire les dates futures à partir de la dernière date réelle ---
last_date = serie_temp.index.max()
future_dates_24h = [last_date + timedelta(hours=i + 1) for i in range(24)]

# --- Graphique ---
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

st.info(
    "Prévisions SARIMA sur 24h à partir de la dernière heure connue.\n"
    "Les fichiers `pred_24h.csv` et `conf_24h.csv` sont régénérés chaque jour automatiquement."
)
