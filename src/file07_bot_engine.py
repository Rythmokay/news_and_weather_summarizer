from datetime import datetime
from typing import List, Dict, Any
from src.file02_weather_service import fetch_city_weather
from src.file03_news_service import fetch_news
from src.file04_ollama_service import is_ollama_running, generate_ollama_completion
from src.file05_gemini_service import generate_gemini_completion

# -----------------------------------------------------------------------------
# FUNCTION: answer_bot_query
# PURPOSE: Answers chatbot user queries using target city's real-time local timezone & weather
# -----------------------------------------------------------------------------
def answer_bot_query(
    user_question_text: str,
    target_city_name: str = "London",
    selected_news_category: str = "World",
    selected_ai_engine: str = "Built-in NLP (Free)",
    selected_ollama_model_name: str = "",
    gemini_api_key_string: str = ""
) -> str:
    # Fetch live weather context and city local time
    city_weather_information = fetch_city_weather(target_city_name)
    if city_weather_information:
        weather_context_text = city_weather_information["summary_text"]
        city_local_time_string = city_weather_information["city_local_time"]
    else:
        weather_context_text = f"Weather unavailable for {target_city_name}."
        city_local_time_string = datetime.now().strftime("%A, %B %d, %Y - %I:%M %p")
    
    # Fetch live news context
    latest_news_articles_list = fetch_news(selected_news_category, limit=5)
    news_context_text = "\n".join([f"- {article['title']} ({article['source']})" for article in latest_news_articles_list])

    # Construct System Prompt & Full Context Prompt
    ai_system_instructions = (
        f"Target City: {target_city_name}. Local Time in {target_city_name}: {city_local_time_string}.\n"
        f"Current Weather in {target_city_name}: {weather_context_text}.\n"
        f"Top {selected_news_category} News:\n{news_context_text}"
    )
    complete_ai_prompt = f"{ai_system_instructions}\n\nUser Question: {user_question_text}\nAnswer:"

    # 1. Try Gemini API if selected
    if selected_ai_engine == "✨ Gemini API":
        gemini_bot_reply = generate_gemini_completion(complete_ai_prompt, user_gemini_api_key=gemini_api_key_string)
        if gemini_bot_reply:
            return gemini_bot_reply

    # 2. Try Ollama if selected and server is running
    if selected_ai_engine == "🤖 Local LLM (Ollama)" and selected_ollama_model_name and is_ollama_running():
        ollama_bot_reply = generate_ollama_completion(user_question_text, target_ollama_model_name=selected_ollama_model_name, system_instructions_prompt=ai_system_instructions)
        if ollama_bot_reply:
            return ollama_bot_reply

    # 3. Rule-based Fallback Response if AI engine is offline or using Built-in NLP
    user_question_in_lowercase = user_question_text.lower()
    if "time" in user_question_in_lowercase or "date" in user_question_in_lowercase:
        return f"📅 **Current Local Time in {target_city_name}**: {city_local_time_string}"
    elif "weather" in user_question_in_lowercase or "rain" in user_question_in_lowercase or "temp" in user_question_in_lowercase:
        return f"🌤️ **Weather in {target_city_name}** ({city_local_time_string}):\n{weather_context_text}"
    elif "news" in user_question_in_lowercase or "headline" in user_question_in_lowercase:
        return f"📰 **Top {selected_news_category} Headlines** ({city_local_time_string}):\n{news_context_text}"
    else:
        top_article_title = latest_news_articles_list[0]['title'] if latest_news_articles_list else 'N/A'
        return f"👋 Hello! Current local time in **{target_city_name}** is **{city_local_time_string}**.\n\n• **Weather**: {weather_context_text}\n• **Top Story**: {top_article_title}"
