import time
from selenium import webdriver
import pychrome
import json

requestIDs= []

def request_will_be_sent(**kwargs):
    if 'aemaisle' in kwargs.get('request').get('url'):
        requestIDs.append(kwargs.get('requestId'))

url = 'https://shop.vons.com/aisles/bread-bakery/bakery-bread.2832.html?zipcode=91007'

options = webdriver.ChromeOptions()

options.add_argument('headless')
options.add_argument('remote-debugging-port=9222')

driver = webdriver.Chrome(chrome_options=options)

browser = pychrome.Browser(url='http://127.0.0.1:9222')
tab = browser.new_tab()

tab.set_listener('Network.requestWillBeSent', request_will_be_sent)

tab.start()
tab.call_method('Network.enable')
tab.call_method('Page.navigate', url=url, _timeout=10)

tab.wait(10)

for requestID in requestIDs:
    print(json.dumps(json.loads(tab.call_method('Network.getResponseBody', requestId=requestID)['body']), indent=4))
tab.stop()

driver.quit()
