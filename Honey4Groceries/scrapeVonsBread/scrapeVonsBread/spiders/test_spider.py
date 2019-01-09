import scrapy
from scrapy_splash import SplashRequest

class TestSpider(scrapy.Spider):
        name = "test"
    
        def start_requests(self):
            yield SplashRequest(
                url = 'https://shop.vons.com/aisles/bread-bakery/bakery-bread.2118.html',
                callback = self.parse,
            )

        def parse(self, response):
            filename = "testFile"
            with open(filename, 'wb') as f:
                f.write(response.body)
