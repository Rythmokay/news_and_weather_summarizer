import requests
from typing import List, Optional
from src.file01_config import ollama_server_url

# -----------------------------------------------------------------------------
# FUNCTION: is_ollama_running
# PURPOSE: Checks if the local Ollama API server is active and online
# OUTPUT: True if active, False if offline
# -----------------------------------------------------------------------------
def is_ollama_running() -> bool:
    try:
        ollama_api_status_response = requests.get(f"{ollama_server_url}/api/tags", timeout=2)
        return ollama_api_status_response.status_code == 200
    except Exception:
        return False

# -----------------------------------------------------------------------------
# FUNCTION: get_installed_models
# PURPOSE: Retrieves the list of model names installed on the local Ollama server
# OUTPUT: List of model strings (e.g. ['llama3.2:3b', 'mistral', 'gemma2'])
# -----------------------------------------------------------------------------
def get_installed_models() -> List[str]:
    try:
        installed_models_response = requests.get(f"{ollama_server_url}/api/tags", timeout=3)
        if installed_models_response.status_code == 200:
            installed_models_data = installed_models_response.json().get("models", [])
            return [model_item["name"] for model_item in installed_models_data]
    except Exception:
        pass
    return []

# -----------------------------------------------------------------------------
# FUNCTION: generate_ollama_completion
# PURPOSE: Sends prompt to local Ollama model to generate AI completions
# INPUT: user_prompt_text (str), target_ollama_model_name (str), system_instructions_prompt (str)
# OUTPUT: Generated completion string or None
# -----------------------------------------------------------------------------
def generate_ollama_completion(
    user_prompt_text: str,
    target_ollama_model_name: str,
    system_instructions_prompt: str = ""
) -> Optional[str]:
    ollama_generation_url = f"{ollama_server_url}/api/generate"
    ollama_request_payload = {
        "model": target_ollama_model_name,
        "prompt": user_prompt_text,
        "system": system_instructions_prompt,
        "stream": False
    }
    try:
        ollama_generation_response = requests.post(ollama_generation_url, json=ollama_request_payload, timeout=60)
        if ollama_generation_response.status_code == 200:
            return ollama_generation_response.json().get("response", "").strip()
    except Exception as error_exception:
        print(f"Ollama API Error: {error_exception}")
    return None
