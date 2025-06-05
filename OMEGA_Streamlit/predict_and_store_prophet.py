# predict_and_store_prophet.py

import pandas as pd
from prophet import Prophet

# Chargement et préparation
df = pd.read_csv("csv/meteo_aix_hour.csv", parse_dates=["time"])
df = df[["time", "apparent_temperature (°C)"]].dropna()
df.columns = ["ds", "y"]  # Prophet exige ds/y
df = df.set_index("ds").asfreq("h").reset_index()

# Modèle Prophet
model = Prophet(daily_seasonality=True, weekly_seasonality=True, yearly_seasonality=False)
model.fit(df)

# Génération des 48 prochaines heures
future = model.make_future_dataframe(periods=48, freq='H', include_history=False)
forecast = model.predict(future)

# Extraction de la prévision utile
pred = forecast[["ds", "yhat"]].copy()
pred.columns = ["time", "predicted_temperature"]

# Sauvegarde
pred.to_csv("csv/predictions_prophet.csv", index=False)
print("Prévisions Prophet sauvegardées dans 'csv/predictions_prophet.csv'")
