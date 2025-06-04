import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX
from datetime import datetime, timedelta, timezone

# Chargement des données exportées via Open-Meteo
df = pd.read_csv("csv/meteo_aix.csv", parse_dates=["date"])
df = df.sort_values("date")

# Série horaire avec timezone UTC
serie = df.set_index("date")["temperature_2m"]
serie.index = serie.index.tz_convert("UTC")  # assure l'uniformité

# Récupère le moment actuel en UTC
now_utc = datetime.now(timezone.utc).replace(minute=0, second=0, microsecond=0)

# Si la dernière heure dans les données est avant maintenant (ce qui est normal)
if now_utc not in serie.index:
    last_observed = serie.index[serie.index < now_utc].max()
else:
    last_observed = now_utc

# Tronque la série jusqu'au dernier point connu
serie_tronquee = serie[:last_observed]

# SARIMA pour les 24 prochaines heures
model = SARIMAX(serie_tronquee, order=(1, 1, 1), seasonal_order=(0, 1, 1, 24),
                enforce_stationarity=False, enforce_invertibility=False)
results = model.fit(disp=False)

forecast = results.get_forecast(steps=24)
pred = forecast.predicted_mean
conf = forecast.conf_int()

# Sauvegarde des prévisions
pred.to_csv("csv/pred_24h.csv")
conf.to_csv("csv/conf_24h.csv")

print(f"✅ Prévision SARIMA sauvegardée à partir de {last_observed} UTC.")
