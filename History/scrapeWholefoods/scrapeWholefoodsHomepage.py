"""
Filename: scrapeWholefoodsHomepage.py
Author: Vivian Wei
Date: February 28th, 2019
Description: this file scrapes wholefoods category urls from the homepage.
It uses selenium to accomplish this. Furthermore, this file is split into
functions for easy use later on.
"""
from selenium import webdriver
import requests
import urllib.request
from bs4 import BeautifulSoup
import re

"""
main calls getURLs to get a list of URLs
"""
def main():
    myURLs = getWholefoodsURLs()
    print(myURLs)

#-------------------------getting urls from homepage---------------------------
"""
getWholefoodsURLs returns a list of URLS
"""
def getWholefoodsURLs():

    #create a headless chrome
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    # options.add_argument('dump-dom')
    options.add_argument('disable-dev-shm-usage')
    options.add_argument('remote-debugging-port=8080')

    #create chrome webdriver that goes to groceries homepage
    browser = webdriver.Chrome(chrome_options=options)
    url = 'https://products.wholefoodsmarket.com/categories'
    browser.get(url)

    #assign the page source to html and create soup with it
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

#call main
main()
