# 🌤️ Weather & News Bot Summarizer (Beginner-Friendly & Numbered Files)

A beginner-friendly, sequentially numbered **Python & Streamlit** project for daily weather forecasts, live RSS news summaries, and an AI chatbot.

---

## 📂 Sequentially Numbered File Architecture

All project files are sequentially numbered (`file01_` through `file12_`) so they appear in exact logical execution order:

| File Name | Description | Purpose |
| :--- | :--- | :--- |
| **`app.py`** | Main Entry Point | Streamlit page config & view loader (~35 lines) |
| **`src/file01_config.py`** | Config Loader | Loads `.env` environment variables using `python-dotenv` |
| **`src/file02_weather_service.py`** | Weather API | Fetches weather & 7-day forecast from Open-Meteo |
| **`src/file03_news_service.py`** | News Parser | Fetches Google News RSS feeds across categories |
| **`src/file04_ollama_service.py`** | Local LLM Client | Communicates with local Ollama (`http://localhost:11434`) |
| **`src/file05_gemini_service.py`** | Gemini API Client | Communicates with Google Gemini REST API |
| **`src/file06_summarizer.py`** | AI Router | Routes summarizations to Gemini, Ollama, or NLP |
| **`src/file07_bot_engine.py`** | Chatbot Engine | Injects real-time context into AI chatbot responses |
| **`src/file08_sidebar_view.py`** | Sidebar Component | Renders AI engine choices & preference controls |
| **`src/file09_briefing_view.py`** | Briefing Component | Renders the Daily Briefing tab UI |
| **`src/file10_weather_view.py`** | Weather Component | Renders the Live Weather metrics tab UI |
| **`src/file11_news_view.py`** | News Component | Renders the Top News cards tab UI |
| **`src/file12_chat_view.py`** | Chatbot Component | Renders the AI Assistant Chat interface tab UI |

---

## 🎓 Beginner-Friendly Code Standards Applied

1. **Descriptive Variable Names**: Every variable uses clear names like `current_temperature_celsius`, `fetched_news_articles_list`, `user_question_text`, and `human_readable_weather_summary`.
2. **Line-by-Line Function Comments**: Every function starts with a header block describing its **purpose**, **inputs**, and **outputs**.
3. **Commented `requirements.txt`**: Each dependency is commented explaining what it does.
4. **Environment Secret Management (`.env`)**: Secret keys like `GEMINI_API_KEY` are kept safely out of source code.

---

## 🚀 Quick Start Guide

```bash
# 1. Navigate to directory & activate environment
cd proj
source .venv/bin/activate

# 2. Run Streamlit web app
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser!
