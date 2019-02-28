from selenium import webdriver
from bs4 import BeautifulSoup
import json

def main(event, context):

    urls = scrape_home()

    response = {
        "headers": {'Content-Type': 'application/json'},
        "isBase64Encoded": False,
        "statusCode": 200,
        "body": json.dumps({'urls': scrape_home()})
    }

    return response

def scrape_home():
#create a headless chrome
    options = webdriver.ChromeOptions()
    options.binary_location = '/opt/headless-chromium'
    options.add_argument('headless')
    options.add_argument('disable-dev-shm-usage')
    options.add_argument('single-process')
    options.add_argument('no-sandbox')

    desired_capabilities = {'browserName': 'chrome', 'loggingPrefs': {'performance': 'ALL'}}

#create chrome webdriver that goes to groceries homepage
    browser = webdriver.Chrome('/opt/chromedriver',chrome_options=options, desired_capabilities=desired_capabilities)
    url = 'https://www.costco.com/grocery-household.html'
    browser.get(url)
    title = browser.title

#assign the page source to html and create soup with it
    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')

#create list of urls
    urls = []

#create base to add href too
    costcoBase = "https://www.costco.com"

#get hrefs and store into urls list
    for link in soup.find_all("a", {"class": "thumbnail"}):
        #print(link['href'])
        #add the url to https://www.costco.com
        addOn = costcoBase + link['href']
        urls.append(addOn)

#pop the first two elements because we do not want
#all same-day delivery category and all 2-day delivery
    urls.pop(0)
    urls.pop(0)

    #remove the last two elements because there are no products
    #in those categories
    del urls[-1]
    del urls[-1]

# quit browser
    browser.quit()
    return urls
