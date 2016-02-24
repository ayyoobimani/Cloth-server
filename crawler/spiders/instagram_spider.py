from scrapy.contrib.spiders import CrawlSpider
from scrapy.http.request import Request
from crawler.items import HiClothItem
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
import urllib2
import json
import time
import re


class MainSpider(CrawlSpider):
    name = "instagramSpider"

    def __init__(self, time=0):
        infoFile = open("info.txt", "r")
        client_id = infoFile.readline().split()[1]
        userLines = infoFile.read().splitlines()
        users = [line.split()[0] for line in userLines]
        user_urls = ['https://api.instagram.com/v1/users/search?q='+user +
                     '&client_id='+client_id for user in users]
        self.start_urls = []
        self.userIDs = []
        for userURL in user_urls:
            userURLResponse = urllib2.urlopen(userURL)
            responseDict = json.load(userURLResponse)
            self.start_urls.append("https://api.instagram.com/v1/users/" +
                              responseDict["data"][0]["id"] +
                              "/media/recent/?client_id=" + client_id)
            self.userIDs.append(responseDict["data"][0]["id"].split('-')[-1])

        rules = []
        self.time = time
        self.urlTags = dict(zip(self.userIDs, [line.split()[1] for line in userLines]))
        print self.urlTags
        with open("time.txt", "r") as finalCrawlTimeFile:
            self.finalCrawlTime = float(finalCrawlTimeFile.read())
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def parse(self, response):
        readableResponse = json.loads(response.body_as_unicode())
        nextURL = readableResponse['pagination'].get('next_url')

        with open("nextURLs.txt", "a") as inputFile:
            inputFile.write(nextURL + "\n")

        item = HiClothItem()
        item["created_time"] = [readableResponse['data'][i]["created_time"]
                                for i in range(len(readableResponse['data']))]
        item["image_urls"] = [readableResponse['data'][i]
                              ['images']['standard_resolution']['url'] for i in
                              range(len(readableResponse['data']))]
        item["tags"] = self.urlTags[re.findall(r'[\d]+', response.url)[1]]
        finalNewImageIndex = None
        if self.time:
            for timeStamp in item["created_time"]:
                if int(timeStamp) < self.finalCrawlTime:
                    finalNewImageIndex = item["created_time"].index(timeStamp)
                    break
        yield HiClothItem({key: item[key][0:finalNewImageIndex] for key in item.keys()})
        if nextURL and (finalNewImageIndex is None):
            yield Request(nextURL, callback=self.parse)

    def spider_closed(self):
        with open("time.txt", "w") as newCrawlTimeFile:
            newCrawlTimeFile.write(str(time.time() + 24*60*60 ))