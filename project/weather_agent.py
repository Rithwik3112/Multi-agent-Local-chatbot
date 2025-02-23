import requests
import os

def get_weather_info():
    """Fetch weather details based on public IP location using AccuWeather API."""
    API_KEY = os.getenv("ACCUWEATHER_API_KEY", "8fSPG8oIhMCqaxIPL7Ann8N7hG6mHBzF")
    BASE_URL = "http://dataservice.accuweather.com"

    try:
        # Get coordinates from public IP
        loc_response = requests.get("https://ipinfo.io/json", timeout=5)
        loc_response.raise_for_status()
        loc_data = loc_response.json()
        loc = loc_data.get("loc", None)

        if not loc:
            return "Could not determine coordinates."

        latitude, longitude = map(float, loc.split(","))

        # Get location key
        location_url = f"{BASE_URL}/locations/v1/cities/geoposition/search"
        location_params = {"apikey": "8fSPG8oIhMCqaxIPL7Ann8N7hG6mHBzF", "q": f"{latitude},{longitude}"}
        location_response = requests.get(location_url, params=location_params, timeout=5)
        location_response.raise_for_status()
        location_data = location_response.json()
        location_key = location_data.get("Key")

        if not location_key:
            return "Could not find location key."

        # Get weather details
        weather_url = f"{BASE_URL}/currentconditions/v1/{location_key}"
        weather_params = {"apikey": "8fSPG8oIhMCqaxIPL7Ann8N7hG6mHBzF"}  # Corrected key here
        weather_response = requests.get(weather_url, params=weather_params, timeout=5)
        weather_response.raise_for_status()
        weather_data = weather_response.json()

        if weather_data:
            weather_text = weather_data[0].get("WeatherText", "Unknown")
            temperature = weather_data[0].get("Temperature", {}).get("Metric", {}).get("Value", "Unknown")
            return f"Weather: {weather_text}, Temperature: {temperature}°C"
    
    except requests.RequestException as e:
        return f"Error fetching data: {e}"

    return "Could not fetch weather."

