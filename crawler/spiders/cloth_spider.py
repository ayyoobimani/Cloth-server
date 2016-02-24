from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy import Selector
from crawler.items import HiClothItem


class MainSpider(CrawlSpider):
    name = "clothSpider"
    start_urls = ["http://modelhani1.blogfa.com", ]
    rules = [Rule(SgmlLinkExtractor(allow=[r'/post/\d+/[\w\W]+']),
                  callback='parse_news', follow=True), ]

    def parse_news(self, response):
        hxs = Selector(response)
        item = HiClothItem()
        imageQuery = "//div[@class='Clear center-mian-bg']//img/@src"
        item["image_urls"] = hxs.xpath(imageQuery).extract()

        tagsQuery = "//div[@class='content']/h5/b/following-sibling::node()"
        item["tags"] = hxs.xpath(tagsQuery).extract()[0].strip()

        return item