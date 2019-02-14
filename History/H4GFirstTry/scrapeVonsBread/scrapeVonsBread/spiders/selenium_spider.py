import scrapy
from selenium import webdriver

class SeleniumSpider(scrapy.Spider):
    name = "selenium"
    start_urls = ['https://shop.vons.com/aisles/bread-bakery/bakery-bread.2118.html']

    def __init__(self):
        self.driver = webdriver.Chrome()

    def parse(self, response):
        self.driver.get(response.url)
        res = response.replace(body=self.driver.page_source)

        filename = "testFile"
        with open(filename, 'wb') as f:
            f.write(res.body)

        self.driver.quit()
