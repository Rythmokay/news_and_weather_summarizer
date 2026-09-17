import streamlit as st
from src.file03_news_service import fetch_news
from src.file06_summarizer import generate_summary

# -----------------------------------------------------------------------------
# FUNCTION: render_news_tab
# PURPOSE: Renders the Top News category stories and individual article summarizer
# INPUT: user_configuration_dictionary (dict)
# -----------------------------------------------------------------------------
def render_news_tab(user_configuration_dictionary: dict):
    target_news_category = user_configuration_dictionary["news_category"]
    st.subheader(f"📰 Top {target_news_category} Headlines")
    
    fetched_news_articles = fetch_news(selected_news_category=target_news_category, article_fetch_limit=6)
    for article_index_number, article_item in enumerate(fetched_news_articles):
        st.markdown(f"### [{article_item['title']}]({article_item['link']})")
        st.caption(f"📌 Source: {article_item['source']} | 🕒 {article_item['published']}")
        st.write(article_item['snippet'])
        
        with st.expander("✨ Summarize Article"):
            if st.button(f"Summarize Story #{article_index_number + 1}", key=f"news_btn_{article_index_number}"):
                generated_article_summary = generate_summary(
                    input_article_text=f"{article_item['title']}. {article_item['snippet']}",
                    selected_ai_engine=user_configuration_dictionary["engine_choice"],
                    selected_ollama_model_name=user_configuration_dictionary["ollama_model"],
                    gemini_api_key_string=user_configuration_dictionary["gemini_key"]
                )
                st.markdown(generated_article_summary)
        st.markdown("---")
