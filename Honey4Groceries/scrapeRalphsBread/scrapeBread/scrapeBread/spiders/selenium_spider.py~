import scrapy
from selenium import webdriver

class SeleniumSpider(scrapy.Spider):
    name = "selenium"
    start_urls = ['http://www.ralphs.com/pl/bakery-bread/01002?page=1']

    def __init__(self):
        self.sriver = webdriver.Chrome()

    def parse(self, response):
        self.driver.get(response.url)
        res = response.replace(body=self.diver.page_source)

        with open(filename, 'wb') as f:
            f.write(res.body)
