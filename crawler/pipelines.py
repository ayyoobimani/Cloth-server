from rest.models import *  # use django models in scrapy
import datetime


class ImagePipeline(object):
    def process_item(self, item, spider):
        print len(item["images"])

        for image in item["images"]:
            for tag in item["tags"].split('-'):
                Tag.objects.get_or_create(name=tag)
            print "I am an Image: " + image["url"]
            newImage = Image(
                URL=image["url"],
                location=image["path"],
                tags=item["tags"],
                date=datetime.datetime.fromtimestamp(float(item["created_time"]
                         [item["images"].index(image)]))
            )
            newImage.save()
        print "items completed"
        return item
