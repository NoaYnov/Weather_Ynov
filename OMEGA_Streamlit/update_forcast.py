import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX
from datetime import timedelta

# Chargement
df = pd.read_csv("csv/meteo_aix.csv", parse_dates=["date"])
df = df.sort_values("date")
serie = df.set_index("date")["temperature_2m"]

# Fixe la fréquence explicite
serie = serie.asfreq("h")

# Modèle SARIMA
model = SARIMAX(serie, order=(1, 1, 1), seasonal_order=(0, 1, 1, 24),
                enforce_stationarity=False, enforce_invertibility=False)
results = model.fit(disp=False)

# Prévision 24h
forecast = results.get_forecast(steps=24)
pred = forecast.predicted_mean
conf = forecast.conf_int()

# Sauvegarde
pred.to_csv("csv/pred_24h.csv")
conf.to_csv("csv/conf_24h.csv")

print("✅ Prévisions SARIMA sauvegardées sans warning.")
