"""
Filename: costcoIntegrated.py
Author: Vivian Wei, Casey Price
Date: February 14th, 2019
Description: this file scrapes costco categories starting from the homepage
to get the name and price of the products in each category. It uses selenium,
requests, and beautiful soup to accomplish this.
"""
from selenium import webdriver
import requests
import urllib.request
from bs4 import BeautifulSoup

#-------------------------getting urls from homepage---------------------------

#create a headless chrome
options = webdriver.ChromeOptions()
options.add_argument('headless')
# options.add_argument('dump-dom')
options.add_argument('disable-dev-shm-usage')
options.add_argument('remote-debugging-port=8080')

#create chrome webdriver that goes to groceries homepage
browser = webdriver.Chrome(chrome_options=options)
url = 'https://www.costco.com/grocery-household.html'
browser.get(url)

#assign the page source to html and create soup with it
html = browser.page_source
soup = BeautifulSoup(html, 'html.parser')

#print the title
print(soup.title.get_text())

#create list of links to categories
links = []

#create base to add href to
costcoBase = "https://www.costco.com"

#get hrefs and store into urls list
for link in soup.find_all("a", {"class": "thumbnail"}):
    #print(link['href'])
    #add the url to https://www.costco.com
    addOn = costcoBase + link['href']
    links.append(addOn)

#pop the first two elements because we do not want
#all same-day delivery category and all 2-day delivery category
links.pop(0)
links.pop(0)

#remove the last two elements because there are no products
#in those categories
del links[-1]
del links[-1]

#-------------------------scraping categories----------------------------------

# Text file to hold output
text_file = open("output.txt", "w")


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

#links = ["https://www.costco.com/kirkland-signature-groceries.html?currentPage=1"]

# Loops through each webpage
for link in links:

    # Go to url
    url = link
    headers = {'User-Agent':'Wget/1.11.4', 'Accept':'*/*',
               'Connection':'Keep-  Alive'}
    html = requests.get(url, headers=headers)
    #browser.get(url)
    #html = browser.page_source

    # Create a BeautifulSoup object
    bsObj = BeautifulSoup(html.text, 'html.parser')

    #write newline to file for readability
    text_file.write('\n')
    #prints the name of the category
    text_file.write("----------" + bsObj.title.get_text() + \
            "----------")
    #write newline to file for readability
    text_file.write('\n')

    # Scrape the first page
    scrapeItems()


    # If multiple pages exist, iterate through each page and scrape it
    while 1:
        try:
            # Find next page button and go to it
            paging_elem = bsObj.find("li", {"class":"forward"})
            url = paging_elem.find("a")
            link = url.get('href')

            #seeing if browser can get this too
            #browser.get(link)
            #html = browser.page_source

            html = requests.get(link, headers=headers)
            bsObj = BeautifulSoup(html.text, 'html.parser')

            # Scrape all items on the page
            scrapeItems()
        except:
            # Reached last page in the category
            break;


#quit browser
browser.quit()
