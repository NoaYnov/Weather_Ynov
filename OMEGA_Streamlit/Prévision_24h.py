# 0_🌡️_Prévision_24h.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import timedelta

st.set_page_config(page_title="Prévision météo - 24h", layout="wide")
st.title("Prévision météo sur 24 heures (Aix-en-Provence)")

@st.cache_data
def load_data():
    df = pd.read_csv("csv/meteo_aix.csv", parse_dates=["date"])
    return df.sort_values("date")

df = load_data()
serie_temp = df.set_index("date")["temperature_2m"]

col_hum = "relative_humidity_2m"
col_press = "surface_pressure"
last_row = df.iloc[-1]

st.metric("Humidité (%)", f"{last_row[col_hum]:.1f}")
st.metric("Pression au sol (hPa)", f"{last_row[col_press]:.1f}")

@st.cache_data
def load_forecast():
    pred = pd.read_csv("csv/pred_24h.csv", index_col=0, parse_dates=True).squeeze()
    conf = pd.read_csv("csv/conf_24h.csv", index_col=0, parse_dates=True)
    return pred, conf

pred_24h, conf_24h = load_forecast()
last_date = serie_temp.index.max()
future_dates = [last_date + timedelta(hours=i + 1) for i in range(24)]

def plot_forecast(history, future_dates, forecast, confidence):
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.plot(history[-48:], label="Historique (48h)")
    ax.plot(future_dates, forecast, label="Prévision 24h", color="red")
    ax.fill_between(future_dates, confidence.iloc[:, 0], confidence.iloc[:, 1],
                    color="pink", alpha=0.3)
    ax.set_xlabel("Date")
    ax.set_ylabel("Température (°C)")
    ax.legend()
    st.pyplot(fig)
    plt.close(fig)

plot_forecast(serie_temp, future_dates, pred_24h, conf_24h)
