import requests
from typing import Optional
from src.file01_config import gemini_api_key_from_env

# -----------------------------------------------------------------------------
# FUNCTION: generate_gemini_completion
# PURPOSE: Sends prompt to Google Gemini REST API to generate AI completions
# INPUT: input_prompt_text (str), user_gemini_api_key (str), model_name (str)
# OUTPUT: Generated text response string or error message
# -----------------------------------------------------------------------------
def generate_gemini_completion(
    input_prompt_text: str,
    user_gemini_api_key: str = "",
    model_name: str = "gemini-1.5-flash"
) -> Optional[str]:
    # Use user provided API key or fallback to environment variable from .env
    active_gemini_api_key = user_gemini_api_key.strip() if user_gemini_api_key else gemini_api_key_from_env
    
    if not active_gemini_api_key:
        return "⚠️ Gemini API key is missing. Please set GEMINI_API_KEY in .env or enter it in the sidebar."

    gemini_api_url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={active_gemini_api_key}"
    request_headers = {"Content-Type": "application/json"}
    request_payload_json = {
        "contents": [
            {"parts": [{"text": input_prompt_text}]}
        ]
    }

    try:
        gemini_http_response = requests.post(gemini_api_url, json=request_payload_json, headers=request_headers, timeout=30)
        if gemini_http_response.status_code == 200:
            response_data_json = gemini_http_response.json()
            candidates_list = response_data_json.get("candidates", [])
            if candidates_list:
                parts_list = candidates_list[0].get("content", {}).get("parts", [])
                if parts_list:
                    return parts_list[0].get("text", "").strip()
        else:
            return f"⚠️ Gemini API Error (Status {gemini_http_response.status_code}): {gemini_http_response.text}"
    except Exception as error_exception:
        return f"⚠️ Connection error to Gemini API: {error_exception}"

    return None
