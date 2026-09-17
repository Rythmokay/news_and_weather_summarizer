import requests
from datetime import datetime
from zoneinfo import ZoneInfo
from typing import Dict, Any, Optional

# Dictionary mapping weather condition codes to descriptive names and emojis
weather_code_emojis = {
    0: ("Clear Sky", "☀️"),
    1: ("Mainly Clear", "🌤️"),
    2: ("Partly Cloudy", "⛅"),
    3: ("Overcast", "☁️"),
    61: ("Slight Rain", "🌧️"),
    63: ("Moderate Rain", "🌧️"),
    95: ("Thunderstorm", "🌩️")
}

# -----------------------------------------------------------------------------
# FUNCTION: fetch_city_weather
# PURPOSE: Fetches real-time weather metrics, 7-day forecast, and local time for any city
# INPUT: target_city_name (str) -> e.g. "London", "Tokyo", "New York"
# OUTPUT: Dictionary containing weather data and target city local time
# -----------------------------------------------------------------------------
def fetch_city_weather(target_city_name: str) -> Optional[Dict[str, Any]]:
    try:
        # STEP 1: Convert City Name to Coordinates and Timezone using Open-Meteo Geocoding API
        geocoding_api_url = f"https://geocoding-api.open-meteo.com/v1/search?name={target_city_name}&count=1&language=en&format=json"
        geocoding_response_json = requests.get(geocoding_api_url, timeout=5).json()
        
        # If city name was not found by geocoding API, return None
        if not geocoding_response_json.get("results"):
            return None
        
        # Extract location coordinates, timezone name, and display name
        location_data = geocoding_response_json["results"][0]
        city_latitude = location_data["latitude"]
        city_longitude = location_data["longitude"]
        city_timezone_name = location_data.get("timezone", "UTC")
        formatted_city_display_name = f"{location_data['name']}, {location_data.get('country', '')}"

        # STEP 2: Calculate City Local Date and Time using timezone
        try:
            target_city_timezone = ZoneInfo(city_timezone_name)
            city_local_datetime = datetime.now(target_city_timezone)
        except Exception:
            city_local_datetime = datetime.now()
            
        city_local_time_string = city_local_datetime.strftime("%A, %B %d, %Y | 🕒 %I:%M %p (%Z)")

        # STEP 3: Fetch Current Weather & 7-Day Forecast Data using Coordinates
        forecast_api_url = (
            f"https://api.open-meteo.com/v1/forecast?latitude={city_latitude}&longitude={city_longitude}"
            f"&current_weather=true&daily=temperature_2m_max,temperature_2m_min,precipitation_sum&timezone=auto"
        )
        weather_response_json = requests.get(forecast_api_url, timeout=5).json()
        
        # Extract current weather values
        current_weather_data = weather_response_json.get("current_weather", {})
        daily_forecast_data = weather_response_json.get("daily", {})
        
        weather_code = current_weather_data.get("weathercode", 0)
        weather_condition_text, weather_emoji = weather_code_emojis.get(weather_code, ("Cloudy/Fair", "🌤️"))
        
        current_temperature_celsius = current_weather_data.get("temperature", 0.0)
        wind_speed_kmh = current_weather_data.get("windspeed", 0.0)
        daily_high_temperature = daily_forecast_data.get("temperature_2m_max", [current_temperature_celsius])[0]
        daily_low_temperature = daily_forecast_data.get("temperature_2m_min", [current_temperature_celsius])[0]
        precipitation_amount_mm = daily_forecast_data.get("precipitation_sum", [0.0])[0]

        # STEP 4: Format Human-Readable Weather Summary Sentence
        human_readable_weather_summary = (
            f"Weather in {formatted_city_display_name} (Local Time: {city_local_time_string}): "
            f"{current_temperature_celsius}°C {weather_emoji} ({weather_condition_text}). "
            f"High: {daily_high_temperature}°C, Low: {daily_low_temperature}°C, Wind: {wind_speed_kmh} km/h, Rainfall: {precipitation_amount_mm} mm."
        )

        return {
            "city_display": formatted_city_display_name,
            "city_timezone": city_timezone_name,
            "city_local_time": city_local_time_string,
            "temp": current_temperature_celsius,
            "condition": weather_condition_text,
            "emoji": weather_emoji,
            "temp_max": daily_high_temperature,
            "temp_min": daily_low_temperature,
            "wind": wind_speed_kmh,
            "precip": precipitation_amount_mm,
            "summary_text": human_readable_weather_summary,
            "daily": daily_forecast_data
        }
    except Exception as error_exception:
        print(f"Weather Fetch Error: {error_exception}")
        return None
