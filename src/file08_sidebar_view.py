import streamlit as st
from src.file01_config import default_city_name, default_news_category_name, gemini_api_key_from_env
from src.file04_ollama_service import is_ollama_running, get_installed_models

# -----------------------------------------------------------------------------
# FUNCTION: render_sidebar
# PURPOSE: Renders sidebar input controls and returns user configuration dictionary
# OUTPUT: Dictionary containing engine choice, ollama model, gemini key, city name, and category
# -----------------------------------------------------------------------------
def render_sidebar() -> dict:
    with st.sidebar:
        st.header("⚙️ AI Engine Setup")
        
        chosen_ai_engine = st.radio(
            "Choose AI Engine:",
            ["🤖 Local LLM (Ollama)", "✨ Gemini API", "⚡ Built-in NLP (Free)"]
        )
        
        chosen_ollama_model = ""
        entered_gemini_key = ""
        
        if chosen_ai_engine == "🤖 Local LLM (Ollama)":
            if is_ollama_running():
                available_model_names_list = get_installed_models()
                if available_model_names_list:
                    chosen_ollama_model = st.selectbox("Select Ollama Model:", available_model_names_list)
                else:
                    st.warning("No local models found! Run `ollama pull llama3` in terminal.")
            else:
                st.error("Ollama server is offline! Start it with `ollama serve` or select another engine.")

        elif chosen_ai_engine == "✨ Gemini API":
            default_gemini_key_value = gemini_api_key_from_env if gemini_api_key_from_env else ""
            entered_gemini_key = st.text_input(
                "Enter Gemini API Key:",
                value=default_gemini_key_value,
                type="password",
                help="Loaded automatically from .env if present. Get free key at https://aistudio.google.com"
            )

        st.markdown("---")
        st.header("📍 Preferences")
        entered_city_name = st.text_input("City Name", value=default_city_name)
        chosen_news_category = st.selectbox("News Category", ["World", "Technology", "Business", "Science", "Sports"], index=0)

    user_configuration_dictionary = {
        "engine_choice": chosen_ai_engine,
        "ollama_model": chosen_ollama_model,
        "gemini_key": entered_gemini_key,
        "city_name": entered_city_name,
        "news_category": chosen_news_category
    }
    
    return user_configuration_dictionary
