# -*- coding: utf-8 -*-

# Scrapy settings for crawler project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

import sys
import os
import django

DJANGO_ROOT = '/home/mojtaba/Documents/hisis/hicloth/hiCloth/hicloth'

sys.path.append(DJANGO_ROOT)

os.environ['DJANGO_SETTINGS_MODULE'] = 'hicloth.settings'

django.setup()


BOT_NAME = 'crawler'

SPIDER_MODULES = ['crawler.spiders']
NEWSPIDER_MODULE = 'crawler.spiders'

ITEM_PIPELINES = {'scrapy.contrib.pipeline.images.ImagesPipeline': 1,
                  'crawler.pipelines.ImagePipeline': 2,
}

IMAGES_STORE = 'data/images/'


MONGODB_SERVER = "localhost"
MONGODB_PORT = 27017
MONGODB_DB = "hicloth"
MONGODB_COLLECTION = "clothes"
LOG_ENABLED = True
