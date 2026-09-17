import feedparser
from bs4 import BeautifulSoup
import re
from typing import List, Dict, Any, Optional

# Map category names to their respective Google News RSS feed URLs
news_category_urls = {
    "World": "https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en",
    "Technology": "https://news.google.com/rss/headlines/section/topic/TECHNOLOGY?hl=en-US&gl=US&ceid=US:en",
    "Business": "https://news.google.com/rss/headlines/section/topic/BUSINESS?hl=en-US&gl=US&ceid=US:en",
    "Science": "https://news.google.com/rss/headlines/section/topic/SCIENCE?hl=en-US&gl=US&ceid=US:en",
    "Sports": "https://news.google.com/rss/headlines/section/topic/SPORTS?hl=en-US&gl=US&ceid=US:en",
}

# -----------------------------------------------------------------------------
# FUNCTION: clean_html_text
# PURPOSE: Strips HTML tags and cleans up whitespace from RSS news descriptions
# INPUT: raw_html_content (str) -> HTML string from RSS feed
# OUTPUT: Clean plain text string
# -----------------------------------------------------------------------------
def clean_html_text(raw_html_content: str) -> str:
    if not raw_html_content:
        return ""
    beautiful_soup_parser = BeautifulSoup(raw_html_content, "html.parser")
    cleaned_text_without_html = re.sub(r'\s+', ' ', beautiful_soup_parser.get_text()).strip()
    return cleaned_text_without_html

# -----------------------------------------------------------------------------
# FUNCTION: fetch_news
# PURPOSE: Fetches the top news articles for a selected category from Google News RSS
# INPUT: selected_news_category (str), limit / article_fetch_limit (int)
# OUTPUT: List of dictionaries containing title, snippet, source, publication date, and link
# -----------------------------------------------------------------------------
def fetch_news(
    selected_news_category: str = "World", 
    limit: int = 6, 
    article_fetch_limit: Optional[int] = None
) -> List[Dict[str, Any]]:
    # Use article_fetch_limit if provided, otherwise fallback to limit
    max_articles_to_fetch = article_fetch_limit if article_fetch_limit is not None else limit
    
    rss_feed_url = news_category_urls.get(selected_news_category, news_category_urls["World"])
    parsed_rss_feed = feedparser.parse(rss_feed_url)
    
    fetched_articles_list = []
    for feed_entry_item in parsed_rss_feed.entries[:max_articles_to_fetch]:
        article_title_text = clean_html_text(feed_entry_item.get("title", ""))
        article_snippet_text = clean_html_text(feed_entry_item.get("summary", article_title_text))
        article_source_name = feed_entry_item.get("source", {}).get("title", "Google News")
        article_publication_date = feed_entry_item.get("published", "Recently")
        article_web_link = feed_entry_item.get("link", "#")

        fetched_articles_list.append({
            "title": article_title_text,
            "snippet": article_snippet_text,
            "source": article_source_name,
            "published": article_publication_date,
            "link": article_web_link
        })
        
    return fetched_articles_list
