import streamlit as st
from src.file02_weather_service import fetch_city_weather
from src.file08_sidebar_view import render_sidebar
from src.file09_briefing_view import render_briefing_tab
from src.file10_weather_view import render_weather_tab
from src.file11_news_view import render_news_tab
from src.file12_chat_view import render_chat_tab

# -----------------------------------------------------------------------------
# MAIN APPLICATION ENTRY POINT
# PURPOSE: Configures Streamlit page layout, sidebar, and tab navigation
# -----------------------------------------------------------------------------
st.set_page_config(page_title="Weather & News Bot", page_icon="🌤️", layout="wide")

# STEP 1: Render Sidebar Configuration and get user settings dictionary
user_configuration_dictionary = render_sidebar()
target_city_name = user_configuration_dictionary["city_name"]

# STEP 2: Fetch Target City Local Time
weather_info = fetch_city_weather(target_city_name)
if weather_info:
    city_time_caption = f"📍 **{weather_info['city_display']}** Local Time: **{weather_info['city_local_time']}**"
else:
    city_time_caption = f"📍 Target City: **{target_city_name}**"

# STEP 3: Render Main Application Header & City Local Timestamp
st.title("🌤️ Weather & News Bot Summarizer")
st.caption(city_time_caption)

# STEP 4: Create Main Navigation Tabs
tab_briefing, tab_weather, tab_news, tab_chat = st.tabs([
    "🌅 Daily Briefing", "🌤️ Live Weather", "📰 Top News", "🤖 AI Assistant Chat"
])

# STEP 5: Render Component Views into their respective tabs
with tab_briefing:
    render_briefing_tab(user_configuration_dictionary)

with tab_weather:
    render_weather_tab(user_configuration_dictionary)

with tab_news:
    render_news_tab(user_configuration_dictionary)

with tab_chat:
    render_chat_tab(user_configuration_dictionary)
