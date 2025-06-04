import openmeteo_requests

import pandas as pd
import requests_cache
from retry_requests import retry
from datetime import datetime

def setup():

	# Setup the Open-Meteo API client with cache and retry on error
	cache_session = requests_cache.CachedSession('.cache', expire_after = -1)
	retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
	openmeteo = openmeteo_requests.Client(session = retry_session)

	# Make sure all required weather variables are listed here
	# The order of variables in hourly or daily is important to assign them correctly below
	url = "https://archive-api.open-meteo.com/v1/archive"
	end_date = datetime.now().strftime("%Y-%m-%d")
	print(end_date)
	params = {
		"latitude": 43.5213,
		"longitude": 5.4228,
		"start_date": "2010-01-01",
		"end_date": end_date,
		"hourly": ["temperature_2m", "pressure_msl", "surface_pressure", "wind_speed_100m", "wind_speed_10m", "wind_direction_10m", "wind_direction_100m", "apparent_temperature", "cloud_cover", "rain", "cloud_cover_low", "cloud_cover_mid", "cloud_cover_high", "snowfall", "precipitation", "relative_humidity_2m"],
		"timezone": "auto"
	}
	responses = openmeteo.weather_api(url, params=params)

	# Process first location. Add a for-loop for multiple locations or weather models
	response = responses[0]
	print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
	print(f"Elevation {response.Elevation()} m asl")
	print(f"Timezone {response.Timezone()}{response.TimezoneAbbreviation()}")
	print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

	# Process hourly data. The order of variables needs to be the same as requested.
	hourly = response.Hourly()
	hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
	hourly_pressure_msl = hourly.Variables(1).ValuesAsNumpy()
	hourly_surface_pressure = hourly.Variables(2).ValuesAsNumpy()
	hourly_wind_speed_100m = hourly.Variables(3).ValuesAsNumpy()
	hourly_wind_speed_10m = hourly.Variables(4).ValuesAsNumpy()
	hourly_wind_direction_10m = hourly.Variables(5).ValuesAsNumpy()
	hourly_wind_direction_100m = hourly.Variables(6).ValuesAsNumpy()
	hourly_apparent_temperature = hourly.Variables(7).ValuesAsNumpy()
	hourly_cloud_cover = hourly.Variables(8).ValuesAsNumpy()
	hourly_rain = hourly.Variables(9).ValuesAsNumpy()
	hourly_cloud_cover_low = hourly.Variables(10).ValuesAsNumpy()
	hourly_cloud_cover_mid = hourly.Variables(11).ValuesAsNumpy()
	hourly_cloud_cover_high = hourly.Variables(12).ValuesAsNumpy()
	hourly_snowfall = hourly.Variables(13).ValuesAsNumpy()
	hourly_precipitation = hourly.Variables(14).ValuesAsNumpy()
	hourly_relative_humidity_2m = hourly.Variables(15).ValuesAsNumpy()

	hourly_data = {"date": pd.date_range(
		start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
		end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
		freq = pd.Timedelta(seconds = hourly.Interval()),
		inclusive = "left"
	)}

	hourly_data["temperature_2m"] = hourly_temperature_2m
	hourly_data["pressure_msl"] = hourly_pressure_msl
	hourly_data["surface_pressure"] = hourly_surface_pressure
	hourly_data["wind_speed_100m"] = hourly_wind_speed_100m
	hourly_data["wind_speed_10m"] = hourly_wind_speed_10m
	hourly_data["wind_direction_10m"] = hourly_wind_direction_10m
	hourly_data["wind_direction_100m"] = hourly_wind_direction_100m
	hourly_data["apparent_temperature"] = hourly_apparent_temperature
	hourly_data["cloud_cover"] = hourly_cloud_cover
	hourly_data["rain"] = hourly_rain
	hourly_data["cloud_cover_low"] = hourly_cloud_cover_low
	hourly_data["cloud_cover_mid"] = hourly_cloud_cover_mid
	hourly_data["cloud_cover_high"] = hourly_cloud_cover_high
	hourly_data["snowfall"] = hourly_snowfall
	hourly_data["precipitation"] = hourly_precipitation
	hourly_data["relative_humidity_2m"] = hourly_relative_humidity_2m

	hourly_dataframe = pd.DataFrame(data = hourly_data)
	hourly_dataframe.to_csv("csv/meteo_aix.csv", index = False)