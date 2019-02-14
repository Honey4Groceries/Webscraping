"""
Filename: scrapeHomepage.py
Author: Vivian Wei
Date: February 5th, 2019
Description: this file contains a request to the homepage
category in Costco Groceries. There is only one request because there is only
one page of items. The file then parses it using bs4 and prints results to
terminal.
"""
from selenium import webdriver
import requests
import urllib.request
from bs4 import BeautifulSoup
import re
#imported re for regular expressions

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

print(urls)

#quit browser
browser.quit()




