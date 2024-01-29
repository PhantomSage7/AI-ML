from bs4 import BeautifulSoup
import requests

import feedparser
import sqlite3
import hashlib

# List of RSS feeds
rss_feeds = [
    "http://rss.cnn.com/rss/cnn_topstories.rss",
    "http://qz.com/feed",
    "http://feeds.foxnews.com/foxnews/politics",
    "http://feeds.reuters.com/reuters/businessNews",
    "http://feeds.feedburner.com/NewshourWorld",
    "https://feeds.bbci.co.uk/news/world/asia/india/rss.xml"
]

def get_all_articles():
    conn = sqlite3.connect('news.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM articles')
    articles = cursor.fetchall()
    conn.close()
    return articles

# Function to parse a feed and extract relevant information
def parse_feed(url):
    try:
        feed = feedparser.parse(url)
    except Exception as e:
        print(f"Error parsing feed: {url} - {str(e)}")
        return []

    articles = []
    seen_articles = set()

    for entry in feed.entries:
        # Generate a unique hash for the article
        article_hash = hashlib.sha256(entry.title.encode('utf-8')).hexdigest()

        # Skip duplicate articles
        if article_hash in seen_articles:
            continue

        # Add the article to the list
        articles.append({
            'title': entry.title,
            'content': entry.get('summary', entry.get('content', '')),
            'published_date': entry.get('published', entry.get('updated', '')),
            'source_url': entry.link
        })

        # Add the hash to the set of seen articles
        seen_articles.add(article_hash)

    print(f"Parsed {len(articles)} articles from {url}")
    return articles

# Parse all feeds and print the extracted information
# for url in rss_feeds:
#     articles = parse_feed(url)
#     print(f"Parsed {len(articles)} articles from {url}")
#
#     for article in articles:
#         print(f"Title: {article['title']}")
#         print(f"Content: {article['content']}")
#         print(f"Published Date: {article['published_date']}")
#         print(f"Source URL: {article['source_url']}")
#         print("")