from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
import re
import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry
from constants import (
    DATA_PERIODS, TIMEZONES, TIMEFORMATS,
    HOURLY_VARIABLES, DAILY_VARIABLES, CURRENT_VARIABLES, MINUTELY_15_VARIABLES,
    WEATHER_MODELS,
    TEMPERATURE_UNITS, WIND_SPEED_UNITS, PRECIPITATION_UNITS,
    CELL_SELECTION
)

class WeatherApp:
    def __init__(
        self,
        hourly_variables: Optional[List[str]] = None,
        daily_variables: Optional[List[str]] = None,
        current_variables: Optional[List[str]] = None,
        minutely_15_variables: Optional[List[str]] = None,
        forecast_days: Optional[int] = None,
        forecast_hours: Optional[int] = None,
        forecast_minutely_15: Optional[int] = None,
        past_days: Optional[int] = None,
        past_hours: Optional[int] = None,
        past_minutely_15: Optional[int] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        latitude: Optional[float] = 52.52,
        longitude: Optional[float] = 13.41,
        timezone: Optional[str] = "auto",
        models: Optional[List[str]] = None,
        temperature_unit: Optional[str] = "celsius",
        wind_speed_unit: Optional[str] = "kmh",
        precipitation_unit: Optional[str] = "mm",
        timeformat: Optional[str] = "iso8601",
        cell_selection: Optional[str] = "land",
        elevation: Optional[float] = None
    ):
        self.hourly_variables = hourly_variables or []
        self.daily_variables = daily_variables or []
        self.current_variables = current_variables or []
        self.minutely_15_variables = minutely_15_variables or []
        self.forecast_days = forecast_days
        self.forecast_hours = forecast_hours
        self.forecast_minutely_15 = forecast_minutely_15
        self.past_days = past_days
        self.past_hours = past_hours
        self.past_minutely_15 = past_minutely_15
        self.start_date = start_date
        self.end_date = end_date
        self.latitude = latitude
        self.longitude = longitude
        self.timezone = timezone
        self.models = models or ["best_match"]
        self.temperature_unit = temperature_unit
        self.wind_speed_unit = wind_speed_unit
        self.precipitation_unit = precipitation_unit
        self.timeformat = timeformat
        self.cell_selection = cell_selection
        self.elevation = elevation
        self.openmeteo = None

        self._validate_inputs()
        self._setup_client()

    def _validate_inputs(self):
        """Validate all input parameters."""
        if self.timezone not in TIMEZONES:
            raise ValueError(f"Timezone must be one of {TIMEZONES}")

        for model in self.models:
            if model not in WEATHER_MODELS:
                raise ValueError(f"Model '{model}' must be one of {WEATHER_MODELS}")

        if self.temperature_unit not in TEMPERATURE_UNITS:
            raise ValueError(f"Temperature unit must be one of {TEMPERATURE_UNITS}")

        if self.wind_speed_unit not in WIND_SPEED_UNITS:
            raise ValueError(f"Wind speed unit must be one of {WIND_SPEED_UNITS}")

        if self.precipitation_unit not in PRECIPITATION_UNITS:
            raise ValueError(f"Precipitation unit must be one of {PRECIPITATION_UNITS}")

        if self.timeformat not in TIMEFORMATS:
            raise ValueError(f"Time format must be one of {TIMEFORMATS}")

        if self.cell_selection not in CELL_SELECTION:
            raise ValueError(f"Cell selection must be one of {CELL_SELECTION}")

        # Validate variables
        for var in self.hourly_variables:
            if var not in HOURLY_VARIABLES:
                raise ValueError(f"Invalid hourly variable '{var}'")

        for var in self.daily_variables:
            if var not in DAILY_VARIABLES:
                raise ValueError(f"Invalid daily variable '{var}'")

        for var in self.current_variables:
            if var not in CURRENT_VARIABLES:
                raise ValueError(f"Invalid current variable '{var}'")

        for var in self.minutely_15_variables:
            if var not in MINUTELY_15_VARIABLES:
                raise ValueError(f"Invalid minutely_15 variable '{var}'")

        # Validate date formats
        if self.start_date:
            if not re.match(r"^\d{4}-\d{2}-\d{2}$", self.start_date):
                raise ValueError("Start date must be in YYYY-MM-DD format")

        if self.end_date:
            if not re.match(r"^\d{4}-\d{2}-\d{2}$", self.end_date):
                raise ValueError("End date must be in YYYY-MM-DD format")

        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValueError("Start date must be before end date")

    def _setup_client(self):
        """Setup the Open-Meteo API client with cache and retry."""
        cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
        retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
        self.openmeteo = openmeteo_requests.Client(session=retry_session)

    def get_weather(self) -> List[Dict[str, Any]]:
        """Fetch weather data from Open-Meteo API.

        Returns:
            List of results, one for each requested model
        """
        url = "https://api.open-meteo.com/v1/forecast"

        params = {
            "latitude": self.latitude,
            "longitude": self.longitude,
            "timezone": self.timezone,
            "models": ",".join(self.models),
            "temperature_unit": self.temperature_unit,
            "wind_speed_unit": self.wind_speed_unit,
            "precipitation_unit": self.precipitation_unit,
            "timeformat": self.timeformat,
            "cell_selection": self.cell_selection
        }

        if self.elevation is not None:
            params["elevation"] = self.elevation

        if self.forecast_days is not None:
            params["forecast_days"] = self.forecast_days

        if self.forecast_hours is not None:
            params["forecast_hours"] = self.forecast_hours

        if self.forecast_minutely_15 is not None:
            params["forecast_minutely_15"] = self.forecast_minutely_15

        if self.past_days is not None:
            params["past_days"] = self.past_days

        if self.past_hours is not None:
            params["past_hours"] = self.past_hours

        if self.past_minutely_15 is not None:
            params["past_minutely_15"] = self.past_minutely_15

        if self.start_date and self.end_date:
            params["start_date"] = self.start_date
            params["end_date"] = self.end_date

        # Add variables for each data period
        if self.hourly_variables:
            params["hourly"] = ",".join(self.hourly_variables)
        if self.daily_variables:
            params["daily"] = ",".join(self.daily_variables)
        if self.current_variables:
            params["current"] = ",".join(self.current_variables)
        if self.minutely_15_variables:
            params["minutely_15"] = ",".join(self.minutely_15_variables)

        responses = self.openmeteo.weather_api(url, params=params)

        results = []
        for response in responses:
            result = {
                "model": response.Model(),
                "coordinates": {
                    "latitude": response.Latitude(),
                    "longitude": response.Longitude()
                },
                "elevation": response.Elevation(),
                "timezone": response.Timezone(),
                "timezone_abbreviation": response.TimezoneAbbreviation(),
                "utc_offset_seconds": response.UtcOffsetSeconds()
            }

            # Process each data period
            if self.hourly_variables:
                result["hourly"] = self._process_hourly(response, self.hourly_variables)
            if self.daily_variables:
                result["daily"] = self._process_daily(response, self.daily_variables)
            if self.current_variables:
                result["current"] = self._process_current(response, self.current_variables)
            if self.minutely_15_variables:
                result["minutely_15"] = self._process_minutely_15(response, self.minutely_15_variables)

            results.append(result)

        return results
    
    def _process_hourly(self, response, variables: List[str]) -> pd.DataFrame:
        """Process hourly weather data."""
        hourly = response.Hourly()
        
        hourly_data = {
            "date": pd.date_range(
                start=pd.to_datetime(hourly.Time() + response.UtcOffsetSeconds(), unit="s", utc=True),
                end=pd.to_datetime(hourly.TimeEnd() + response.UtcOffsetSeconds(), unit="s", utc=True),
                freq=pd.Timedelta(seconds=hourly.Interval()),
                inclusive="left"
            )
        }
        
        for i, var in enumerate(variables):
            hourly_data[var] = hourly.Variables(i).ValuesAsNumpy()
        
        return pd.DataFrame(data=hourly_data)
    
    def _process_daily(self, response, variables: List[str]) -> pd.DataFrame:
        """Process daily weather data."""
        daily = response.Daily()
        
        daily_data = {
            "date": pd.date_range(
                start=pd.to_datetime(daily.Time() + response.UtcOffsetSeconds(), unit="s", utc=True),
                end=pd.to_datetime(daily.TimeEnd() + response.UtcOffsetSeconds(), unit="s", utc=True),
                freq=pd.Timedelta(seconds=daily.Interval()),
                inclusive="left"
            )
        }
        
        for i, var in enumerate(variables):
            daily_data[var] = daily.Variables(i).ValuesAsNumpy()
        
        return pd.DataFrame(data=daily_data)

    def _process_minutely_15(self, response, variables: List[str]) -> pd.DataFrame:
        """Process 15-minutely weather data."""
        minutely_15 = response.Minutely15()
        
        minutely_data = {
            "date": pd.date_range(
                start=pd.to_datetime(minutely_15.Time() + response.UtcOffsetSeconds(), unit="s", utc=True),
                end=pd.to_datetime(minutely_15.TimeEnd() + response.UtcOffsetSeconds(), unit="s", utc=True),
                freq=pd.Timedelta(seconds=minutely_15.Interval()),
                inclusive="left"
            )
        }
        
        for i, var in enumerate(variables):
            minutely_data[var] = minutely_15.Variables(i).ValuesAsNumpy()
        
        return pd.DataFrame(data=minutely_data)
    
    def _process_current(self, response, variables: List[str]) -> Dict[str, Any]:
        """Process current weather data."""
        current = response.Current()
        
        result = {"time": current.Time()}
        
        for i, var in enumerate(variables):
            result[var] = current.Variables(i).Value()
        
        return result
