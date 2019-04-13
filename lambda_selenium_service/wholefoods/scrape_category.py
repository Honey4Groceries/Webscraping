from selenium import webdriver
import time
import json

def main(event, context):
    response = {
            "headers": {'Content-Type': 'application/json'},
            "isBase64Encoded": False,
            "statusCode": 200,
            "body": json.dumps({'data': scrape_category()})
    }
    return response

def scroll(driver):

    last_height = driver.execute_script("return document.documentElement.scrollHeight")

    while True:
        # using action chains to scroll
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(.5)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.documentElement.scrollHeight")

        if new_height == last_height:
            return

        last_height = new_height

def scrape_category():

    requestIDs = []
    data = []

    url = 'https://products.wholefoodsmarket.com/search?sort=relevance&store=10066&category=breads-rolls-bakery'

    desired_capabilities = webdriver.DesiredCapabilities.CHROME.copy()
    desired_capabilities['loggingPrefs'] = {'performance': 'INFO'}

    options = webdriver.ChromeOptions()
    options.binary_location = '/opt/headless-chromium'
    options.add_argument('headless')
    options.add_argument('single-process')
    options.add_argument('disable-dev-shm-usage')
    options.add_argument('no-sandbox')
    options.add_argument('homedir=/tmp')
    options.add_argument('data-path=/tmp/data-path')
    options.add_argument('disk-cache-dir=/tmp/cache-dir')

    driver = webdriver.Chrome('/opt/chromedriver', chrome_options=options, desired_capabilities=desired_capabilities)
    driver.command_executor._commands.update({'getLog': ('POST', '/session/$sessionId/log')})

    driver.get(url)

    scroll(driver)

    logs = driver.execute('getLog', {'type': 'performance'})['value']

    # retrieve ids of relevant requests
    for log in logs:
        parsed_log = json.loads(log['message'])['message']
        if parsed_log['method'] == "Network.requestWillBeSent":
            if 'api/search?' in parsed_log['params']['request']['url']:
                requestIDs.append(parsed_log['params']['requestId'])

    for requestID in requestIDs:
        data.append(json.loads(driver.execute_cdp_cmd('Network.getResponseBody', {'requestId':requestID})['body']))

    driver.quit()
    return data
