import scrapy


class HomepageSpider(scrapy.Spider):
    name = "homepage"

    def start_requests(self):
        headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel \
                Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) \
                Chrome/71.0.3578.98 Safari/537.36', 'Accept':'*/*', \
                'Connection':'Keep-Alive'}
        yield scrapy.Request(url='https://www.costco.com/grocery-household.html',\
                callback=self.parse,\
                headers=headers)

    def parse(self, response):
        filename = 'homepage-html'
        with open(filename, 'wb') as f:
            f.write(response.body)
