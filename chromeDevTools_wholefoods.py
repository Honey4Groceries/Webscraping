from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pychrome
import json
import time

'''
tried using 2 tabs to see if one of them will scroll

tried scrolling by smaller increments

tried sleeping to load the page before scrolling

tried closing all tabs

tried both ActionChains and driver.scrollTo, both only scrolls old tabs and not
the newest one >:(((((((((((((((((

tried changing from driver scroll to tab scroll (tab has no scroll)

'''

requestIDs= []

def request_will_be_sent(**kwargs):
    if 'api/search?' in kwargs.get('request').get('url'):
        requestIDs.append(kwargs.get('requestId'))
        print(kwargs.get('request').get('url'))

def scroll(driver):

    last_height = driver.execute_script("return document.documentElement.scrollHeight")
    actions = ActionChains(driver)

    while True:
        # using action chains to scroll
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(.5)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.documentElement.scrollHeight")

        if new_height == last_height:
                return

        last_height = new_height

url = 'https://products.wholefoodsmarket.com/search?sort=relevance&store=10066&category=breads-rolls-bakery'

options = webdriver.ChromeOptions()

options.add_argument('headless')
options.add_argument('--no-sandbox')
options.add_argument('remote-debugging-port=9222')

driver = webdriver.Chrome(chrome_options=options)

browser = pychrome.Browser(url='http://127.0.0.1:9222')
tab = browser.new_tab()


# SWITCH THE FOCUS TAB THIS IS THE LINE THAT FINALLY FIXED IT OMG
driver.switch_to.window(driver.window_handles[1])


tab.set_listener('Network.requestWillBeSent', request_will_be_sent)
tab.start()
tab.call_method('Network.enable')
tab.call_method('Page.navigate', url=url, _timeout=10)

scroll(driver)

print(len(requestIDs))
# for requestID in requestIDs:
#     print(json.dumps(json.loads(tab.call_method('Network.getResponseBody', requestId=requestID)['body']), indent=4) + '\n\n\n\n\n\n^^^^^^^^^^^^^^^^^^^^')
tab.stop()
driver.quit()
