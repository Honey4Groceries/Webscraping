from selenium import webdriver
import pychrome
import json

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

driver = webdriver.Chrome(chrome_options=options)

browser = pychrome.Browser(url='http://127.0.0.1:9222')
tab = browser.new_tab()

driver.switch_to.window(driver.window_handles[1])

tab.set_listener('Network.requestWillBeSent', request_will_be_sent)

tab.start()
tab.call_method('Network.enable')
tab.call_method('Page.navigate', url=url, _timeout=10)

tab.wait(10)

for requestID in requestIDs:
    print(json.dumps(json.loads(tab.call_method('Network.getResponseBody', requestId=requestID)['body']), indent=4))
tab.stop()

driver.quit()
