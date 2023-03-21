# spiders are classes that we define and that scrapy uses to scrape information from a website; they must subclass Spider and
# define the initial requests to make, they may also define how to follow links in pages, and how to parse the downloaded page content
# to extract data

from pathlib import Path
import scrapy
from scrapy.item import Item
from scrapy.selector import Selector
from itemadapter import ItemAdapter
from scrapy.loader import ItemLoader
from customtypes import PitchforkReview

class PitchforkAlbumsSpider(scrapy.Spider):
    name = 'pitchforkalbums'
    start_urls = [
        'https://pitchfork.com/reviews/albums/'
    ]
    ITEM_PIPELINES= {"scraper.pipelines.ScraperPipeline": 1}

    def __init__(self, *args, **kwargs):
        super(PitchforkAlbumsSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        html = response.css('div[class="review"]').getall()
        for text in html:
            selector = Selector(text=text)
            review = PitchforkReview(
                album=selector.css('h2[class="review__title-album"] *::text').get(),
                artists=selector.css('ul[class="artist-list review__title-artist"] *::text').getall(),
                genres=selector.css('li[class="genre-list__item"] *::text').getall(),
                link=selector.css('a[class="review__link"]::attr(href)').get(),
                meta={
                    'author': selector.css('a[class="linked display-name display-name--linked"]::text').get(),
                    'reviewed_at': selector.css('time[class="pub-date"]::attr(datetime)').get(),
                    'tag': selector.css('a[class="review__meta-bnm"]::text').get()
                })
            yield review
