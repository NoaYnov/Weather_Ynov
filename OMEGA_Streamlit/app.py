import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX
from datetime import timedelta


# --- Chargement des données ---
st.title("Prévisions météo Aix-en-Provence")

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
# st.write("Available columns in last_row:", last_row.index.tolist())
# st.write("Value of col_hum:", col_hum)
# --- Affichage humidité et pression ---
st.metric("Humidité (%)", f"{last_row[col_hum]:.1f}")
st.metric("Pression au sol (hPa)", f"{last_row[col_press]:.1f}")

# --- Prévisions SARIMA ---
def sarima_forecast(series, steps, order=(1,1,1), seasonal_order=(0,1,1,24)):
    # SARIMA simple, adapte les ordres selon ta série et saisonnalité (ici 24 pour horaire)
    model = SARIMAX(series, order=order, seasonal_order=seasonal_order, enforce_stationarity=False, enforce_invertibility=False)
    results = model.fit(disp=False)
    forecast = results.get_forecast(steps=steps)
    pred = forecast.predicted_mean
    conf_int = forecast.conf_int()
    return pred, conf_int

# --- Prévision 24h ---
st.subheader("Prévision température sur 24h")
serie_temp = df.set_index("date")[col_temp]
steps_24h = 24  # Supposé: 1h fréquence
pred_24h, conf_24h = sarima_forecast(serie_temp, steps=steps_24h)

future_dates_24h = [serie_temp.index[-1] + timedelta(hours=i+1) for i in range(steps_24h)]
plt.figure(figsize=(10,4))
plt.plot(serie_temp[-48:], label="Historique (48h)")
plt.plot(future_dates_24h, pred_24h, label="Prévision 24h", color="red")
plt.fill_between(future_dates_24h, conf_24h.iloc[:,0], conf_24h.iloc[:,1], color="pink", alpha=0.3)
plt.legend()
plt.xlabel("Date")
plt.ylabel("Température (°C)")
st.pyplot(plt.gcf())
plt.close()

# --- Prévision 5 jours (5*24h) ---
st.subheader("Prévision température sur 5 jours")
steps_5d = 5*24
pred_5d, conf_5d = sarima_forecast(serie_temp, steps=steps_5d)

future_dates_5d = [serie_temp.index[-1] + timedelta(hours=i+1) for i in range(steps_5d)]
plt.figure(figsize=(10,4))
plt.plot(serie_temp[-7*24:], label="Historique (7j)")
plt.plot(future_dates_5d, pred_5d, label="Prévision 5 jours", color="red")
plt.fill_between(future_dates_5d, conf_5d.iloc[:,0], conf_5d.iloc[:,1], color="pink", alpha=0.3)
plt.legend()
plt.xlabel("Date")
plt.ylabel("Température (°C)")
st.pyplot(plt.gcf())
plt.close()

st.info("Modèle SARIMA simple : les paramètres peuvent être ajustés pour de meilleures prévisions.\nAssurez-vous que les colonnes du CSV sont bien : date, temperature, humidite, pression.")
