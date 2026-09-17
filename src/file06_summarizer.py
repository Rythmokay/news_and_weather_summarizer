import re
from datetime import datetime
from typing import List, Dict, Any
from src.file04_ollama_service import is_ollama_running, generate_ollama_completion
from src.file05_gemini_service import generate_gemini_completion

# -----------------------------------------------------------------------------
# FUNCTION: nlp_simple_summary
# PURPOSE: Basic sentence frequency extraction (Zero-dependency fallback summarizer)
# INPUT: input_article_text (str), desired_bullet_count (int)
# OUTPUT: Formatted bullet-point text summary
# -----------------------------------------------------------------------------
def nlp_simple_summary(input_article_text: str, desired_bullet_count: int = 3) -> str:
    individual_sentence_list = re.split(r'(?<=[.!?]) +', input_article_text.strip())
    if len(individual_sentence_list) <= desired_bullet_count:
        return "\n".join([f"• {sentence_item.strip()}" for sentence_item in individual_sentence_list])
    
    selected_sentences = [
        f"• {individual_sentence_list[sentence_index].strip()}" 
        for sentence_index in range(min(desired_bullet_count, len(individual_sentence_list)))
    ]
    return "\n".join(selected_sentences)

# -----------------------------------------------------------------------------
# FUNCTION: generate_summary
# PURPOSE: Routes single-article summary tasks to Gemini API, Ollama, or Built-in NLP
# -----------------------------------------------------------------------------
def generate_summary(
    input_article_text: str,
    selected_ai_engine: str = "Built-in NLP (Free)",
    selected_ollama_model_name: str = "",
    gemini_api_key_string: str = "",
    desired_bullet_count: int = 3
) -> str:
    combined_prompt_for_ai = f"Summarize the following text into exactly {desired_bullet_count} key bullet points:\n\n{input_article_text}"

    if selected_ai_engine == "✨ Gemini API":
        gemini_response = generate_gemini_completion(combined_prompt_for_ai, user_gemini_api_key=gemini_api_key_string)
        return gemini_response or nlp_simple_summary(input_article_text, desired_bullet_count)

    elif selected_ai_engine == "🤖 Local LLM (Ollama)" and selected_ollama_model_name and is_ollama_running():
        ollama_response = generate_ollama_completion(combined_prompt_for_ai, target_ollama_model_name=selected_ollama_model_name)
        return ollama_response or nlp_simple_summary(input_article_text, desired_bullet_count)

    return nlp_simple_summary(input_article_text, desired_bullet_count)

# -----------------------------------------------------------------------------
# FUNCTION: generate_daily_briefing
# PURPOSE: Blends live weather report & RSS news headlines into an executive briefing using city local time
# -----------------------------------------------------------------------------
def generate_daily_briefing(
    human_readable_weather_summary: str,
    fetched_news_articles_list: List[Dict[str, Any]],
    city_local_time_string: str = "",
    selected_ai_engine: str = "Built-in NLP (Free)",
    selected_ollama_model_name: str = "",
    gemini_api_key_string: str = ""
) -> str:
    timestamp_to_display = city_local_time_string if city_local_time_string else datetime.now().strftime("%A, %B %d, %Y - %I:%M %p")
    top_headline_titles_string = "\n".join([f"- {article['title']} ({article['source']})" for article in fetched_news_articles_list[:5]])
    
    combined_prompt_for_ai = (
        f"Create a friendly Daily Briefing for local time: {timestamp_to_display}.\n"
        f"Include two main sections: '🌤️ Weather Brief' and '📰 News Brief'.\n\n"
        f"WEATHER DATA:\n{human_readable_weather_summary}\n\n"
        f"TOP HEADLINES:\n{top_headline_titles_string}"
    )

    if selected_ai_engine == "✨ Gemini API":
        gemini_briefing_result = generate_gemini_completion(combined_prompt_for_ai, user_gemini_api_key=gemini_api_key_string)
        if gemini_briefing_result:
            return gemini_briefing_result

    if selected_ai_engine == "🤖 Local LLM (Ollama)" and selected_ollama_model_name and is_ollama_running():
        ollama_briefing_result = generate_ollama_completion(combined_prompt_for_ai, target_ollama_model_name=selected_ollama_model_name)
        if ollama_briefing_result:
            return ollama_briefing_result

    # Fallback Briefing
    fallback_briefing_text = f"### 📅 Daily Briefing (Local City Time: {timestamp_to_display})\n\n"
    fallback_briefing_text += f"#### 🌤️ Weather Overview\n{human_readable_weather_summary}\n\n"
    fallback_briefing_text += f"#### 📰 Top Headlines\n" + nlp_simple_summary("\n".join([article['title'] for article in fetched_news_articles_list[:5]]), 4)
    return fallback_briefing_text
