from mcp.server.fastmcp import FastMCP
import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry
from geopy.geocoders import Nominatim

mcp = FastMCP("Weather")

# Setup Open-Meteo client
session = retry(requests_cache.CachedSession('.cache', expire_after=3600), retries=3, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=session)

# Setup geocoder
geolocator = Nominatim(user_agent="simple_weather_agent")

@mcp.tool()
async def get_weather(location: str) -> str:
    """Get current temperature for a location."""
    try:
        loc = geolocator.geocode(location)
        if not loc:
            return f"Could not find location '{location}'"

        latitude, longitude = loc.latitude, loc.longitude
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "hourly": "temperature_2m",
            "timezone": "auto"
        }

        response = openmeteo.weather_api(url, params=params)[0]
        hourly = response.Hourly()
        temps = hourly.Variables(0).ValuesAsNumpy()
        times = pd.date_range(
            start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
            end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=hourly.Interval()),
            inclusive="left"
        )

        now = pd.Timestamp.utcnow().floor("H")
        idx = times.get_indexer([now], method="nearest")[0]
        current_temp = temps[idx]

        return f"The current temperature in {location} is {current_temp:.1f}°C"

    except Exception as e:
        return f"Failed to fetch weather: {str(e)}"

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
