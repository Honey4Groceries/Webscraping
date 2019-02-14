import scrapy
from scrapy_splash import SplashRequest

class SplashSpider(scrapy.Spider):
    name = 'splash'

    def start_requests(self):
        yield SplashRequest(
            url = 'http://www.ralphs.com/pl/bakery-bread/01002',
            callback = self.parse,
            args={'wait':5}
        )

    def parse(self,response):
        filename = 'splash_html'
        with open(filename, 'wb') as f:
            f.write(response.body)

