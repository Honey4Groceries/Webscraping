import scrapy

class BreadSpider(scrapy.Spider):
    name = "bread"
    
    def start_requests(self):
        urls = [
                'https://shop.vons.com/aisles/bread-bakery/bakery-bread.2118.html'
        ]
        

        for url in urls:
            yield scrapy.Request(url=url, callback = self.parse)

    def parse(self, response):
        page = response.url
        filename = 'bread-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)

