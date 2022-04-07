# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field
from itemloaders.processors import TakeFirst, MapCompose

def strip_n(element):
    if element:
        return element.replace('\n' , '')
    return element

class IrasutoyaItem(Item):
    image_urls = Field()
    image_titles = Field( output_processor = TakeFirst() )
    directory_name = Field( output_processor = TakeFirst() )
    page_title = Field( input_processor = MapCompose(strip_n) )