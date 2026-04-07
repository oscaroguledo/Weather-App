# Weather-App

A Python-based weather application using the Open-Meteo API. Supports hourly, daily, current, and 15-minutely weather data with pressure level variables and multiple weather models.

## Installation

```bash
pip install openmeteo-requests requests-cache retry-requests numpy pandas
```

## Quick Start

```python
from main import WeatherApp

# Simple hourly forecast
app = WeatherApp(
    hourly_variables=["temperature_2m", "precipitation"],
    forecast_days=7
)
results = app.get_weather()
print(results[0]["hourly"])
```

## Usage Examples

### Basic Hourly Forecast

```python
from main import WeatherApp

app = WeatherApp(
    hourly_variables=["temperature_2m", "relative_humidity_2m", "wind_speed_10m"],
    latitude=52.52,
    longitude=13.41,
    forecast_days=7
)

results = app.get_weather()
for result in results:
    print(f"Model: {result['model']}")
    print(result["hourly"].head())
```

### Multiple Data Periods

```python
app = WeatherApp(
    hourly_variables=["temperature_2m", "precipitation"],
    daily_variables=["temperature_2m_max", "temperature_2m_min", "precipitation_sum"],
    current_variables=["temperature_2m", "weather_code"],
    latitude=40.71,
    longitude=-74.01,
    timezone="America/New_York"
)

results = app.get_weather()
result = results[0]

print("Current:", result["current"])
print("\nHourly:\n", result["hourly"].head())
print("\nDaily:\n", result["daily"].head())
```

### Pressure Level Variables

```python
app = WeatherApp(
    hourly_variables=[
        "temperature_2m",
        "temperature_1000hPa",
        "temperature_850hPa",
        "temperature_500hPa",
        "relative_humidity_1000hPa",
        "wind_speed_1000hPa"
    ],
    forecast_days=3
)

results = app.get_weather()
print(results[0]["hourly"])
```

### Multiple Weather Models

```python
app = WeatherApp(
    hourly_variables=["temperature_2m"],
    models=["best_match", "ecmwf_ifs_hres", "gfs_seamless"],
    forecast_days=3
)

results = app.get_weather()
for result in results:
    print(f"\nModel: {result['model']}")
    print(result["hourly"][["date", "temperature_2m"]].head(3))
```

### 15-Minutely Data

```python
app = WeatherApp(
    minutely_15_variables=["temperature_2m", "precipitation", "wind_gusts_10m"],
    latitude=48.85,
    longitude=2.35,
    forecast_minutely_15=24
)

results = app.get_weather()
print(results[0]["minutely_15"])
```

### Custom Units

```python
app = WeatherApp(
    hourly_variables=["temperature_2m", "wind_speed_10m", "precipitation"],
    temperature_unit="fahrenheit",
    wind_speed_unit="mph",
    precipitation_unit="inch",
    forecast_days=5
)

results = app.get_weather()
print(results[0]["hourly"])
```

### Historical Data

```python
app = WeatherApp(
    hourly_variables=["temperature_2m", "precipitation"],
    past_days=3,
    forecast_days=7
)

results = app.get_weather()
print(results[0]["hourly"])
```

### Date Range

```python
app = WeatherApp(
    daily_variables=["temperature_2m_max", "temperature_2m_min"],
    start_date="2024-01-01",
    end_date="2024-01-07"
)

results = app.get_weather()
print(results[0]["daily"])
```

### Elevation Override

```python
app = WeatherApp(
    hourly_variables=["temperature_2m"],
    latitude=46.8182,
    longitude=8.2275,
    elevation=1500,
    forecast_days=3
)

results = app.get_weather()
print(f"Elevation: {results[0]['elevation']}m")
```

### Solar Radiation

```python
app = WeatherApp(
    hourly_variables=[
        "shortwave_radiation",
        "direct_radiation",
        "diffuse_radiation",
        "uv_index"
    ],
    latitude=35.68,
    longitude=139.76,
    forecast_days=3
)

results = app.get_weather()
print(results[0]["hourly"])
```

### Cell Selection

```python
app = WeatherApp(
    hourly_variables=["temperature_2m"],
    latitude=21.31,
    longitude=-157.86,
    cell_selection="sea",
    forecast_days=3
)

results = app.get_weather()
```

## Available Variables

### Hourly
- Temperature: `temperature_2m`, `temperature_80m/120m/180m`
- Humidity: `relative_humidity_2m`, `dewpoint_2m`
- Wind: `wind_speed_10m/80m`, `wind_direction_10m`, `wind_gusts_10m`
- Precipitation: `precipitation`, `rain`, `showers`, `snowfall`
- Pressure: `sea_level_pressure`, `surface_pressure`
- Clouds: `cloud_cover`, `cloud_cover_low/mid/high`
- Solar: `shortwave_radiation`, `direct_radiation`, `diffuse_radiation`, `uv_index`
- Soil: `soil_temperature_0/6/18/54cm`, `soil_moisture_0_to_1cm` (etc.)
- **Pressure Levels**: `temperature_1000hPa` through `temperature_30hPa` (19 levels)

### Daily
- `temperature_2m_max/min`, `sunrise/sunset`, `precipitation_sum`, `uv_index_max`

### Current
- `temperature_2m`, `relative_humidity_2m`, `precipitation`, `weather_code`, `wind_speed_10m`

### 15-Minutely
- `temperature_2m`, `precipitation`, `wind_gusts_10m`, `shortwave_radiation`, `cape`

## Weather Models

- `best_match` (default), `ecmwf_ifs_hres`, `gfs_seamless`, `meteofrance_seamless`, `dwd_icon_seamless`, `ukmo_seamless`, `jma_seamless`, and 40+ more.

## API Reference

See [Open-Meteo API Documentation](https://open-meteo.com/en/docs) for full details.
