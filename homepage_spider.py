import scrapy


class HomepageSpider(scrapy.Spider):
    name = "homepage"

    def start_requests(self):
        headers = {'User-Agent':'Wget/1.11.4', 'Accept':'*/*', \
                'Connection':'Keep-Alive'}
        yield scrapy.Request(url='https://www.costco.com/grocery-household.html',\
                callback=self.parse,\
                headers=headers)

    def parse(self, response):
        filename = 'homepage-html'
        with open(filename, 'wb') as f:
            f.write(response.body)
