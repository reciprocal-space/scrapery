import sys
from services.scheduler.task import bootstrapScheduler
from scrapy.crawler import CrawlerProcess
from services.scraper.spiders.spider import PitchforkAlbumsSpider
from celery import shared_task
from scrapy.utils.project import get_project_settings

app = bootstrapScheduler()

@shared_task
def crawl():
    process = CrawlerProcess(get_project_settings())
    process.crawl(PitchforkAlbumsSpider)
    process.start(False)

@app.on_after_configure.connect
def setupPeriodicCrawl(sender, **kwargs):
    sender.add_periodic_task(10, crawl.s(), name='Crawl Pitchfork album reviews periodically')