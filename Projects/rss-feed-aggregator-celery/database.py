import sys
sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1)
import sqlite3
import hashlib
import feedparser
from aggregator import rss_feeds, parse_feed as parse_feed_func
# from tasks import parse_feed, process_article

# Connect to the database
conn = sqlite3.connect('news.db')
cursor = conn.cursor()

# Create the articles table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS articles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        content TEXT,
        published_date DATETIME,
        source_url TEXT NOT NULL,
        feed_url TEXT NOT NULL,
        category TEXT,
        UNIQUE (title, source_url)
    )
''')

# Function to parse a feed and store new articles in the database
def parse_feed_and_store(url):
    articles = parse_feed_func(url)

    for article in articles:
        # Generate a unique hash for the article
        article_hash = hashlib.sha256(article['title'].encode('utf-8')).hexdigest()

        # Check if the article is already in the database
        cursor.execute("SELECT * FROM articles WHERE title = ? AND source_url = ?", (article['title'], article.get('source_url', '')))
        existing_article = cursor.fetchone()

        # If the article is not in the database, insert it
        if existing_article is None:
            # Insert the article into the database
            cursor.execute('''
                INSERT INTO articles (title, content, published_date, source_url, feed_url, category)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (article['title'], article.get('content', ''), article.get('published_parsed', ''), article.get('source_url', ''), url, None))

            conn.commit()
            print(f"Inserted new article: {article['title']}")

# Parse and send all feeds to the Celery queue
for url in rss_feeds:
    parse_feed_and_store(url)

# Close the database connection
conn.close()