from bs4 import BeautifulSoup
import scrapy

class BreadSpider(scrapy.Spider):
    name = "bread"
    
    def start_requests(self):
        urls = [
            'http://www.ralphs.com/pl/bakery-bread/01002?page=1'
        ]
        
        headers = {
                ":authority" : "www.ralphs.com",
                ":method" : "GET",
                ":path" : "/pl/bakery-bread/01002?page=1",
                ":scheme" : "https",
                "accept" : "text/html,application/xhtml+xml,application/xml;"\
                        "q=0.9,image/webp,image/apng,*/*;q=0.8",
                "accept-encoding" : "gzip, deflate, br",
                "accept-language" : "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
                "cache-control" : "max-age=0",
                "upgrade-insecure-requests" : "1",
                "user-agent" : "Mozilla/5.0 (Windows NT 6.3; Win64; x64) "\
                        "AppleWebKit/537.36 (KHTML, like Gecko) "\
                        "Chrome/70.0.3538.110 Safari/537.36"

        }

        for url in urls:
            yield scrapy.Request(url=url, callback = self.parse, headers = headers)

    def parse(self, response):
       soup = BeautifulSoup(response.text, 'html.parser')
       results = soup.select("div.PriceDisplay")
       print(results)
        
       """ page = response.url.split("=")[-1]
        filename = 'bread-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body) """

