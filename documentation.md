# 📘 Complete Beginner-Friendly Documentation: Weather & News Bot Summarizer

Welcome to the beginner-friendly technical documentation for **Weather & News Bot Summarizer**. This guide explains the sequential, numbered file architecture, what every function does, and how environment variables are handled.

---

## 📂 Sequentially Numbered File Structure

The project files are numbered sequentially (`01_config.py` through `12_chat_view.py`) so they appear in exact logical execution order:

```
proj/
├── .env                     # Environment variables & secrets (GEMINI_API_KEY, OLLAMA_HOST, etc.)
├── .env.example             # Example environment template file
├── requirements.txt         # Python dependencies list with comments
├── app.py                   # Main Streamlit web app entry point (~40 lines)
├── README.md                # Quick start tutorial
├── documentation.md         # Detailed code & function documentation
├── .streamlit/
│   └── config.toml          # Streamlit dark theme settings
└── src/
    ├── __init__.py          # Package initializer
    ├── 01_config.py         # Loads environment settings from .env
    ├── 02_weather_service.py # Open-Meteo REST Weather & Geocoding Service
    ├── 03_news_service.py    # Google News RSS Parser & HTML Sanitizer
    ├── 04_ollama_service.py  # Local Ollama REST Client (http://localhost:11434)
    ├── 05_gemini_service.py  # Google Gemini API REST Client
    ├── 06_summarizer.py      # AI Summarization Router
    ├── 07_bot_engine.py      # Conversational Chatbot Engine
    ├── 08_sidebar_view.py    # Sidebar Configuration UI Component
    ├── 09_briefing_view.py   # Daily Briefing Tab UI Component
    ├── 10_weather_view.py    # Live Weather Tab UI Component
    ├── 11_news_view.py       # Top News Tab UI Component
    └── 12_chat_view.py       # AI Chatbot Tab UI Component
```

---

## 📖 Module-by-Module Code Explanation

### 1️⃣ `src/01_config.py` (Configuration Loader)
- **Purpose**: Loads configuration settings from the local `.env` file using `python-dotenv`.
- **Variables**:
  - `gemini_api_key_from_env`: Gemini API key string from `.env`.
  - `ollama_server_url`: Local Ollama URL (default: `http://localhost:11434`).
  - `default_city_name`: Default target city (default: `London`).
  - `default_news_category_name`: Default news category (default: `World`).

---

### 2️⃣ `src/02_weather_service.py` (Weather Service)
- **Function**: `fetch_city_weather(target_city_name)`
  - **Step 1**: Geocodes `target_city_name` into `city_latitude` and `city_longitude` using `geocoding-api.open-meteo.com`.
  - **Step 2**: Queries `api.open-meteo.com` for `current_temperature_celsius`, `daily_high_temperature`, `daily_low_temperature`, `wind_speed_kmh`, and `precipitation_amount_mm`.
  - **Step 3**: Builds `human_readable_weather_summary` string and returns data dictionary.

---

### 3️⃣ `src/03_news_service.py` (News Service)
- **Function**: `clean_html_text(raw_html_content)`
  - Strips HTML tags using `BeautifulSoup`.
- **Function**: `fetch_news(selected_news_category, article_fetch_limit)`
  - Parses RSS feeds using `feedparser` for `World`, `Technology`, `Business`, `Science`, or `Sports`.

---

### 4️⃣ `src/04_ollama_service.py` (Ollama Service)
- **Function**: `is_ollama_running()` -> Checks if local server is online.
- **Function**: `get_installed_models()` -> Returns list of local models (e.g. `llama3.2:3b`).
- **Function**: `generate_ollama_completion(user_prompt_text, target_ollama_model_name)` -> Sends POST request to Ollama `/api/generate`.

---

### 5️⃣ `src/05_gemini_service.py` (Gemini API Service)
- **Function**: `generate_gemini_completion(input_prompt_text, user_gemini_api_key)`
  - Sends POST request directly to Google Gemini REST API (`gemini-1.5-flash`).
  - Falls back to `gemini_api_key_from_env` if no key is entered in the sidebar.

---

### 6️⃣ `src/06_summarizer.py` (Summarization Router)
- **Function**: `nlp_simple_summary(input_article_text)` -> Extractive sentence frequency summarizer.
- **Function**: `generate_summary(...)` -> Routes single-article summary requests to Gemini, Ollama, or NLP.
- **Function**: `generate_daily_briefing(...)` -> Combines weather summary & RSS headlines into an executive daily briefing.

---

### 7️⃣ `src/07_bot_engine.py` (AI Chatbot Engine)
- **Function**: `answer_bot_query(...)` -> Injects current date/time, city weather, and RSS headlines into AI prompt so the chatbot gives accurate context-grounded responses.

---

### 8️⃣ UI Views (`src/08_sidebar_view.py` to `src/12_chat_view.py`)
- `08_sidebar_view.py`: AI Engine choice radio selector, API key input, city input.
- `09_briefing_view.py`: Daily Briefing tab UI.
- `10_weather_view.py`: Live Weather metrics tab UI.
- `11_news_view.py`: Top News cards tab UI.
- `12_chat_view.py`: AI Chatbot interface tab UI.

---

## 🚀 How to Run the App

1. Activate your virtual environment:
   ```bash
   cd proj
   source .venv/bin/activate
   ```
2. Launch Streamlit:
   ```bash
   streamlit run app.py
   ```
3. Open browser at `http://localhost:8501`.
