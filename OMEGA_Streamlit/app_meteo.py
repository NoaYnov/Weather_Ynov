
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.seasonal import seasonal_decompose
from sklearn.metrics import mean_squared_error, mean_absolute_error
import warnings

warnings.filterwarnings("ignore")
st.set_page_config(layout="wide")

st.title("Analyse Météo avec Streamlit")

# Upload ou chargement par défaut

df = pd.read_csv("csv/meteo_aix.csv", parse_dates=["date"])

# Préparation des données
df.set_index("date", inplace=True)
df = df.asfreq('H')

st.subheader("Aperçu des données")
st.write(df.head())

with st.expander("Informations générales"):
    import io
    buffer = io.StringIO()
    df.info(buf=buffer)
    st.text(buffer.getvalue())
    st.write(df.describe())
    st.write("Valeurs manquantes :")
    st.write(df.isna().sum())

# Visualisations
st.subheader("Boxplot des variables numériques")
fig, ax = plt.subplots(figsize=(12, 6))
df.select_dtypes(include='number').plot.box(vert=False, ax=ax)
st.pyplot(fig)

st.subheader("Évolution des variables météorologiques")
# fig, ax = plt.subplots(len(df.columns), 1, figsize=(15, len(df.columns)*2.5))
# for i, col in enumerate(df.columns):
#     df[col].plot(ax=ax[i], title=col)
# plt.tight_layout()
# st.pyplot(fig)

# Décomposition saisonnière
st.subheader("Décomposition saisonnière")
target_var = st.selectbox("Choisissez une variable pour la décomposition :", df.columns)
period = st.number_input("Période de saisonnalité (ex: 24 pour horaire, 168 pour hebdo)", value=24)
decomp = seasonal_decompose(df[target_var].dropna(), model='additive', period=int(period))
fig = decomp.plot()
fig.set_size_inches(10, 8)
st.pyplot(fig)

from datetime import timedelta

# --- Chargement des prévisions SARIMA pré-calculées ---
@st.cache_data
def load_forecast_data():
    pred = pd.read_csv("csv/pred_24h.csv", index_col=0, parse_dates=True).squeeze()
    conf = pd.read_csv("csv/conf_24h.csv", index_col=0, parse_dates=True)
    return pred, conf

st.subheader("Prévision SARIMA sur 24h")

# --- Données historiques
serie_temp = df[target_var].dropna()
last_date = serie_temp.index.max()
future_dates_24h = [last_date + timedelta(hours=i + 1) for i in range(24)]

# --- Chargement des prédictions
pred_24h, conf_24h = load_forecast_data()

# --- Graphique Prédiction vs Réalité ---
def plot_forecast(history, future_dates, forecast, confidence):
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(history[-48:], label="Historique (48h)", color="blue")
    ax.plot(future_dates, forecast, label="Prévision 24h", color="red")
    ax.fill_between(future_dates,
                    confidence.iloc[:, 0],  # lower
                    confidence.iloc[:, 1],  # upper
                    color="pink", alpha=0.3, label="Intervalle de confiance")
    ax.set_xlabel("Date")
    ax.set_ylabel(target_var)
    ax.legend()
    st.pyplot(fig)
    plt.close(fig)

plot_forecast(serie_temp, future_dates_24h, pred_24h, conf_24h)

# --- Évaluation des performances sur la période de recouvrement ---
if len(serie_temp) >= 24:
    real = serie_temp[-24:]
    pred = pred_24h.loc[real.index.intersection(pred_24h.index)]
    if not pred.empty:
        st.write("**MAE:**", mean_absolute_error(real.loc[pred.index], pred))
        st.write("**RMSE:**", mean_squared_error(real.loc[pred.index], pred, squared=False))

st.info(
    "Prévisions SARIMA sur 24h à partir de la dernière heure connue.\\n"
    "Les fichiers `pred_24h.csv` et `conf_24h.csv` sont régénérés automatiquement."
)


