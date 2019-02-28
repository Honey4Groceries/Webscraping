from selenium import webdriver
from bs4 import BeautifulSoup
import json

def main(event, context):
    response = {
        "headers": {'Content-Type': 'application/json'},
        "isBase64Encoded": False,
        "statusCode": 200,
        "body": json.dumps({'data': scrape_category()})
    }

    return response

def scrape_category():
    requestIDs = []
    data = []

    url = 'https://shop.vons.com/aisles/bread-bakery/bakery-bread.2832.html?zipcode=91007'

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

    logs = driver.execute('getLog', {'type': 'performance'})['value']
    for log in logs:
        parsed_log = json.loads(log['message'])['message']
        if parsed_log['method'] == "Network.requestWillBeSent":
            if 'aemaisle' in parsed_log['params']['request']['url']:
                requestIDs.append(parsed_log['params']['requestId'])

    for requestID in requestIDs:
        data.append(json.loads(driver.execute_cdp_cmd('Network.getResponseBody', {'requestId':requestID})['body']))

    driver.quit()
    return data
