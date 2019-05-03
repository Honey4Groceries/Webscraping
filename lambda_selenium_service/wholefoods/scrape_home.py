from selenium import webdriver
from bs4 import BeautifulSoup
import json
import re

def main(event, context):
    response = {
        "headers": {'Content-Type': 'application/json'},
        "isBase64Encoded": False,
        "statusCode": 200,
        "body": json.dumps(scrape_home())
    }

    return response

def scrape_home():
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
    names = []

    #create base to add href to
    wholefoodsBaseFront = 'https://products.wholefoodsmarket.com/api/search?sort=relevance&store=10066&limit=20&skip=0&filters=[{"ns":"category","key":"'
    wholefoodsBaseMiddle = '","value":"'
    wholefoodsBaseEnd = '"}]'
    insertion = "produce"

    #get hrefs and store into urls list
    for link in soup.find_all("a", {"class": \
        re.compile("Categories-Category(.*)")}):

        #add the url to https://www.costco.com
        name = link['href']
        insertion = (name.split("="))[1]
        addOn = wholefoodsBaseFront + insertion + \
            wholefoodsBaseMiddle + insertion + \
            wholefoodsBaseEnd
        names.append(addOn)

    browser.quit()
    return names
