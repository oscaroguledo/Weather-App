"""Constants for Weather App Open-Meteo API integration."""

# Data periods
DATA_PERIODS = {"daily", "hourly", "current", "minutely_15"}

# Temperature units
TEMPERATURE_UNITS = {"celsius", "fahrenheit"}

# Wind speed units
WIND_SPEED_UNITS = {"kmh", "ms", "mph", "kn"}

# Precipitation units
PRECIPITATION_UNITS = {"mm", "inch"}

# Time formats
TIMEFORMATS = {"iso8601", "unixtime"}

# Cell selection methods
CELL_SELECTION = {"land", "sea", "nearest"}

TIMEZONES = {
    "auto",
    "GMT",
    "America/Anchorage",
    "America/Chicago",
    "America/Denver",
    "America/New_York",
    "America/Los_Angeles",
    "America/Sao_Paulo",
    "Europe/London",
    "Europe/Moscow",
    "Europe/Berlin",
    "Africa/Cairo",
    "Asia/Tokyo",
    "Asia/Bangkok",
    "Asia/Singapore",
    "Australia/Sydney",
    "Pacific/Auckland"
}

# Pressure levels for pressure level variables
PRESSURE_LEVELS = [1000, 975, 950, 925, 900, 850, 800, 700, 600, 500, 400, 300, 250, 200, 150, 100, 70, 50, 30]

# Generate pressure level variable names
def _generate_pressure_level_vars(base_name):
    """Generate variable names for all pressure levels."""
    return {f"{base_name}_{level}hPa" for level in PRESSURE_LEVELS}

# Pressure level variables
PRESSURE_LEVEL_VARIABLES = (
    _generate_pressure_level_vars("temperature") |
    _generate_pressure_level_vars("relative_humidity") |
    _generate_pressure_level_vars("dew_point") |
    _generate_pressure_level_vars("cloud_cover") |
    _generate_pressure_level_vars("wind_speed") |
    _generate_pressure_level_vars("wind_direction") |
    _generate_pressure_level_vars("geopotential_height")
)

# Hourly variables (includes surface and pressure level variables)
HOURLY_VARIABLES = {
    "temperature_2m",
    "relative_humidity_2m",
    "dewpoint_2m",
    "apparent_temperature",
    "precipitation_probability",
    "precipitation",
    "rain",
    "showers",
    "snowfall",
    "snow_depth",
    "weather_code",
    "sea_level_pressure",
    "surface_pressure",
    "cloud_cover",
    "cloud_cover_low",
    "cloud_cover_mid",
    "cloud_cover_high",
    "visibility",
    "evapotranspiration",
    "et0_fao_evapotranspiration",
    "vapour_pressure_deficit",
    "wind_speed_10m",
    "wind_speed_80m",
    "wind_speed_120m",
    "wind_speed_180m",
    "wind_direction_10m",
    "wind_direction_80m",
    "wind_direction_120m",
    "wind_direction_180m",
    "wind_gusts_10m",
    "temperature_80m",
    "temperature_120m",
    "temperature_180m",
    "soil_temperature_0cm",
    "soil_temperature_6cm",
    "soil_temperature_18cm",
    "soil_temperature_54cm",
    "soil_moisture_0_to_1cm",
    "soil_moisture_1_to_3cm",
    "soil_moisture_3_to_9cm",
    "soil_moisture_9_to_27cm",
    "soil_moisture_27_to_81cm",
    "uv_index",
    "uv_index_clear_sky",
    "is_day",
    "sunshine_duration",
    "wet_bulb_temperature_2m",
    "total_column_integrated_water_vapour",
    "cape",
    "lifted_index",
    "convective_inhibition",
    "freezing_level_height",
    "boundary_layer_height",
    "shortwave_radiation",
    "direct_radiation",
    "diffuse_radiation",
    "direct_normal_irradiance",
    "global_tilted_irradiance",
    "terrestrial_radiation",
    "shortwave_radiation_instant",
    "direct_radiation_instant",
    "diffuse_radiation_instant",
    "direct_normal_irradiance_instant",
    "global_tilted_irradiance_instant",
    "terrestrial_radiation_instant",
    "pressure_msl"
} | PRESSURE_LEVEL_VARIABLES

