from selenium import webdriver
import time
import json

def main(event, context):
    """ Main function that is executed upon lambda function invocation.
    
    Arguments:
        event {dict} -- event data of function invocation
        context {[LambdaContext]} -- runtime information to handler
    
    Returns:
        json -- type 
    """
    if 'queryStringParameters' not in event.keys() or 'url' not in event['queryStringParameters'].keys():
        failedResponse = {
            "headers": {'Content-Type': 'application/json'},
            "isBase64Encoded": False,
            "statusCode": 406,
            "body": json.dumps({'body':'URL must be specified!'})
        }
        return failedResponse

    url = event['queryStringParameters']['url']

    response = {
            "headers": {'Content-Type': 'application/json'},
            "isBase64Encoded": False,
            "statusCode": 200,
            "body": json.dumps({'data': scrape_category(url)})
    }
    return response

def scroll(driver):
    """scroll down on page 
    
    Arguments:
        driver {webdriver} -- selenium webdriver to be scrolled down on
    """

    last_height = driver.execute_script("return document.documentElement.scrollHeight")

    while True:
        # execute js to scroll
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(.5)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.documentElement.scrollHeight")

        if new_height == last_height:
            return

        last_height = new_height

def scrape_category(url):
    """scrapes item data given url to category page
    
    Arguments:
        url {string} -- url to category page
    
    Returns:
        json -- raw unprocessed json intercepted from outbound request
    """

    requestIDs = []
    data = []

    # need to setup desired_capabilities as follows in order to obtain logs
    desired_capabilities = webdriver.DesiredCapabilities.CHROME.copy()
    desired_capabilities['loggingPrefs'] = {'performance': 'INFO'}

    # setup webdriver as follows to get it to run on 
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

    # get url from webdriver
    driver.get(url)

    # scrolls webdriver till bottom of page
    scroll(driver)

    # retrieve logs from chrome
    logs = driver.execute('getLog', {'type': 'performance'})['value']

    # retrieve ids of relevant requests
    for log in logs:
        parsed_log = json.loads(log['message'])['message']
        if parsed_log['method'] == "Network.requestWillBeSent":
            # relevant requests will be made to a url containing the string 'api/search?'
            if 'api/search?' in parsed_log['params']['request']['url']:
                requestIDs.append(parsed_log['params']['requestId'])

    # get response for relevant requests
    for requestID in requestIDs:
        data.append(json.loads(driver.execute_cdp_cmd('Network.getResponseBody', {'requestId':requestID})['body']))

    driver.quit()
    return data
