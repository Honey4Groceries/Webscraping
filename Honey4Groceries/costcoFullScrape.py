import requests
import urllib.request
from bs4 import BeautifulSoup

# text file for output
text_file = open("output.txt", "w")


def scrapeItems():
    productList = bsObj.findAll("div", {"class":"product"})

    if productList == None:
        print("products could not be found")
    else:
        for idx in range(0, len(productList)):
            product_name = productList[idx].find("p", {"class":"description"})
            text_file.write(product_name.text)

            try:
                product_price = productList[idx].find("div", {"class":"price"})
                text_file.write(product_price.text + "\n")
            except:
                text_file.write("Warehouse only -- No price listed.\n")

for link in links:
    # go to url using headers
    url = link
    headers = {'User-Agent':'Wget/1.11.4', 'Accept':'*/*', 'Connection':'Keep-Alive'}
    html = requests.get(url, headers=headers)

    # create a beautifulsoup object
    bsObj = BeautifulSoup(html.text, 'html.parser')

    scrapeItems()


    while 1:
        try:
            # next page button
            paging_elem = bsObj.find("li", {"class":"forward"})
            url = paging_elem.find("a")
            link = url.get('href')

            html = requests.get(link, headers=headers)
            bsObj = BeautifulSoup(html.text, 'html.parser')
            scrapeItems()
        except:
            break;
