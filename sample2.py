"""
    Module for scrapping pages.
    Read references first as they are helpful guide to building and expanding this module.

    Reference: https://morph.io/documentation/scraping_javascript_sites
    Reference: https://sites.google.com/a/chromium.org/chromedriver/getting-started
    More readings: https://medium.com/@hoppy/how-to-test-or-scrape-javascript-rendered-websites-with-python-selenium-a-beginner-step-by-c137892216aa
"""

from selenium import webdriver
import time
import json
import datetime


def get_produce_title(product) -> str:
    """ Returns the product title from WebElement of the product

    :param product:
    :return:
    """

    title = product.find_element_by_class_name("product-title")
    title_text = title.text
    return str(title_text)


def get_product_price(product) -> str:
    """ Returns the product price from WebElement of the product

    :param product:
    :return:
    """
    price_elem = product.find_element_by_class_name("product-price")
    price_text = price_elem.text
    price_str = str(price_text)
    return price_str


def create_product_dict(title_text, price_substr) -> dict:
    return {
        "productName": title_text,
        "priceInDollars": price_substr
    }


if __name__ == '__main__':

    """
        Specify the url that you want load. 
    """

    url = 'https://shop.vons.com/search-results.html?q=bread&zipcode=92122'

    """
        Set up driver for chrome. If error is thrown, check the guide. 
            See: https://sites.google.com/a/chromium.org/chromedriver/getting-started
    """

    driver = webdriver.Chrome('./chromedriver')
    driver.get(url)

    """
        Record source to page_source.html for debugging purposes
    """

    with open("page_source.html", "w") as file:
        html = driver.page_source
        file.write(html)

    """
        (Optional) wait 5 seconds
    """

    time.sleep(5)  # "Let the user actually see something!"

    """
        (Optional) Save a screenshot for debugging
    """

    # driver.get_screenshot_as_file("file2a.png")

    """
        Parse the elements in driver and save them to the list
    """

    products = list()

    product_col = driver.find_elements_by_tag_name("product-item")
    for product in product_col:
        """
            For each product-item, retrieve its price and title and more. 
            
            TODO: parse more fields
        """
        title_text = get_produce_title(product)
        price_str = get_product_price(product)
        price_substr = price_str.split("$")[1]
        products.append(create_product_dict(title_text, price_substr))

    """
        Print the product information to dict
    """

    print(products)

    """
        Find button that goes to the next page and click
        TODO: Implement and refactor so that the code reads the new page 
        
    """

    # Sample code for clicking next
    #   (does not work since it's written with another library, adapt to selenium first)
    # submit the search form...
    #     button = browser.find_by_css("button[type='submit']")
    #     button.click()

    """
        Save products as JSON to file.
    """

    filename = str(datetime.datetime.now().timestamp()) + ".json"

    with open(filename, 'x') as outfile:
        """
        Note that the file must be empty
        """
        json.dump(products, outfile)
        print("Export to json successful. Filename: {}".format(filename))

    """
        Quit the driver/browser. 
    """

    driver.quit()
