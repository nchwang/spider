# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import logging
from jxnewspider.items import JxnewspiderItem


class JxNewSpider(CrawlSpider):
    #name of spider, -- scrapy crawl [spider name]



    name = 'spider'
    allowed_domains = ['jxnews.com.cn']
    start_urls = ['http://jxnews.com.cn/']



    rules = (
        # Extract links matching 'category.php' (but not matching 'subsection.php')
        # and follow links from them (since no callback means follow=True by default).
        Rule(LinkExtractor(allow=('jiangxi.jxnews.com.cn')),follow=True,callback='process_items'),
    )

    def process_items(self,response):

        try:
            title = response.xpath('//*[@id="Con620"]/div[7]/text()').extract_first()

            detail = ''
            publishTime = ''
            originalSite = ''

            if title:
                detailList = response.xpath('//*[@id="Con620"]/div[22]/div//text()').extract()

                if not detailList:
                    detailList = response.xpath('//*[@id ="Con620"]/div[@class="text"]//text()').extract()

                if detailList:
                    for rec in detailList:
                        rec = rec.strip().replace('\n','')
                        if len(rec) > 1:
                            detail = detail + '\r\n'+ rec

                    publishTime = response.xpath('//*[@id="pubtime_baidu"]/text()').extract_first()
                    if publishTime:
                        pass
                    else:
                        publishTime = ''

                    originalSite = response.xpath('//*[@id="source_baidu"]/a/text()').extract_first()
                    if originalSite:
                        pass
                    else:
                        originalSite =  ''

                    item = JxnewspiderItem(url=response.url, title=title, detail=detail, publishTime=publishTime,
                                           originalSite=originalSite)
                    yield item
                    #logging.info(item)

                else:
                    logging.error("Wrong URL : %s for content" % (response.url))


            else:
                logging.error("Wrong URL : %s for title" % (response.url))


        except Exception , err:
            logging.critical("Wrong URL : %s for %s" % (response.url,err))

    def parse_start_url(self, response):
        pass




