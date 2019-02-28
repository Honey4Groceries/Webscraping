from bs4 import BeautifulSoup
import requests
import json

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
    for url in urls:
        html = requests.get(url, headers=headers)

        # Create a BeautifulSoup object
        bsObj = BeautifulSoup(html.text, 'html.parser')

        category_name = bsObj.title.get_text()

        # Scrape the first page
        product_data = scrapeItems(bsObj)

        # If multiple pages exist, iterate through each page and scrape it
        while 1:
            try:
                # Find next page button and go to it
                paging_elem = bsObj.find("li", {"class":"forward"})
                url = paging_elem.find("a")
                link = url.get('href')

                html = requests.get(link, headers=headers)
                bsObj = BeautifulSoup(html.text, 'html.parser')

                # Scrape all items on the page
                product_data.extend(scrapeItems(bsObj))
            except:
                # Reached last page in the category
                break
        
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
            product_name = productList[idx].find("p", {"class":"description"}).text
            # Some products do not have a price listed because they are only available in the warehouse
            product_price = None
            try:
                product_price = productList[idx].find("div", {"class":"price"}).text
            except:
                pass

            productDictList.append({'name': product_name, 'price': product_price})

    return productDictList