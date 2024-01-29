from celery import shared_task
from aggregator import rss_feeds
from aggregator import parse_feed as parse_feed_func
from aggregator import get_all_articles
from aggregator import rss_feeds

@shared_task
def parse_feed(url):
    articles = parse_feed_func(url)

    for article in articles:
        # Generate a unique hash for the article
        article_hash = hashlib.sha256(article['title'].encode('utf-8')).hexdigest()

        # Check if the article is already in the database
        cursor.execute("SELECT * FROM articles WHERE title = ? AND source_url = ?", (article['title'], article['source_url']))
        existing_article = cursor.fetchone()

        # If the article is not in the database, insert it
        if existing_article is None:
            cursor.execute('''
                INSERT INTO articles (title, content, published_date, source_url, feed_url)
                VALUES (?, ?, ?, ?, ?)
            ''', (article['title'], article['content'], article['published_date'], article['source_url'], url))

    # Commit the changes
    conn.commit()

@shared_task
def process_article(article_metadata):
    # Classify the article into a category
    category = classify_article(article_metadata['content'])

    # Insert the article into the database
    cursor.execute('''
        INSERT INTO articles (title, content, published_date, source_url, feed_url, category)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (article_metadata['title'], article_metadata['content'], article_metadata['published_date'], article_metadata['source_url'], article_metadata['feed_url'], category))
    conn.commit()

@shared_task
def get_all_articles_task():
    articles = get_all_articles()
    return [
        {
            'id': article[0],
            'title': article[1],
            'content': article[2],
            'published_date': article[3],
            'source_url': article[4],
            'feed_url': article[5],
            'category': article[6]
        }
        for article in articles
    ]