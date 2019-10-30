from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from vacancyparser import settings
from vacancyparser.spiders.spider_hh import SpiderHhSpider
from vacancyparser.spiders.spider_sj import SpiderSjSpider

if __name__=='__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process=CrawlerProcess(settings=crawler_settings)
    process.crawl(SpiderHhSpider)
    process.crawl(SpiderSjSpider)
    process.start()