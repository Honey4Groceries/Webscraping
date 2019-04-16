import requests
import urllib.request
from bs4 import BeautifulSoup
import time

# Text file to hold output
text_file = open("output.txt", "w")
html_file = open("html.html", "r")


def scrapeItems():
    """Gets the name and price of each product on the webpage."""

    # Collects all of the products on the page into a list
    productList = bsObj.findAll("div", {"class":"product"})

    if productList == None:
        print("products could not be found")
    else:
        # Iterates through each product, printint the name and price to the output text file
        for idx in range(0, len(productList)):
            product_name = productList[idx].find("p", {"class":"description"})
            text_file.write(product_name.text)

            # Some products do not have a price listed because they are only available in the warehouse
            try:
                product_price = productList[idx].find("div", {"class":"price"})
                text_file.write(product_price.text + "\n")
            except:
                text_file.write("Warehouse only -- No price listed.\n")

"""links =
["https://www.costco.com/kirkland-signature-groceries.html?currentPage=1"]

# Loops through each webpage
for link in links:
    start = time.time()

    # Go to url using headers
    url = link
    headers = {'User-Agent':'Wget/1.11.4', 'Accept':'*/*',
               'Connection':'Keep-  Alive'}
    html = requests.get(url, headers=headers)
"""
# Create a BeautifulSoup object
sum = 0;

bsObj = BeautifulSoup(html_file.read(), 'html.parser')

for x in range(1, 100):
    start = time.time()
    # Scrape the first page
    scrapeItems()
    end=time.time()
    sum = sum + end - start

print(sum/100)

"""    # If multiple pages exist, iterate through each page and scrape it
    while 1:
        try:
            # Find next page button and go to it
            paging_elem = bsObj.find("li", {"class":"forward"})
            url = paging_elem.find("a")
            link = url.get('href')

            html = requests.get(link, headers=headers)
            bsObj = BeautifulSoup(html.text, 'html.parser')

            # Scrape all items on the page
            scrapeItems()
        except:
            # Reached last page in the category
            break;
"""
