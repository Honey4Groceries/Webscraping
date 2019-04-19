"""
Filename: scrapeCostco.py
Author: Vivian Wei
Date: Janurary 30th, 2019
Description: this file contains a request to the cakes, cookies & desserts
category in Costco Groceries. There is only one request because there is only
one page of items. The file then parses it using bs4 and prints results to
terminal.
"""
import requests
import urllib.request
from bs4 import BeautifulSoup
import re
#imported re for regular expressions

url = 'https://www.costco.com/cakes-cookies.html'
headers = {'User-Agent':'Wget/1.11.4', 'Accept':'*/*', 'Connection':'Keep-Alive'}
r = requests.get(url, headers=headers)

# r.text contains the html code associated with this url
soup = BeautifulSoup(r.text, 'html.parser')
#print(soup.prettify())
print(soup.title.get_text())

#create a name list to hold product names
names = []
#create prices list
prices = []

#get names and store into names list
for link in soup.find_all(href=re.compile("www.costco.com(.*).product.1(.*)html")):
    #print('\n');
    names.append(link.get_text())
    #print(link.get_text())

#get prices and store into prices list
for priceTag in soup.find_all("div", class_="price"):
    #print(priceTag.get_text())
    prices.append(priceTag.get_text())

#print out names and prices
for i in range(len(names)):
    print(names[i])
    print(prices[i])

#print(names)
#print(prices)
