import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX
from datetime import datetime, timedelta, timezone
import os


def load_temperature_series(csv_path: str) -> pd.Series:
    """Charge les données météo et retourne la série temporelle des températures UTC."""
    df = pd.read_csv(csv_path, parse_dates=["date"])
    df = df.sort_values("date")
    serie = df.set_index("date")["temperature_2m"]

    # Assurer que l'index est en UTC timezone-aware
    if serie.index.tz is None:
        serie.index = serie.index.tz_localize("UTC")
    else:
        serie.index = serie.index.tz_convert("UTC")

    return serie


def get_last_valid_timestamp(serie: pd.Series) -> pd.Timestamp:
    """Renvoie la dernière heure d'observation valide avant l'heure actuelle (UTC)."""
    now = datetime.now(timezone.utc).replace(minute=0, second=0, microsecond=0)
    return serie.index[serie.index < now].max()


def generate_forecast(serie: pd.Series, steps: int) -> tuple[pd.Series, pd.DataFrame]:
    """Entraîne le modèle SARIMA et prédit `steps` pas de temps."""
    model = SARIMAX(serie, order=(1, 1, 1), seasonal_order=(0, 1, 1, 24),
                    enforce_stationarity=False, enforce_invertibility=False)
    results = model.fit(disp=False)
    forecast = results.get_forecast(steps=steps)
    pred = forecast.predicted_mean
    conf = forecast.conf_int()
    return pred, conf


def save_forecast(pred: pd.Series, conf: pd.DataFrame, name: str, output_dir: str):
    """Sauvegarde les fichiers CSV pour les prévisions et intervalles de confiance."""
    pred.to_csv(os.path.join(output_dir, f"pred_{name}.csv"))
    conf.to_csv(os.path.join(output_dir, f"conf_{name}.csv"))
    print(f"✅ Prévisions '{name}' sauvegardées ({len(pred)} pas de temps)")


def main():
    csv_input = "csv/meteo_aix.csv"
    output_dir = "csv"

    print("📥 Chargement des données...")
    serie = load_temperature_series(csv_input)
    last_valid_time = get_last_valid_timestamp(serie)
    serie_truncated = serie[:last_valid_time]

    print(f"📊 Données utilisées jusqu'à : {last_valid_time}")

    # --- Prévision sur 24h ---
    print("🔮 Génération des prévisions sur 24h...")
    pred_24h, conf_24h = generate_forecast(serie_truncated, steps=24)
    save_forecast(pred_24h, conf_24h, "24h", output_dir)

    # --- Prévision sur 1 mois ---
    print("🔮 Génération des prévisions sur 1 mois (720h)...")
    pred_month, conf_month = generate_forecast(serie_truncated, steps=720)
    save_forecast(pred_month, conf_month, "1mois", output_dir)

    print("🎉 Prévisions mises à jour avec succès.")


if __name__ == "__main__":
    main()
