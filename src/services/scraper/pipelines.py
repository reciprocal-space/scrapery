# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from scrapy.loader import ItemLoader
from services.db.models.pitchfork import PitchForkReviewModel
import logging

class ScraperPipeline:
    def __init__(self):
        self.log = logging.getLogger(__name__)
        self.model = PitchForkReviewModel()

    def process_item(self, item, spider):
        try:
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

        except Exception as e:
            self.log.error(f'Something went wrong in the pipeline: {e}')

    def saveItem(self):
        self.model.save()
        self.log.info(f'Saved: {self.model.__dict__}')
