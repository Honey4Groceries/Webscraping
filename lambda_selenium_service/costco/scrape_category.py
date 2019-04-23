from bs4 import BeautifulSoup
from selenium import webdriver
import json
import time

def main(event, context):
    if 'queryStringParameters' not in event.keys() or 'urls' not in event['queryStringParameters'].keys():
        failedResponse = {
            "headers": {'Content-Type': 'application/json'},
            "isBase64Encoded": False,
            "statusCode": 406,
            "body": json.dumps({'body':'URL must be specified!'})
        }
        return failedResponse

    urls = event['queryStringParameters']['urls'].split(',')

    product_data = scrape_category(urls)
    response = {
        "headers": {'Content-Type': 'application/json'},
        "isBase64Encoded": False,
        "statusCode": 200,
        "body": json.dumps(product_data)
    }

    return response

def scrape_category(urls):
    headers = {'User-Agent':'Wget/1.11.4', 'Accept':'*/*',
               'Connection':'Keep-Alive'}
    product_cat_data = []

    options = webdriver.ChromeOptions()
    options.binary_location = '/opt/headless-chromium'
    options.add_argument('headless')
    options.add_argument('single-process')
    options.add_argument('disable-dev-shm-usage')
    options.add_argument('no-sandbox')
    options.add_argument('homedir=/tmp')
    options.add_argument('data-path=/tmp/data-path')
    options.add_argument('disk-cache-dir=/tmp/cache-dir')

    driver = webdriver.Chrome('/opt/chromedriver', chrome_options=options)
    driver.command_executor._commands.update({'getLog': ('POST', '/session/$sessionId/log')})

    for url in urls:
        driver.get(url)
        html = driver.page_source
        """note that THIS IS THE PROBLEM, html is not a html apparantly"""
        # Create a BeautifulSoup object
        bsObj = BeautifulSoup(html, 'html.parser')

        category_name = bsObj.title.get_text()

        # Scrape the first page
        product_data = scrapeItems(bsObj)

        # If multiple pages exist, iterate through each page and scrape it
        """while 1:
            try:
                #wait a bit so that we don't get banned
                time.sleep(0.5)
                # Find next page button and go to it
                paging_elem = bsObj.find("li", {"class":"forward"})
                url = paging_elem.find("a")
                link = url.get('href')

                driver.get(link)
                html = driver.page_source
                bsObj = BeautifulSoup(html, 'html.parser')

                # Scrape all items on the page
                product_data.extend(scrapeItems(bsObj))

            except:
                # Reached last page in the category
                break
"""
        product_cat_data.append({'category':category_name, 'data':product_data})
    return product_cat_data

"""
this function takes in a beautifulSoup object and a text_file and returns a
dictionary with product dictionaries containing name and prices
"""
def scrapeItems(bsObj):
    """Gets the name and price of each product on the webpage."""

    # Collects all of the products on the page into a list
    productList = bsObj.findAll("div", {"class":"product"})
    productDictList = []

    if not productList:
        return {}
    else:
        # Iterates through each product, print the name and price to the output text file
        for idx in range(0, len(productList)):
            product_name = productList[idx].find("p", {"class":"description"}).text.lstrip('\n').rstrip('\n')
            # Some products do not have a price listed because they are only available in the warehouse
            product_price = None
            try:
                product_price = productList[idx].find("div", {"class":"price"}).text
            except:
                pass

            productDictList.append({'name': product_name, 'price': product_price})

    return productDictList
