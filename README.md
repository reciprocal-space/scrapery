# Scrapery
Scrapery is Celery + Scrapy lovechild to scrape data from the web in a scalable, distributed manner.


## Architecture

## Installation

The following steps work for MacOS; feel free to message me if you need steps for a different operating system

1. Install Python (3.11)
```       brew install python@3.11```
2. Create a virtual environment for the project
```       virtualenv venv --python=python3.11```
2. Activate the environment
```       source venv/bin/activate```
3. Install the Python dependencies
```       pip install -r requirements.txt```
4. Install Redis
```       brew install Redis```

## Running the web scaper

Use the following steps to run the webscraper
1. Start Redis
``` redis-server ```
2. Run the Celery task-queue to start scraping
``` 
