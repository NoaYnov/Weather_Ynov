import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX
from datetime import datetime, timedelta, timezone

# Chargement des données
df = pd.read_csv("OMEGA_Streamlit/csv/meteo_aix.csv", parse_dates=["date"])
df = df.sort_values("date")

# Série avec timezone UTC
serie = df.set_index("date")["temperature_2m"]
serie.index = serie.index.tz_convert("UTC")

# Date actuelle (UTC) arrondie à l’heure
now_utc = datetime.now(timezone.utc).replace(minute=0, second=0, microsecond=0)
last_observed = serie.index[serie.index < now_utc].max()
serie_tronquee = serie[:last_observed]

# Fonction générique de prédiction
def generate_forecast_and_save(steps, pred_file, conf_file):
    model = SARIMAX(serie_tronquee, order=(1, 1, 1), seasonal_order=(0, 1, 1, 24),
                    enforce_stationarity=False, enforce_invertibility=False)
    results = model.fit(disp=False)
    forecast = results.get_forecast(steps=steps)
    pred = forecast.predicted_mean
    conf = forecast.conf_int()
    pred.to_csv(pred_file)
    conf.to_csv(conf_file)
    print(f"✅ Fichiers sauvegardés : {pred_file}, {conf_file}")

# Génération prévision 24h
generate_forecast_and_save(24, "OMEGA_Streamlit/csv/pred_24h.csv", "OMEGA_Streamlit/csv/conf_24h.csv")

# Génération prévision 1 mois (720h)
generate_forecast_and_save(720, "OMEGA_Streamlit/csv/pred_1mois.csv", "OMEGA_Streamlit/csv/conf_1mois.csv")
