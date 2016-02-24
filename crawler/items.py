from scrapy.item import Item, Field


class HiClothItem(Item):
    image_urls = Field()
    images = Field()
    tags = Field()
    created_time = Field()