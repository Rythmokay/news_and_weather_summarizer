import streamlit as st
from src.file07_bot_engine import answer_bot_query

# -----------------------------------------------------------------------------
# FUNCTION: render_chat_tab
# PURPOSE: Renders the AI Assistant Chat interface in Streamlit
# INPUT: user_configuration_dictionary (dict)
# -----------------------------------------------------------------------------
def render_chat_tab(user_configuration_dictionary: dict):
    target_city_name = user_configuration_dictionary["city_name"]
    target_news_category = user_configuration_dictionary["news_category"]
    
    st.subheader("🤖 AI Assistant Chat")
    
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": f"👋 Hi! Ask me anything about weather in {target_city_name} or top {target_news_category} news!"}
        ]

    for chat_message_item in st.session_state.messages:
        with st.chat_message(chat_message_item["role"]):
            st.markdown(chat_message_item["content"])

    if user_submitted_question := st.chat_input("Ask a question (e.g. 'Should I carry an umbrella today?'):"):
        st.session_state.messages.append({"role": "user", "content": user_submitted_question})
        with st.chat_message("user"):
            st.markdown(user_submitted_question)

        with st.chat_message("assistant"):
            assistant_reply_text = answer_bot_query(
                user_question_text=user_submitted_question,
                target_city_name=target_city_name,
                selected_news_category=target_news_category,
                selected_ai_engine=user_configuration_dictionary["engine_choice"],
                selected_ollama_model_name=user_configuration_dictionary["ollama_model"],
                gemini_api_key_string=user_configuration_dictionary["gemini_key"]
            )
            st.markdown(assistant_reply_text)
            st.session_state.messages.append({"role": "assistant", "content": assistant_reply_text})
