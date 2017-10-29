# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HouseSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    house_name=scrapy.Field()
    total_price=scrapy.Field()
    unit_price=scrapy.Field()
    house_rooms=scrapy.Field()
    house_area=scrapy.Field()
    house_towards=scrapy.Field()
    house_fitmend=scrapy.Field()
    house_located=scrapy.Field()
