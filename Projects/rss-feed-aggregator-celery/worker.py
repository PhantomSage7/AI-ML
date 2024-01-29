from celery import Celery
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from spacy.lang.en import English

app = Celery('aggregator')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

nlp = English()

@app.task
def process_article(article):
    # Tokenize the article content
    tokens = word_tokenize(article['content'])

    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [token for token in tokens if token.lower() not in stop_words]

    # Perform category classification using spaCy
    doc = nlp(' '.join(filtered_tokens))
    categories = [label.text for label in doc.ents if label.label_ == 'CATEGORY']

    # Update the database with the assigned category for each article
    for category in categories:
        cursor.execute("UPDATE articles SET category = ? WHERE id = ?", (category, article['id']))

    # Commit the changes
    conn.commit()