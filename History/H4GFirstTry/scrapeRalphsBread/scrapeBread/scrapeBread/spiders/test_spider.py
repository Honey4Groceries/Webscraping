import scrapy
from selenium import webdriver
class TestSpider(scrapy.Spider):
        name = "test"

        start_urls = [
            'http://www.ralphs.com/pl/bakery-bread/01002',
        ]

        def parse(self, response):
            filename = response.url.split("/")[-1] + '.html'
            with open(filename, 'wb') as f:
                f.write(response.body)
