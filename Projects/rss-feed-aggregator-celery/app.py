import sqlite3

from flask import Flask, jsonify, redirect, url_for
from database import parse_feed_and_store

app = Flask(__name__)

@app.route('/parse_feed/<url>')
def parse_feed(url):
    parse_feed_and_store.delay(url)
    return jsonify({'message': 'Parsing feed started'})

@app.route('/articles')
def get_articles():
    # Connect to the database and retrieve the articles
    conn = sqlite3.connect('news.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM articles')
    articles = cursor.fetchall()
    conn.close()

    # Format the articles as JSON and return them
    formatted_articles = []
    for article in articles:
        formatted_articles.append({
            'id': article[0],
            'title': article[1],
            'content': article[2],
            'published_date': article[3],
            'source_url': article[4],
            'feed_url': article[5],
            'category': article[6]
        })
    return jsonify(formatted_articles)

@app.route('/')
def redirect_to_articles():
    return redirect(url_for('get_articles'))

if __name__ == '__main__':
    app.run(debug=True)