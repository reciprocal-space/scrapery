# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from scrapy.loader import ItemLoader
from services.db.models import PitchForkReviewModel
import logging
import os

class ScraperPipeline:
    def __init__(self):
        logging.error('msg')
        self.model = PitchForkReviewModel()

    def process_item(self, item, spider):
        # TODO: uppercase or lowercase alphanumeric characters to simplify comparisons
        # TODO: remove references to pitchfork in column names for reviews/authors and add source column to identify where the review is from
        self.model.load(item)

        if not self.model.album:
            raise DropItem('Missing album in {item}')
        if not self.model.genres:
            raise DropItem('Missing genres in {item}')
        if not self.model.link:
            raise DropItem('Missing link in {item}')
        if not self.model.author:
            raise DropItem('Missing author in {item}')
        if not self.model.reviewedAt:
            raise DropItem('Missing reviewed_at in {item}')

        # TODO: add idempotency check to see if we've saved review before

        self.saveItem()

    def saveItem(self):
        self.model.save()
