# Export all numbered views and services for clean importing
from src.file01_config import *
from src.file02_weather_service import fetch_city_weather
from src.file03_news_service import fetch_news
from src.file04_ollama_service import is_ollama_running, get_installed_models, generate_ollama_completion
from src.file05_gemini_service import generate_gemini_completion
from src.file06_summarizer import generate_summary, generate_daily_briefing
from src.file07_bot_engine import answer_bot_query
from src.file08_sidebar_view import render_sidebar
from src.file09_briefing_view import render_briefing_tab
from src.file10_weather_view import render_weather_tab
from src.file11_news_view import render_news_tab
from src.file12_chat_view import render_chat_tab
