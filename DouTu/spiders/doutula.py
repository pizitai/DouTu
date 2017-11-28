#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@version: ??
@author: wzp
@contact: 993459032@qq.com
@software: PyCharm
@file: doutula.py
@time: 2017/9/7 19:33
"""

import os
import scrapy
import requests
import sys
from DouTu.items import DoutuItem

reload(sys)
sys.setdefaultencoding('utf-8')


class Doutu(scrapy.Spider):
    name = 'doutu'
    allowed_domains = ['doutula']
    # 列表推导式
    start_urls = ['http://www.doutula.com/photo/list/?page={}'.format(i) for i in range(1, 2)]

    def parse(self, response):
        i = 0
        for content in response.xpath('//*[@id="pic-detail"]/div/div[1]/div[2]/ul/li/div/div/a'):
            items = DoutuItem()
            i += 1
            try:
                print (content.xpath('//img/@data-original').extract()[i])
                items['img_url'] = content.xpath('//img/@data-original').extract()[i]
                items['name'] = content.xpath('//p/text()').extract()[i]
            except Exception as e:
                raise IndexError

            try:
                filename = 'F:\doutu\\{}'.format(items['name']) + items['img_url'][-4:]  # 图片路径
                if not os.path.exists(filename):
                    # r = requests.get('http:'+items['img_url'])
                    r = requests.get(':'.join(['http', items['img_url']]))
                    with open(filename, 'wb') as f:
                        f.write(r.content)
                print (u'图片已经存在了')
            except Exception as e:
                print (e, '--------')
            yield items
            # print (content)
