from selenium import webdriver
import pychrome
import json
import time

requestIDs= []

def request_will_be_sent(**kwargs):
    print("1")
    if 'api/search?' in kwargs.get('request').get('url'):
        requestIDs.append(kwargs.get('requestId'))
        print(kwargs.get('request').get('url'))

url = 'https://products.wholefoodsmarket.com/search?sort=relevance&store=10066&category=breads-rolls-bakery'

options = webdriver.ChromeOptions()

options.add_argument('headless')
options.add_argument('--no-sandbox')
options.add_argument('remote-debugging-port=9222')

driver = webdriver.Chrome(chrome_options=options)

browser = pychrome.Browser(url='http://127.0.0.1:9222')
tab = browser.new_tab()

tab.set_listener('Network.requestWillBeSent', request_will_be_sent)

tab.start()
tab.call_method('Network.enable')
tab.call_method('Page.navigate', url=url, _timeout=10)


SCROLL_PAUSE_TIME = 0.5

# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    print("2")
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height


tab.wait(10)

for requestID in requestIDs:
    print(json.dumps(json.loads(tab.call_method('Network.getResponseBody', requestId=requestID)['body']), indent=4))
tab.stop()

