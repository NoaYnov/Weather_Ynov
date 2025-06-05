import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import timedelta

st.set_page_config(page_title="Prévisions 24h - WeatherForYnov", layout="centered")
st.title("Prévisions météo - Aix-en-Provence (24h)")

# --- Chargement des données historiques ---
@st.cache_data
def load_data():
    df = pd.read_csv("csv/meteo_aix.csv", parse_dates=["date"])
    df = df.sort_values("date")
    return df

df = load_data()
serie_temp = df.set_index("date")["temperature_2m"]
last_date = serie_temp.index.max()

# --- Chargement des prévisions SARIMA ---
@st.cache_data
def load_forecast_data():
    pred = pd.read_csv("csv/pred_24h.csv", index_col=0, parse_dates=True).squeeze()
    conf = pd.read_csv("csv/conf_24h.csv", index_col=0, parse_dates=True)
    return pred, conf

pred_24h, conf_24h = load_forecast_data()
future_dates_24h = [last_date + timedelta(hours=i + 1) for i in range(24)]

# --- Visualisation des prévisions ---
st.subheader("Prévision de la température pour les prochaines 24h")

def plot_forecast(history, future_dates, forecast, confidence):
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(history[-48:], label="Historique (48h)", linewidth=2)
    ax.plot(future_dates, forecast, label="Prévision SARIMA (24h)", color="red", linewidth=2)
    ax.fill_between(future_dates, confidence.iloc[:, 0], confidence.iloc[:, 1],
                    color="pink", alpha=0.3, label="Intervalle de confiance")
    ax.set_xlabel("Heure")
    ax.set_ylabel("Température (°C)")
    ax.legend()
    ax.grid(True, linestyle="--", alpha=0.5)
    st.pyplot(fig)
    plt.close(fig)

plot_forecast(serie_temp, future_dates_24h, pred_24h, conf_24h)

# --- Derniers relevés utiles ---
st.subheader("Derniers relevés météo")
last_row = df.iloc[-1]
st.metric("Température actuelle (°C)", f"{last_row['temperature_2m']:.1f}")
st.metric("Humidité relative (%)", f"{last_row['relative_humidity_2m']:.1f}")
st.metric("Pression au sol (hPa)", f"{last_row['surface_pressure']:.1f}")

# --- Note méthodologique ---
st.info(
    "Les prévisions sont générées à l'aide d'un modèle SARIMA entraîné sur les dernières données disponibles.\n"
    "Les fichiers `pred_24h.csv` et `conf_24h.csv` contiennent respectivement la température prévue et l’intervalle de confiance à 95%."
)


# MAE (Erreur Absolue Moyenne): 4.185174862417118
# RMSE (Racine de l'Erreur Quadratique Moyenne): 4.65397594233298

MAE = 4.185174862417118
RMSE = 4.65397594233298
st.sidebar.subheader("Performances du modèle")
st.sidebar.metric("MAE ", f"{MAE}")
st.sidebar.metric("RMSE ", f"{RMSE}")


