from selenium import webdriver
from bs4 import BeautifulSoup
import json
import re

def main(event, context):
     """ Main function that is executed upon lambda function invocation.
    
    Arguments:
        event {dict} -- event data of function invocation
        context {[LambdaContext]} -- runtime information to handler
    
    Returns:
        json -- type 
    """
    response = {
        "headers": {'Content-Type': 'application/json'},
        "isBase64Encoded": False,
        "statusCode": 200,
        "body": json.dumps(scrape_home())
    }

    return response

def scrape_home():
    """scrapes category urls
    
    Returns:
        [string] -- list of category urls as strings
    """
    options = webdriver.ChromeOptions()
    options.binary_location = '/opt/headless-chromium'
    options.add_argument('headless')
    options.add_argument('disable-dev-shm-usage')
    options.add_argument('single-process')
    options.add_argument('no-sandbox')

    # create chrome webdriver that goes to groceries homepage
    browser = webdriver.Chrome('/opt/chromedriver',chrome_options=options)
    url = 'https://products.wholefoodsmarket.com/categories'
    browser.get(url)

    # assign the page source to html and create soup with it
    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')

    #create list of links to categories
    links = []

    #create base to add href to
    wholefoodsBase = "https://products.wholefoodsmarket.com"

    #get hrefs and store into urls list
    for link in soup.find_all("a", {"class": \
        re.compile("Categories-Category(.*)")}):

        #add the url to https://www.costco.com
        addOn = wholefoodsBase + link['href']
        links.append(addOn)

    browser.quit()

    return links
