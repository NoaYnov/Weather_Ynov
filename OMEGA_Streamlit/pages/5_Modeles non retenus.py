import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

st.set_page_config(layout="wide")
st.title("Prévision Temporelle : N-BEATS vs Prophet")

# === Fonctions de chargement ===
@st.cache_data
def load_actual_data():
    df = pd.read_csv("csv/meteo_aix_hour.csv", parse_dates=["time"])
    df.set_index("time", inplace=True)
    df = df.asfreq("h")
    return df

@st.cache_data
def load_nbeats_predictions():
    df = pd.read_csv("csv/predictions_nbeats.csv", parse_dates=["time"])
    df.set_index("time", inplace=True)
    return df

@st.cache_data
def load_prophet_predictions():
    df = pd.read_csv("csv/predictions_prophet.csv", parse_dates=["time"])
    df.set_index("time", inplace=True)
    return df

# === Chargement des données ===
actual_df = load_actual_data()
nbeats_df = load_nbeats_predictions()
prophet_df = load_prophet_predictions()

# === Tabs ===
tab1, tab2 = st.tabs(["📈 N-BEATS", "🔮 Prophet"])

# Fonction pour affichage dans chaque onglet
def plot_forecast(pred_df, model_name, color):
    horizon = st.radio("Durée de prévision", ["24h", "48h"], horizontal=True, key=model_name)
    n_hours = 24 if horizon == "24h" else 48
    pred_df = pred_df.iloc[:n_hours]

    if pred_df.empty:
        st.warning(f"Aucune donnée de prévision pour {model_name} sur {n_hours}h.")
        return

    start_time = pred_df.index[0]
    end_time = pred_df.index[-1]

    # Vérifie si les dates existent dans actual_df
    try:
        actual_segment = actual_df.loc[start_time:end_time]["apparent_temperature (°C)"]
    except KeyError:
        st.warning("Période non trouvée dans les données réelles.")
        return

    if actual_segment.empty:
        st.warning("Aucune donnée réelle disponible pour cette période.")
        return

    st.subheader(f"{model_name} – Prévision {horizon} vs Température réelle")
    fig, ax = plt.subplots(figsize=(12, 5))

    actual_segment.plot(ax=ax, label="Température réelle", color="blue", linestyle='--', marker='o')
    pred_df["predicted_temperature"].plot(ax=ax, label=f"Prévision ({model_name})", color=color, marker='o')

    fig.autofmt_xdate(rotation=45)
    plt.xlabel("Date et heure")
    plt.ylabel("Température (°C)")
    plt.legend()
    plt.tight_layout()
    st.pyplot(fig)
# === Onglet N-BEATS ===
with tab1:
    plot_forecast(nbeats_df, "N-BEATS", "orange")

# === Onglet Prophet ===
with tab2:
    plot_forecast(prophet_df, "Prophet", "green")
    st.markdown("""
    📊 Métriques de fiabilité globales sur nos données
    
        🌡️ Température :
        MAE : 2.38
        RMSE : 3.01
        
        🌧️ Précipitations :
        MAE : 0.14
        RMSE : 0.49
        
        💨 Vitesse du vent :
        MAE : 6.39
        RMSE : 7.90
    """)
