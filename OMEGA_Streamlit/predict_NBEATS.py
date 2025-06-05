# predict_and_store.py

import pandas as pd
from darts import TimeSeries
from darts.models import NBEATSModel
from darts.dataprocessing.transformers import Scaler

# Chargement des données
df = pd.read_csv("csv/meteo_aix_hour.csv", parse_dates=["time"])
df.set_index("time", inplace=True)
df = df.asfreq('h')
series = TimeSeries.from_series(df["apparent_temperature (°C)"].dropna())

# Normalisation
scaler = Scaler()
series_scaled = scaler.fit_transform(series)

# Split données
train, _ = series_scaled.split_after(0.8)

# Entraînement modèle
model = NBEATSModel(input_chunk_length=48, output_chunk_length=24, n_epochs=5, random_state=0)
model.fit(train, verbose=True)

# Prédiction
forecast = model.predict(n=48)
forecast = scaler.inverse_transform(forecast)

# Sauvegarde
forecast_df = forecast.to_series().reset_index()
forecast_df.columns = ["time", "predicted_temperature"]
forecast_df.to_csv("csv/predictions_nbeats.csv", index=False)
print("Prévisions sauvegardées dans 'csv/predictions_nbeats.csv'")
