import time
from selenium import webdriver
import pychrome
import json

# store all the requestIDs we want
requestIDs= []

# callback for requestWillBeSent, finds requests with 'aemaisle' and add the id
# it to requestIDs. When Vons makes a HTTP request this will be called
def request_will_be_sent(**kwargs):
    if 'aemaisle' in kwargs.get('request').get('url'):
        requestIDs.append(kwargs.get('requestId'))

url = 'https://shop.vons.com/aisles/bread-bakery/bakery-bread.2832.html?zipcode=91007'

# options for local debugging
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('remote-debugging-port=9222')

driver = webdriver.Chrome(chrome_options=options)

# create a tab
browser = pychrome.Browser(url='http://127.0.0.1:9222')
tab = browser.new_tab()

# register the callback
tab.set_listener('Network.requestWillBeSent', request_will_be_sent)

# call method with timeout
tab.start()
tab.call_method('Network.enable')
tab.call_method('Page.navigate', url=url, _timeout=10)

# wait for loading
tab.wait(10)

# get the response body for each requestId and print it out
for requestID in requestIDs:
    print(json.dumps(json.loads(tab.call_method('Network.getResponseBody', requestId=requestID)['body']), indent=4))

# stop the tab
tab.stop()

driver.quit()
