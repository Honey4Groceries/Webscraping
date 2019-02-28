from selenium import webdriver
import pychrome
import json

requestIDs= []

def request_will_be_sent(**kwargs):
    if 'api/search?' in kwargs.get('request').get('url'):
        requestIDs.append(kwargs.get('requestId'))
        print(kwargs.get('request').get('url'))

url = 'https://products.wholefoodsmarket.com/search?sort=relevance&store=10066&category=breads-rolls-bakery'

options = webdriver.ChromeOptions()

options.add_argument('headless')

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
