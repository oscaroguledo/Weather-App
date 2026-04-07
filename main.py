from typing import Optional, List
from datetime import datetime, timedelta
import re
import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry
from constants import DATA_PERIODS, TIMEZONES, HOURLY_VARIABLES, DAILY_VARIABLES, CURRENT_VARIABLES, WEATHER_MODELS

class WeatherApp:
    def __init__(self, 
                 variables: List[str],
                 data_period: str, 
                 forecast_period: Optional[int] = None,
                 past_days: Optional[int] = None, 
                 start_date: Optional[str] = None, 
                 end_date: Optional[str] = None,
                 latitude: Optional[float] = 52.52, 
                 longitude: Optional[float] = 13.41, 
                 timezone: Optional[str] = "auto",
                 model: Optional[str] = "best_match"):
        self.variables = variables
        self.data_period = data_period
        self.forecast_period = forecast_period
        self.past_days = past_days
        self.start_date = start_date
        self.end_date = end_date
        self.latitude = latitude
        self.longitude = longitude
        self.timezone = timezone
        self.model = model
        self.openmeteo = None
        self._setup_client()

        if self.data_period not in DATA_PERIODS:
            raise ValueError(f"Data period must be one of {DATA_PERIODS}")
        if self.timezone not in TIMEZONES:
            raise ValueError(f"Timezone must be one of {TIMEZONES}")
        if self.model not in WEATHER_MODELS:
            raise ValueError(f"Model must be one of {WEATHER_MODELS}")
        
        # Validate variables based on data period
        valid_vars = self._get_valid_variables()
        for var in self.variables:
            if var not in valid_vars:
                raise ValueError(f"Invalid variable '{var}' for {self.data_period} period. Must be one of {valid_vars}")
        
        if self.forecast_period:
            now = datetime.now()
            self.start_date = now.strftime("%Y-%m-%d")
            self.end_date = (now + timedelta(days=self.forecast_period)).strftime("%Y-%m-%d")

        if self.start_date:
            if isinstance(self.start_date, datetime):
                self.start_date = self.start_date.strftime("%Y-%m-%d")
            if not re.match(r"\d{4}-\d{2}-\d{2}", self.start_date):
                raise ValueError("Start date must be in YYYY-MM-DD format")
            if self.end_date and self.start_date > self.end_date:
                raise ValueError("Start date must be before end date")
            if not self.end_date:
                raise ValueError("End date is required when start date is provided")
            if self.forecast_period:
                raise ValueError("Forecast period cannot be used with start and end dates")
                
        
        if self.end_date:
            if isinstance(self.end_date, datetime):
                self.end_date = self.end_date.strftime("%Y-%m-%d")
            if not re.match(r"\d{4}-\d{2}-\d{2}", self.end_date):
                raise ValueError("End date must be in YYYY-MM-DD format")
            if self.start_date and self.start_date > self.end_date:
                raise ValueError("Start date must be before end date")
            if not self.start_date:
                raise ValueError("Start date is required when end date is provided")
            if self.forecast_period:
                raise ValueError("Forecast period cannot be used with start and end dates")
    
    def _get_valid_variables(self):
        """Return valid variables based on data period."""
        var_map = {
            "hourly": HOURLY_VARIABLES,
            "daily": DAILY_VARIABLES,
            "current": CURRENT_VARIABLES
        }
        return var_map.get(self.data_period, set())
    
    def _setup_client(self):
        """Setup the Open-Meteo API client with cache and retry."""
        cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
        retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
        self.openmeteo = openmeteo_requests.Client(session=retry_session)

    def get_weather(self):
        """Fetch weather data from Open-Meteo API."""
        url = "https://api.open-meteo.com/v1/forecast"
        
        # Build params based on data period
        params = {
            "latitude": self.latitude,
            "longitude": self.longitude,
            "timezone": self.timezone,
            "models": self.model
        }
        
        if self.past_days:
            params["past_days"] = self.past_days
        
        # Add variables based on data period
        if self.data_period == "hourly":
            params["hourly"] = ",".join(self.variables)
        elif self.data_period == "daily":
            params["daily"] = ",".join(self.variables)
        elif self.data_period == "current":
            params["current"] = ",".join(self.variables)
        
        responses = self.openmeteo.weather_api(url, params=params)
        response = responses[0]
        
        result = {
            "coordinates": {
                "latitude": response.Latitude(),
                "longitude": response.Longitude()
            },
            "elevation": response.Elevation(),
            "timezone": response.Timezone(),
            "timezone_abbreviation": response.TimezoneAbbreviation(),
            "utc_offset_seconds": response.UtcOffsetSeconds()
        }
        
        # Process data based on period
        if self.data_period == "hourly":
            result["data"] = self._process_hourly(response)
        elif self.data_period == "daily":
            result["data"] = self._process_daily(response)
        elif self.data_period == "current":
            result["data"] = self._process_current(response)
        
        return result
    
    def _process_hourly(self, response):
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
        
        for i, var in enumerate(self.variables):
            hourly_data[var] = hourly.Variables(i).ValuesAsNumpy()
        
        return pd.DataFrame(data=hourly_data)
    
    def _process_daily(self, response):
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
        
        for i, var in enumerate(self.variables):
            daily_data[var] = daily.Variables(i).ValuesAsNumpy()
        
        return pd.DataFrame(data=daily_data)
    
    def _process_current(self, response):
        """Process current weather data."""
        current = response.Current()
        
        result = {"time": current.Time()}
        
        for i, var in enumerate(self.variables):
            result[var] = current.Variables(i).Value()
        
        return result
