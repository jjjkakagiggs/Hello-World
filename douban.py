# -*- coding: utf-8 -*-
import scrapy
import random
import time
from scrapy.http import Request
from Doubanmovie.items import DoubanmovieItem

class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['movie.douban.com']
    # start_urls = ['http://movie.douban.com/']
    user_agent_list = [
        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36',
        'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
    ]
    user_agent = random.choice(user_agent_list)
    headers = {'User-Agent': user_agent,
               # 'Host': 'www.dianping.com',
               # 'Accept': '*/*',
               }

    def start_requests(self):
        for i in range(0,260,25):
            url = 'https://movie.douban.com/top250?start={}&filter='.format(i)
            time.sleep(10)
            yield Request(url=url,callback=self.parse,headers=self.headers,dont_filter=True)


    def parse(self, response):
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        nodes = response.xpath('//ol[@class="grid_view"]/li')
        item = DoubanmovieItem()
        for node in nodes:
            title = node.xpath('./div/div[@class="info"]/div[@class="hd"]/a/span[@class="title"]/text()').extract_first()
            url = node.xpath('./div/div[@class="info"]/div[@class="hd"]/a/@href').extract_first()
            content_ori =  node.xpath('./div/div[@class="info"]/div[@class="bd"]/p/text()').extract()
            content_list = []
            for co in content_ori:
                co = co.strip()
                content_list.append(co)
            content = ';'.join(content_list)
            content = content.replace('\xa0','')
            content = content.replace(';', '')
            score = node.xpath('./div/div[@class="info"]/div[@class="bd"]/div[@class="star"]/span[@class="rating_num"]/text()').extract_first()
            info = node.xpath('./div/div[@class="info"]/div[@class="bd"]/p[@class="quote"]/span/text()').extract_first()
            item['title'] = title
            item['content'] = content
            item['score'] = score
            item['info'] = info
            item['url'] = url

            yield item