DAILY_VARIABLES = {
    "weather_code",
    "temperature_2m_max",
    "temperature_2m_min",
    "apparent_temperature_max",
    "apparent_temperature_min",
    "sunrise",
    "sunset",
    "daylight_duration",
    "sunshine_duration",
    "uv_index_max",
    "uv_index_clear_sky_max",
    "rain_sum",
    "showers_sum",
    "snowfall_sum",
    "precipitation_sum",
    "precipitation_hours",
    "precipitation_probability_max",
    "wind_speed_10m_max",
    "wind_gusts_10m_max",
    "wind_direction_10m_dominant",
    "shortwave_radiation_sum",
    "et0_fao_evapotranspiration"
}

CURRENT_VARIABLES = {
    "temperature_2m",
    "relative_humidity_2m",
    "apparent_temperature",
    "is_day",
    "precipitation",
    "rain",
    "showers",
    "snowfall",
    "weather_code",
    "cloud_cover",
    "sea_level_pressure",
    "surface_pressure",
    "wind_speed_10m",
    "wind_direction_10m",
    "wind_gusts_10m"
}

MINUTELY_15_VARIABLES = {
    "temperature_2m",
    "relative_humidity_2m",
    "dewpoint_2m",
    "apparent_temperature",
    "shortwave_radiation",
    "direct_radiation",
    "diffuse_radiation",
    "direct_normal_irradiance",
    "global_tilted_irradiance",
    "global_tilted_irradiance_instant",
    "terrestrial_radiation",
    "shortwave_radiation_instant",
    "direct_radiation_instant",
    "diffuse_radiation_instant",
    "direct_normal_irradiance_instant",
    "terrestrial_radiation_instant",
    "sunshine_duration",
    "lightning_potential",
    "precipitation",
    "snowfall",
    "rain",
    "showers",
    "snowfall_height",
    "freezing_level_height",
    "cape",
    "wind_speed_10m",
    "wind_speed_80m",
    "wind_direction_10m",
    "wind_direction_80m",
    "wind_gusts_10m",
    "visibility",
    "weather_code",
    "is_day"
}

WEATHER_MODELS = {
    "best_match",
    "ecmwf_ifs_hres",
    "ecmwf_ifs025",
    "ecmwf_aifs025_single",
    "cma_grapes_global",
    "bom_access_global",
    "gfs_seamless",
    "gfs_global",
    "gfs_hrrr",
    "ncep_nbm_conus",
    "ncep_nam_conus",
    "gfs_graphcast025",
    "ncep_aigfs025",
    "ncep_hgefs025",
    "jma_seamless",
    "jma_msm",
    "jma_gsm",
    "kma_seamless",
    "kma_ldps",
    "kma_gdps",
    "dwd_icon_seamless",
    "dwd_icon_global",
    "dwd_icon_eu",
    "dwd_icon_d2",
    "gem_seamless",
    "gem_global",
    "gem_regional",
    "gem_hrdps_continental",
    "gem_hrdps_west",
    "meteofrance_seamless",
    "meteofrance_arpege_world",
    "meteofrance_arpege_europe",
    "meteofrance_arome_france",
    "meteofrance_arome_france_hd",
    "arpae_icon2i",
    "metno_seamless",
    "metno_nordic",
    "knmi_seamless",
    "knmi_harmonie_arome_europe",
    "knmi_harmonie_arome_netherlands",
    "dmi_seamless",
    "dmi_harmonie_arome_europe",
    "ukmo_seamless",
    "ukmo_global_deterministic_10km",
    "ukmo_uk_deterministic_2km",
    "meteoswiss_seamless",
    "meteoswiss_icon_ch1",
    "meteoswiss_icon_ch2",
    "geosphere_seamless",
    "geosphere_arome_austria"
}