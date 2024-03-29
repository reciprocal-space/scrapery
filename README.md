# Scrapery
Scrapery is Celery + Scrapy lovechild to scrape data from the web in a scalable, distributed manner. Currently it is directed at scraping metadata for album reviews from Pitchfork, but extending this to other domains should be as simple as defining new models and pipelines.

There is also a GraphQL api to query the scraped data.


## Architecture

## Installation

The following steps work for MacOS; feel free to message me if you need steps for a different operating system

1. Install Python (3.11)
```
brew install python@3.11
```
2. Create a virtual environment for the project
```
virtualenv venv --python=python3.11
```
2. Activate the environment
```
source venv/bin/activate
```
3. Install the Python dependencies
```
pip install -r requirements.txt
```
4. Install Redis
```
brew install Redis
```
5. Setup the database
```
python utils/create-db.py
```

## Running the web scaper

Use the following steps to run the webscraper
1. Start Redis
```
redis-server
```
2. Run the Celery task-queue to start scraping
```
celery --workdir src -A crawler worker -B -l ERROR
```

NB: This scraper does not respect robots.txt, and is configured to run once daily

## Running the API

Start the graphql server
```python src/app.py```

The graphql playground is available at `http://localhost:8080/graphql`

## Accessing the database

The application relies on a sqlite database found at `src/services/db/storage/music.db`; it can be accessed with the following command from a terminal:
```
sqlite3 src/services/db/storage/music.db
```
Schema:

![music](https://user-images.githubusercontent.com/19412227/224117571-6d1ea250-4a1f-47c8-a025-9a959b5da1f4.png)
