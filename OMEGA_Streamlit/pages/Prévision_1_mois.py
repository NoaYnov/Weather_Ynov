# pages/1_📅_Prévision_1_mois.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import timedelta

st.title("Prévision météo sur 1 mois (Aix-en-Provence)")

@st.cache_data
def load_data():
    df = pd.read_csv("csv/meteo_aix.csv", parse_dates=["date"])
    return df.sort_values("date")

df = load_data()
serie_temp = df.set_index("date")["temperature_2m"]

@st.cache_data
def load_forecast():
    pred = pd.read_csv("csv/pred_1mois.csv", index_col=0, parse_dates=True).squeeze()
    conf = pd.read_csv("csv/conf_1mois.csv", index_col=0, parse_dates=True)
    return pred, conf

pred_1mois, conf_1mois = load_forecast()
last_date = serie_temp.index.max()
future_dates = [last_date + timedelta(hours=i + 1) for i in range(720)]

def plot_forecast(history, future_dates, forecast, confidence):
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(history[-7*24:], label="Historique (7 jours)")
    ax.plot(future_dates, forecast, label="Prévision 1 mois", color="red")
    ax.fill_between(future_dates, confidence.iloc[:, 0], confidence.iloc[:, 1],
                    color="pink", alpha=0.3)
    ax.set_xlabel("Date")
    ax.set_ylabel("Température (°C)")
    ax.legend()
    st.pyplot(fig)
    plt.close(fig)

plot_forecast(serie_temp, future_dates, pred_1mois, conf_1mois)
