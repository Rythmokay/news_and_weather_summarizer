import streamlit as st
from src.file02_weather_service import fetch_city_weather

# -----------------------------------------------------------------------------
# FUNCTION: render_weather_tab
# PURPOSE: Renders the Live Weather metrics tab UI in Streamlit
# INPUT: user_configuration_dictionary (dict)
# -----------------------------------------------------------------------------
def render_weather_tab(user_configuration_dictionary: dict):
    target_city_name = user_configuration_dictionary["city_name"]
    st.subheader(f"🌤️ Live Weather Hub - {target_city_name}")
    
    fetched_weather_details = fetch_city_weather(target_city_name)
    if fetched_weather_details:
        column_temperature, column_high_low, column_wind_speed, column_rainfall = st.columns(4)
        column_temperature.metric("Temperature", f"{fetched_weather_details['temp']} °C", f"{fetched_weather_details['emoji']} {fetched_weather_details['condition']}")
        column_high_low.metric("High / Low", f"{fetched_weather_details['temp_max']}° / {fetched_weather_details['temp_min']}°")
        column_wind_speed.metric("Wind Speed", f"{fetched_weather_details['wind']} km/h")
        column_rainfall.metric("Rainfall", f"{fetched_weather_details['precip']} mm")
    else:
        st.error(f"Could not find weather for '{target_city_name}'.")
