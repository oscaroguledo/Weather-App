# WeatherApp Documentation

Complete reference guide for the WeatherApp Open-Meteo API client.

## Table of Contents

1. [Installation](#installation)
2. [Quick Start](#quick-start)
3. [Class Reference](#class-reference)
4. [Parameters](#parameters)
5. [Variable Categories](#variable-categories)
6. [Data Periods](#data-periods)
7. [Time Settings](#time-settings)
8. [Examples](#examples)
9. [Constants Reference](#constants-reference)

---

## Installation

```bash
pip install openmeteo-requests requests-cache retry-requests numpy pandas
```

---

## Quick Start

```python
from main import WeatherApp

# Get current weather and 7-day forecast
app = WeatherApp(
    hourly_variables=["temperature_2m", "precipitation"],
    current_variables=["temperature_2m"],
    forecast_days=7
)

results = app.get_weather()
print(results[0]["hourly"])
print(results[0]["current"])
```

---

## Class Reference

### `WeatherApp` Class

The main class for interacting with the Open-Meteo API.

#### Constructor Parameters

All parameters are optional except at least one variable list must be provided.

### Variable Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `hourly_variables` | `List[str]` | `None` | List of hourly weather variables to fetch |
| `daily_variables` | `List[str]` | `None` | List of daily weather variables to fetch |
| `current_variables` | `List[str]` | `None` | List of current weather variables to fetch |
| `minutely_15_variables` | `List[str]` | `None` | List of 15-minutely weather variables to fetch |

### Location Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `latitude` | `float` | `52.52` | Latitude in decimal degrees (WGS84) |
| `longitude` | `float` | `13.41` | Longitude in decimal degrees (WGS84) |
| `elevation` | `float` | `None` | Elevation in meters. Uses 90m DEM if not specified |

### Time Range Parameters

| Parameter | Type | Default | Range | Description |
|-----------|------|---------|-------|-------------|
| `forecast_days` | `int` | `None` | 0-16 | Number of forecast days to return |
| `forecast_hours` | `int` | `None` | >0 | Number of forecast hours to return |
| `forecast_minutely_15` | `int` | `None` | >0 | Number of 15-min forecast steps |
| `past_days` | `int` | `None` | 0-92 | Number of past days to include |
| `past_hours` | `int` | `None` | >0 | Number of past hours to include |
| `past_minutely_15` | `int` | `None` | >0 | Number of past 15-min steps |
| `start_date` | `str` | `None` | YYYY-MM-DD | Start date for historical data |
| `end_date` | `str` | `None` | YYYY-MM-DD | End date for historical data |

### Settings Parameters

| Parameter | Type | Default | Options | Description |
|-----------|------|---------|---------|-------------|
| `timezone` | `str` | `"auto"` | See timezones below | Timezone for timestamps |
| `models` | `List[str]` | `["best_match"]` | See models below | Weather models to use |
| `temperature_unit` | `str` | `"celsius"` | `celsius`, `fahrenheit` | Temperature unit |
| `wind_speed_unit` | `str` | `"kmh"` | `kmh`, `ms`, `mph`, `kn` | Wind speed unit |
| `precipitation_unit` | `str` | `"mm"` | `mm`, `inch` | Precipitation unit |
| `timeformat` | `str` | `"iso8601"` | `iso8601`, `unixtime` | Timestamp format |
| `cell_selection` | `str` | `"land"` | `land`, `sea`, `nearest` | Grid cell selection method |

---

## Variable Categories

### Hourly Variables (Surface)

#### Temperature
- `temperature_2m` - Air temperature at 2m above ground (°C or °F)
- `temperature_80m` - Air temperature at 80m above ground
- `temperature_120m` - Air temperature at 120m above ground
- `temperature_180m` - Air temperature at 180m above ground

#### Humidity & Dew Point
- `relative_humidity_2m` - Relative humidity at 2m (%)
- `dewpoint_2m` - Dew point temperature at 2m (°C or °F)
- `apparent_temperature` - Feels-like temperature combining wind, humidity, solar (°C or °F)
- `wet_bulb_temperature_2m` - Wet bulb temperature at 2m

#### Wind
- `wind_speed_10m` - Wind speed at 10m above ground
- `wind_speed_80m` - Wind speed at 80m above ground
- `wind_speed_120m` - Wind speed at 120m above ground
- `wind_speed_180m` - Wind speed at 180m above ground
- `wind_direction_10m` - Wind direction at 10m (degrees)
- `wind_direction_80m` - Wind direction at 80m (degrees)
- `wind_direction_120m` - Wind direction at 120m (degrees)
- `wind_direction_180m` - Wind direction at 180m (degrees)
- `wind_gusts_10m` - Maximum wind gusts at 10m in preceding hour

#### Precipitation
- `precipitation` - Total precipitation (rain + showers + snow) in preceding hour
- `rain` - Rain from large-scale weather systems in preceding hour
- `showers` - Showers from convective precipitation in preceding hour
- `snowfall` - Snowfall amount in preceding hour (cm)
- `snow_depth` - Snow depth on the ground (meters)
- `precipitation_probability` - Probability of precipitation > 0.1mm (%)

#### Pressure
- `sea_level_pressure` - Atmospheric pressure reduced to mean sea level (hPa)
- `surface_pressure` - Atmospheric pressure at surface (hPa)
- `pressure_msl` - Alias for sea_level_pressure

#### Clouds
- `cloud_cover` - Total cloud cover as area fraction (%)
- `cloud_cover_low` - Low level clouds and fog up to 3km (%)
- `cloud_cover_mid` - Mid level clouds from 3 to 8km (%)
- `cloud_cover_high` - High level clouds from 8km (%)

#### Solar Radiation
- `shortwave_radiation` - Global horizontal irradiation, preceding hour mean (W/m²)
- `direct_radiation` - Direct solar radiation on horizontal plane (W/m²)
- `diffuse_radiation` - Diffuse solar radiation (W/m²)
- `direct_normal_irradiance` - Direct normal irradiance (W/m²)
- `global_tilted_irradiance` - Total radiation on tilted pane (W/m²)
- `terrestrial_radiation` - Longwave terrestrial radiation (W/m²)
- `shortwave_radiation_instant` - Shortwave radiation at indicated time (W/m²)
- `direct_radiation_instant` - Direct radiation at indicated time (W/m²)
- `diffuse_radiation_instant` - Diffuse radiation at indicated time (W/m²)
- `direct_normal_irradiance_instant` - DNI at indicated time (W/m²)
- `global_tilted_irradiance_instant` - GTI at indicated time (W/m²)
- `terrestrial_radiation_instant` - Terrestrial radiation at indicated time (W/m²)

#### UV & Sunshine
- `uv_index` - UV index at indicated time
- `uv_index_clear_sky` - UV index assuming cloud-free conditions
- `sunshine_duration` - Duration of sunshine in preceding hour (seconds)
- `is_day` - 1 if daylight, 0 at night

#### Soil
- `soil_temperature_0cm` - Soil temperature at surface (°C or °F)
- `soil_temperature_6cm` - Soil temperature at 6cm depth
- `soil_temperature_18cm` - Soil temperature at 18cm depth
- `soil_temperature_54cm` - Soil temperature at 54cm depth
- `soil_moisture_0_to_1cm` - Soil water content at 0-1cm depth (m³/m³)
- `soil_moisture_1_to_3cm` - Soil water content at 1-3cm depth (m³/m³)
- `soil_moisture_3_to_9cm` - Soil water content at 3-9cm depth (m³/m³)
- `soil_moisture_9_to_27cm` - Soil water content at 9-27cm depth (m³/m³)
- `soil_moisture_27_to_81cm` - Soil water content at 27-81cm depth (m³/m³)

#### Atmospheric & Other
- `weather_code` - WMO weather interpretation code
- `visibility` - Viewing distance (meters)
- `evapotranspiration` - Evapotranspiration from land surface (mm)
- `et0_fao_evapotranspiration` - Reference ET₀ from well-watered grass (mm)
- `vapour_pressure_deficit` - VPD in kilopascals (kPa)
- `cape` - Convective available potential energy (J/kg)
- `lifted_index` - Lifted index
- `convective_inhibition` - Convective inhibition
- `freezing_level_height` - Altitude of 0°C level (meters)
- `boundary_layer_height` - Planetary boundary layer height (meters)
- `total_column_integrated_water_vapour` - Total precipitable water

### Hourly Variables (Pressure Levels)

Pressure level variables available for 19 pressure levels (1000hPa to 30hPa).
Altitude ranges from ~110m (1000hPa) to ~22km (30hPa).

**Available at all pressure levels:**
- `temperature_1000hPa` through `temperature_30hPa`
- `relative_humidity_1000hPa` through `relative_humidity_30hPa`
- `dew_point_1000hPa` through `dew_point_30hPa`
- `cloud_cover_1000hPa` through `cloud_cover_30hPa`
- `wind_speed_1000hPa` through `wind_speed_30hPa`
- `wind_direction_1000hPa` through `wind_direction_30hPa`
- `geopotential_height_1000hPa` through `geopotential_height_30hPa`

**Common pressure levels and approximate altitudes:**
| Level | Altitude | Use Case |
|-------|----------|----------|
| 1000 hPa | 110m | Surface/near-surface |
| 925 hPa | 800m | Low level |
| 850 hPa | 1500m | Lower troposphere |
| 700 hPa | 3km | Mid troposphere |
| 500 hPa | 5.6km | Upper troposphere |
| 300 hPa | 9.2km | Jet stream level |
| 200 hPa | 11.8km | Lower stratosphere |
| 100 hPa | 15.8km | Stratosphere |
| 50 hPa | 19.3km | Upper stratosphere |
| 30 hPa | 22km | Top of data |

### Daily Variables

#### Temperature
- `temperature_2m_max` - Maximum daily air temperature at 2m
- `temperature_2m_min` - Minimum daily air temperature at 2m
- `temperature_2m_mean` - Mean daily air temperature at 2m
- `apparent_temperature_max` - Maximum daily apparent temperature
- `apparent_temperature_min` - Minimum daily apparent temperature
- `apparent_temperature_mean` - Mean daily apparent temperature

#### Sun
- `sunrise` - Sunrise time (ISO8601)
- `sunset` - Sunset time (ISO8601)
- `daylight_duration` - Number of seconds of daylight
- `sunshine_duration` - Number of seconds of sunshine (>120 W/m² direct)

#### Precipitation
- `precipitation_sum` - Sum of daily precipitation (mm)
- `rain_sum` - Sum of daily rain (mm)
- `showers_sum` - Sum of daily showers (mm)
- `snowfall_sum` - Sum of daily snowfall (cm)
- `precipitation_hours` - Number of hours with rain
- `precipitation_probability_max` - Maximum daily precipitation probability
- `precipitation_probability_mean` - Mean daily precipitation probability
- `precipitation_probability_min` - Minimum daily precipitation probability

#### Wind
- `wind_speed_10m_max` - Maximum daily wind speed at 10m
- `wind_gusts_10m_max` - Maximum daily wind gusts at 10m
- `wind_direction_10m_dominant` - Dominant wind direction

#### Solar & Other
- `shortwave_radiation_sum` - Daily sum of solar radiation (MJ/m²)
- `et0_fao_evapotranspiration` - Daily sum of reference evapotranspiration (mm)
- `uv_index_max` - Daily maximum UV index
- `uv_index_clear_sky_max` - Daily maximum UV index (cloud-free)
- `weather_code` - Most severe weather condition of the day (WMO code)

### Current Variables

- `temperature_2m` - Current air temperature at 2m
- `relative_humidity_2m` - Current relative humidity at 2m
- `apparent_temperature` - Current apparent temperature
- `precipitation` - Current precipitation
- `rain` - Current rain
- `showers` - Current showers
- `snowfall` - Current snowfall
- `weather_code` - Current weather condition
- `cloud_cover` - Current cloud cover (%)
- `sea_level_pressure` - Current pressure at sea level
- `surface_pressure` - Current surface pressure
- `wind_speed_10m` - Current wind speed at 10m
- `wind_direction_10m` - Current wind direction at 10m
- `wind_gusts_10m` - Current wind gusts at 10m
- `is_day` - Whether it is currently day (1) or night (0)

### 15-Minutely Variables

**Only available in Central Europe and North America.** Other regions use interpolated hourly data.

- `temperature_2m` - Air temperature at 2m
- `relative_humidity_2m` - Relative humidity at 2m
- `dewpoint_2m` - Dew point at 2m
- `apparent_temperature` - Apparent temperature
- `precipitation` - Precipitation in preceding 15 minutes
- `rain` - Rain in preceding 15 minutes
- `showers` - Showers in preceding 15 minutes
- `snowfall` - Snowfall in preceding 15 minutes
- `snowfall_height` - Snowfall height
- `freezing_level_height` - Freezing level height
- `shortwave_radiation` - Shortwave radiation (15-min mean)
- `direct_radiation` - Direct radiation (15-min mean)
- `diffuse_radiation` - Diffuse radiation (15-min mean)
- `direct_normal_irradiance` - DNI (15-min mean)
- `global_tilted_irradiance` - GTI (15-min mean)
- `global_tilted_irradiance_instant` - GTI instant
- `terrestrial_radiation` - Terrestrial radiation
- `shortwave_radiation_instant` - Shortwave instant
- `direct_radiation_instant` - Direct instant
- `diffuse_radiation_instant` - Diffuse instant
- `direct_normal_irradiance_instant` - DNI instant
- `sunshine_duration` - Sunshine duration (15-min sum)
- `lightning_potential` - Lightning potential index (LPI)
- `cape` - Convective available potential energy
- `wind_speed_10m` - Wind speed at 10m
- `wind_speed_80m` - Wind speed at 80m
- `wind_direction_10m` - Wind direction at 10m
- `wind_direction_80m` - Wind direction at 80m
- `wind_gusts_10m` - Wind gusts at 10m
- `visibility` - Visibility
- `weather_code` - Weather code
- `is_day` - Day/night indicator

---

## Data Periods

### Hourly Data
- Time resolution: 1 hour
- Maximum forecast: 16 days (384 hours)
- Most variables are instantaneous values for the indicated hour
- Precipitation variables are sum/average of preceding hour
- Solar radiation is average of preceding hour
- Past data available: up to 92 days

### Daily Data
- Time resolution: 1 day
- Maximum forecast: 16 days
- All values are 24-hour aggregations from hourly values
- Sunrise/sunset in local time
- Past data available: up to 92 days

### Current Data
- Single time step representing current conditions
- Based on 15-minutely weather model data
- Available for all variables that exist in hourly data

### 15-Minutely Data
- Time resolution: 15 minutes
- Only available in Central Europe and North America
- Uses HRRR (North America) or ICON-D2/AROME (Europe) models
- Other regions fall back to interpolated hourly data

---

## Time Settings

### Timezones

Common timezones:
- `"auto"` - Automatically resolve from coordinates (default)
- `"GMT"` - Greenwich Mean Time
- `"America/New_York"`, `"America/Chicago"`, `"America/Denver"`, `"America/Los_Angeles"`
- `"Europe/London"`, `"Europe/Berlin"`, `"Europe/Moscow"`
- `"Asia/Tokyo"`, `"Asia/Singapore"`, `"Asia/Bangkok"`
- `"Australia/Sydney"`, `"Pacific/Auckland"`
- `"Africa/Cairo"`, `"America/Sao_Paulo"`

Any timezone from the IANA timezone database is supported.

### Units

**Temperature:**
- `"celsius"` - Degrees Celsius (default)
- `"fahrenheit"` - Degrees Fahrenheit

**Wind Speed:**
- `"kmh"` - Kilometers per hour (default)
- `"ms"` - Meters per second
- `"mph"` - Miles per hour
- `"kn"` - Knots

**Precipitation:**
- `"mm"` - Millimeters (default)
- `"inch"` - Inches

### Time Format

- `"iso8601"` - ISO 8601 timestamps (default), e.g., "2024-01-15T12:00"
- `"unixtime"` - UNIX timestamps in seconds since epoch (GMT+0)

---

## Examples

### Example 1: Basic Temperature Forecast

```python
from main import WeatherApp

app = WeatherApp(
    hourly_variables=["temperature_2m"],
    latitude=52.52,  # Berlin
    longitude=13.41,
    forecast_days=7
)

results = app.get_weather()
df = results[0]["hourly"]
print(df)
```

### Example 2: Aviation Weather (Pressure Levels)

```python
app = WeatherApp(
    hourly_variables=[
        "temperature_2m",
        "wind_speed_1000hPa",
        "wind_direction_1000hPa",
        "wind_speed_850hPa",
        "wind_direction_850hPa",
        "wind_speed_300hPa",
        "wind_direction_300hPa",
        "geopotential_height_500hPa"
    ],
    latitude=51.47,  # London Heathrow
    longitude=-0.46,
    forecast_days=2
)

results = app.get_weather()
print(results[0]["hourly"])
```

### Example 3: Agricultural Monitoring

```python
app = WeatherApp(
    hourly_variables=[
        "temperature_2m",
        "relative_humidity_2m",
        "precipitation",
        "soil_moisture_0_to_1cm",
        "soil_moisture_1_to_3cm",
        "soil_moisture_3_to_9cm",
        "et0_fao_evapotranspiration",
        "vapour_pressure_deficit"
    ],
    daily_variables=[
        "temperature_2m_max",
        "temperature_2m_min",
        "precipitation_sum",
        "et0_fao_evapotranspiration"
    ],
    latitude=38.0,  # California Central Valley
    longitude=-120.0,
    forecast_days=7
)

results = app.get_weather()
print(results[0]["daily"])
```

### Example 4: Solar PV Planning

```python
app = WeatherApp(
    hourly_variables=[
        "shortwave_radiation",
        "direct_radiation",
        "diffuse_radiation",
        "direct_normal_irradiance",
        "global_tilted_irradiance",
        "temperature_2m",
        "cloud_cover"
    ],
    latitude=35.68,  # Tokyo
    longitude=139.76,
    forecast_days=3
)

results = app.get_weather()
hourly = results[0]["hourly"]
daily_sum = hourly["shortwave_radiation"].sum() / 1000  # Convert to kWh/m²
print(f"Total solar radiation: {daily_sum:.2f} kWh/m²")
```

### Example 5: Severe Weather Monitoring

```python
app = WeatherApp(
    hourly_variables=[
        "cape",
        "lifted_index",
        "convective_inhibition",
        "wind_gusts_10m",
        "precipitation_probability"
    ],
    minutely_15_variables=[
        "lightning_potential",
        "wind_gusts_10m",
        "cape"
    ],
    latitude=35.47,  # Oklahoma (tornado alley)
    longitude=-97.5,
    forecast_hours=24,
    forecast_minutely_15=96  # 24 hours of 15-min data
)

results = app.get_weather()
print(results[0]["hourly"])
print(results[0]["minutely_15"])
```

### Example 6: Marine Weather

```python
app = WeatherApp(
    hourly_variables=[
        "temperature_2m",
        "wind_speed_10m",
        "wind_direction_10m",
        "wind_gusts_10m",
        "sea_level_pressure",
        "precipitation",
        "weather_code"
    ],
    latitude=50.0,  # North Sea
    longitude=0.0,
    cell_selection="sea",  # Prefer sea grid cells
    forecast_days=5
)

results = app.get_weather()
print(results[0]["hourly"])
```

### Example 7: Mountain Weather

```python
app = WeatherApp(
    hourly_variables=[
        "temperature_2m",
        "snowfall",
        "snow_depth",
        "freezing_level_height",
        "wind_speed_10m",
        "wind_gusts_10m",
        "cloud_cover",
        "visibility"
    ],
    latitude=46.8182,  # Swiss Alps
    longitude=8.2275,
    elevation=2500,  # Force elevation for mountain peak
    forecast_days=3
)

results = app.get_weather()
print(f"Elevation used: {results[0]['elevation']}m")
print(results[0]["hourly"])
```

### Example 8: Model Comparison

```python
app = WeatherApp(
    hourly_variables=["temperature_2m", "precipitation"],
    models=["best_match", "ecmwf_ifs_hres", "gfs_seamless", "meteofrance_seamless"],
    forecast_days=3
)

results = app.get_weather()
for result in results:
    print(f"\nModel: {result['model']}")
    df = result["hourly"]
    print(f"Temp range: {df['temperature_2m'].min():.1f} - {df['temperature_2m'].max():.1f}")
    print(f"Total precip: {df['precipitation'].sum():.1f}mm")
```

### Example 9: Historical Data Retrieval

```python
app = WeatherApp(
    hourly_variables=["temperature_2m", "precipitation"],
    start_date="2024-01-01",
    end_date="2024-01-31",
    timezone="auto"
)

results = app.get_weather()
df = results[0]["hourly"]
print(f"Mean temperature: {df['temperature_2m'].mean():.1f}°C")
print(f"Total precipitation: {df['precipitation'].sum():.1f}mm")
```

### Example 10: Multi-Period Data

```python
app = WeatherApp(
    hourly_variables=["temperature_2m", "precipitation", "wind_speed_10m"],
    daily_variables=["temperature_2m_max", "temperature_2m_min", "precipitation_sum"],
    current_variables=["temperature_2m", "weather_code", "wind_speed_10m"],
    latitude=40.71,  # New York
    longitude=-74.01,
    timezone="America/New_York",
    forecast_days=7
)

results = app.get_weather()
result = results[0]

print("Current conditions:")
print(f"  Temperature: {result['current']['temperature_2m']}°C")
print(f"  Weather: {result['current']['weather_code']}")

print("\nHourly forecast (next 24h):")
print(result["hourly"].head(24))

print("\nDaily forecast:")
print(result["daily"])
```

---

## Constants Reference

### Data Periods
```python
DATA_PERIODS = {"daily", "hourly", "current", "minutely_15"}
```

### Temperature Units
```python
TEMPERATURE_UNITS = {"celsius", "fahrenheit"}
```

### Wind Speed Units
```python
WIND_SPEED_UNITS = {"kmh", "ms", "mph", "kn"}
```

### Precipitation Units
```python
PRECIPITATION_UNITS = {"mm", "inch"}
```

### Time Formats
```python
TIMEFORMATS = {"iso8601", "unixtime"}
```

### Cell Selection Methods
```python
CELL_SELECTION = {"land", "sea", "nearest"}
```

### Pressure Levels
```python
PRESSURE_LEVELS = [1000, 975, 950, 925, 900, 850, 800, 700, 600, 500, 400, 300, 250, 200, 150, 100, 70, 50, 30]
```

---

## Weather Models

### European Models
- `ecmwf_ifs_hres` - ECMWF IFS HRES (9km, 15 days, 6hr updates)
- `ecmwf_ifs025` - ECMWF IFS 0.25°
- `ecmwf_aifs025_single` - ECMWF AIFS 0.25° Single

### US Models
- `gfs_seamless` - NCEP GFS Seamless
- `gfs_global` - NCEP GFS Global 0.11°/0.25°
- `gfs_hrrr` - NCEP HRRR U.S. Conus
- `ncep_nbm_conus` - NCEP NBM U.S. Conus
- `ncep_nam_conus` - NCEP NAM U.S. Conus

### French Models
- `meteofrance_seamless` - Météo-France Seamless
- `meteofrance_arpege_world` - ARPEGE World
- `meteofrance_arpege_europe` - ARPEGE Europe
- `meteofrance_arome_france` - AROME France

### German Models
- `dwd_icon_seamless` - DWD ICON Seamless
- `dwd_icon_global` - DWD ICON Global
- `dwd_icon_eu` - DWD ICON EU
- `dwd_icon_d2` - DWD ICON D2

### UK Models
- `ukmo_seamless` - UK Met Office Seamless
- `ukmo_global_deterministic_10km` - UKMO Global 10km
- `ukmo_uk_deterministic_2km` - UKMO UK 2km

### Other Models
- `jma_seamless`, `jma_msm`, `jma_gsm` - Japan
- `kma_seamless`, `kma_ldps`, `kma_gdps` - Korea
- `gem_seamless`, `gem_global` - Canada
- `metno_seamless`, `metno_nordic` - Norway
- `knmi_seamless` - Netherlands
- `meteoswiss_seamless` - Switzerland
- `cma_grapes_global` - China
- `bom_access_global` - Australia
- And more...

---

## Return Value Structure

The `get_weather()` method returns a list of dictionaries, one per requested model.

```python
[
    {
        "model": "best_match",
        "coordinates": {
            "latitude": 52.52,
            "longitude": 13.41
        },
        "elevation": 44.8,
        "timezone": "Europe/Berlin",
        "timezone_abbreviation": "CET",
        "utc_offset_seconds": 3600,
        "hourly": DataFrame,      # If hourly_variables provided
        "daily": DataFrame,       # If daily_variables provided
        "current": dict,          # If current_variables provided
        "minutely_15": DataFrame  # If minutely_15_variables provided
    },
    # ... additional models if requested
]
```

---

## Error Handling

The application validates all inputs and raises `ValueError` for:
- Invalid variable names
- Invalid timezone
- Invalid model names
- Invalid units or timeformat
- Invalid date formats
- Start date after end date

Example:

```python
try:
    app = WeatherApp(
        hourly_variables=["invalid_variable"]
    )
except ValueError as e:
    print(f"Error: {e}")
```

---

## API Limits

- Non-commercial use: < 10,000 daily API calls
- No authentication required for free tier
- Commercial use requires API key

For details see: https://open-meteo.com/en/docs

---

## Additional Resources

- [Open-Meteo Website](https://open-meteo.com)
- [Open-Meteo API Docs](https://open-meteo.com/en/docs)
- [WMO Weather Codes](https://open-meteo.com/en/docs#weathervariables)
