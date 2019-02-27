from selenium import webdriver
# from selenium.webdriver.chrome.options import Options

def hello(event, context):
    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": event
    }

    title = scrapeVons()

    response = {
        "statusCode": 200,
        "body": title
    }

    return response

    # Use this code if you don't use the http event with the LAMBDA-PROXY
    # integration
    """
    return {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "event": event
    }
    """

def scrapeVons():

#create a headless chrome
    options = webdriver.ChromeOptions()
    options.binary_location = '/opt/headless-chromium'
    options.add_argument('headless')
    options.add_argument('disable-dev-shm-usage')
    options.add_argument('single-process')
    options.add_argument('no-sandbox')

#create chrome webdriver that goes to groceries homepage
    browser = webdriver.Chrome('/opt/chromedriver',chrome_options=options)
    url = 'https://www.costco.com/grocery-household.html'
    browser.get(url)
    title = browser.title

#assign the page source to html and create soup with it
    #html = browser.page_source
    #soup = BeautifulSoup(html, 'html.parser')

##print the title
    #print(soup.title.get_text())

##create list of urls
    #urls = []

##create base to add href too
    #costcoBase = "https://www.costco.com"

##get hrefs and store into urls list
    #for link in soup.find_all("a", {"class": "thumbnail"}):
    #    #print(link['href'])
    #    #add the url to https://www.costco.com
    #    addOn = costcoBase + link['href']
    #    urls.append(addOn)

##pop the first two elements because we do not want
##all same-day delivery category and all 2-day delivery
    #urls.pop(0)
    #urls.pop(0)

    #print(urls)

#quit browser
    browser.quit()
    return title





## def scrapeVons():
##     requestIDs = []

##     def request_will_be_sent(**kwargs):
##         if 'aemaisle' in kwargs.get('request').get('url'):
##             requestIDs.append(kwargs.get('requestId'))

##     url = 'https://shop.vons.com/aisles/bread-bakery/bakery-bread.2832.html?zipcode=91007'

##     options = webdriver.ChromeOptions()

##     options.binary_location = '/opt/headless-chromium'

##     options.add_argument('headless')
##     options.add_argument('remote-debugging-port=9222')
##     options.add_argument('disable-dev-shm-usage')

##     driver = webdriver.Chrome('/opt/chromedriver', chrome_options=options)

##     browser = pychrome.Browser(url='http://127.0.0.1:9222')
##     tab = browser.new_tab()

##     tab.set_listener('Network.requestWillBeSent', request_will_be_sent)

##     tab.start()
##     tab.call_method('Network.enable')
##     tab.call_method('Page.navigate', url=url, _timeout=10)

##     tab.wait(10)

##     jsons = []

##     for requestID in requestIDs:
##        jsons.append(tab.call_method('Network.getResponseBody', requestId=requestID)['body'])
##     tab.stop()

##     driver.quit()

##     return jsons
