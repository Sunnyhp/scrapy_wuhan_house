# -*- coding: utf-8 -*-
import scrapy
from scrapy import Spider,Request
import re
from ..items import HouseSpiderItem

class HouseSpider(scrapy.Spider):
    name = "wh_house"

    region_mapping={'jiangan': u'江岸', 'jianghan': u'江汉', 'qiaokou': u'硚口', 'dongxihu': u'东西湖',
             "wuchang": u'武昌',"qingshan": u'青山',"hongshan":u'洪山',"hanyang":u'汉阳',
             'donghugaoxin':u'东湖高新',"jiangxia":u'江夏'}

    house_fitmend_mapping={u'精装':u'精装', u'简装':u'简装', u"毛坯":u"毛坯", u"其他":u"其他"}

    def start_requests(self):
        wh_area = ["jiangan", "jianghan", "qiaokou", "dongxihu", "wuchang", "qingshan", "hongshan", "hanyang", "donghugaoxin", "jiangxia"]
        urls = ['https://wh.lianjia.com/ershoufang/' + area + '/' for area in wh_area]
        for url in urls:
            print 'url:',url
            yield Request(url=url,callback=self.parse)


    def parse(self,response):
        page_info=response.css('div[class="page-box fr"]').css('div::attr(page-data)').extract_first()
        page_list=re.findall('\d+',page_info)
        total_page=int(page_list[0])
        for i in range(1,total_page+1):
            url=response.url+'pg'+str(i)
            yield Request(url=url, callback=self.parse_each_page)


    def parse_each_page(self, response):
        clears=response.css('.sellListContent li')
        print 'Total:',len(clears)
        for c in clears:
            item = HouseSpiderItem()

            try:
                house_name = c.css('.houseInfo a::text').extract_first()
                house_text = c.css('.houseInfo::text').extract_first()
                house_info_list = [e for e in re.split('\|', house_text) if len(e) > 1]
                house_room_text = house_info_list[0].strip()
                house_rooms= house_room_text
                house_area = ''.join(re.findall(r'[\d+\.]', house_info_list[1]))
                house_towards=re.sub('\s+','',house_info_list[2])
                house_fitmend=house_info_list[3].strip()
                total_price = c.css('.totalPrice span::text').extract_first()
                unit_price = c.css('.unitPrice span::text').extract_first()
                unit_price = re.findall('\d+', unit_price)[0]

                house_located = [x for x in response.url.split('/') if x][-2]

                print 'house_name:',house_name
                print 'house_text:',house_text
                print 'house_area:',house_area
                print 'house_rooms:', house_rooms
                print 'house_towards:',house_towards
                print 'house_fitmend:',self.house_fitmend_mapping[house_fitmend]
                print 'total_price:',total_price
                print 'unit_price:',unit_price
                print 'house_located:',self.region_mapping[house_located]

                item['house_name'] = house_name
                item['total_price'] = float(total_price)
                item['unit_price'] = int(unit_price)
                item['house_area'] = float(house_area)
                item['house_rooms'] = house_rooms
                item['house_towards'] = house_towards
                item['house_fitmend'] = house_fitmend
                item['house_located'] = self.region_mapping[house_located]

                yield item
            except Exception as e:
                print e,house_info_list


