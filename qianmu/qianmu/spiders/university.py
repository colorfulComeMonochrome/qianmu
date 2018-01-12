# -*- coding: utf-8 -*-
import scrapy


class UniversitySpider(scrapy.Spider):
    name = 'university'
    allowed_domains = ['qianmu.iguye.com']
    start_urls = ['http://qianmu.iguye.com/2018USNEWS世界大学排名']

    def __init__(self, max_num=0, *args, **kwargs):
        super(UniversitySpider, self).__init__(*args, **kwargs)
        self.max_num = int(max_num)

    def parse(self, response):
        links = response.xpath('//*[@id="content"]//tr[position()>1]/td[2]//@href').extract()
        for i, link in enumerate(links):
            if self.max_num and self.max_num <= i:
                break
            if not link.startswith('http://'):
                link = 'http://qianmu.iguye.com/%s' % link
            request = scrapy.Request(link, callback=self.parse_university)
            request.meta["class"] = i + 1
            yield request


    def parse_university(self, response):
        self.logger.info(response.url)
        item = dict(title=response.xpath('//*[@id="wikiContent"]/h1/text()').extract_first())
        wiki_content = response.xpath('//div[@class="infobox"]')[0]
        keys = wiki_content.xpath('./table/tbody/tr/td[1]/p/text()').extract()
        cols = wiki_content.xpath('./table//tr/td[2]')
        values = [''.join(col.xpath('.//text()').extract()) for col in cols]
        item["class"] = response.meta["class"]
        item.update(zip(keys, values))
        self.logger.info('item %s scraped' % item["title"])
        yield item



