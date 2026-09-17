import os
from dotenv import load_dotenv

# -----------------------------------------------------------------------------
# FUNCTION: load_environment_variables
# PURPOSE: Loads environment configuration settings from the local .env file.
# -----------------------------------------------------------------------------
load_dotenv()

# Beginner-Friendly Environment Variable Definitions
gemini_api_key_from_env = os.getenv("GEMINI_API_KEY", "").strip()
ollama_server_url = os.getenv("OLLAMA_HOST", "http://localhost:11434").strip()
default_city_name = os.getenv("DEFAULT_CITY", "London").strip()
default_news_category_name = os.getenv("DEFAULT_NEWS_CATEGORY", "World").strip()
