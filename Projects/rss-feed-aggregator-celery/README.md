# RSS Feed Aggregator with Celery

An RSS feed aggregator that extracts articles from multiple RSS feeds and stores them in a SQLite database. This project uses Celery for asynchronous processing.

## Features

- Extracts articles from multiple RSS feeds
- Stores articles in a SQLite database
- Uses Celery for asynchronous processing

## Requirements

- Python 3.x
- Celery
- Flask
- feedparser
- BeautifulSoup4
- requests
- SQLite3

## Installation

1. Clone the repository:

git clone https://github.com/your_username/rss-feed-aggregator-celery.git


2. Create a virtual environment and activate it:

python3 -m venv venv source venv/bin/activate (for Linux/macOS) venv\Scripts\activate (for Windows)


3. Install the required packages:

pip install -r requirements.txt


4. Run the Celery worker in a separate terminal:

celery -A tasks worker --loglevel=info


5. Run the Flask app:

python app.py


6. Access the app at http://127.0.0.1:5000/

## Usage

- To parse and store all feeds, send a POST request to /parse_feed:
curl -X POST http://127.0.0.1:5000/parse_feed


- To get all articles, send a GET request to /articles:
curl http://127.0.0.1:5000/articles


## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
