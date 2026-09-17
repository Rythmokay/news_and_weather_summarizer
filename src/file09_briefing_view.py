import streamlit as st
from src.file02_weather_service import fetch_city_weather
from src.file03_news_service import fetch_news
from src.file06_summarizer import generate_daily_briefing

# -----------------------------------------------------------------------------
# FUNCTION: render_briefing_tab
# PURPOSE: Renders the Daily Briefing tab UI in Streamlit
# INPUT: user_configuration_dictionary (dict)
# -----------------------------------------------------------------------------
def render_briefing_tab(user_configuration_dictionary: dict):
    target_city_name = user_configuration_dictionary["city_name"]
    target_news_category = user_configuration_dictionary["news_category"]
    
    st.subheader(f"🌅 Daily Briefing for {target_city_name}")
    is_generate_button_clicked = st.button("🚀 Generate Briefing", type="primary")
    
    if is_generate_button_clicked:
        with st.spinner(f"Fetching weather for {target_city_name}, news & generating AI summary..."):
            fetched_weather_details = fetch_city_weather(target_city_name)
            if fetched_weather_details:
                weather_summary_text = fetched_weather_details["summary_text"]
                city_local_time_string = fetched_weather_details["city_local_time"]
            else:
                weather_summary_text = "Weather unavailable."
                city_local_time_string = ""

            fetched_news_articles = fetch_news(selected_news_category=target_news_category, limit=5)
            
            generated_briefing_markdown = generate_daily_briefing(
                human_readable_weather_summary=weather_summary_text,
                fetched_news_articles_list=fetched_news_articles,
                city_local_time_string=city_local_time_string,
                selected_ai_engine=user_configuration_dictionary["engine_choice"],
                selected_ollama_model_name=user_configuration_dictionary["ollama_model"],
                gemini_api_key_string=user_configuration_dictionary["gemini_key"]
            )
            st.markdown(generated_briefing_markdown)
