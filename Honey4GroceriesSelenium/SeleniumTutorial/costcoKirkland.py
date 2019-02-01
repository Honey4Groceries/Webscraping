
from selenium import webdriver

# Navigate to url
browser = webdriver.Chrome()
url = "https://www.costco.com/kirkland-signature-groceries.html"
browser.get(url)

# Open text file for output
text_file = open("output.txt", "w")

# Container for page nav buttons
paging_elem = browser.find_element_by_class_name("paging")

# Each element labeled as a button
page_btns = paging_elem.find_elements_by_class_name("btn")


# Scrape items on the page
def scrapeItems():
    items = browser.find_elements_by_class_name("product")

    for x in range (0, len(items)):
        element_name = items[x].find_element_by_class_name("description")
        text_file.write("%s\n" % element_name.text)

        # Warehouse only products do not have a price listed
        try:
            element_price = items[x].find_element_by_class_name("price")
            text_file.write("%s\n" % element_price.text)
        except:
            text_file.write("Warehouse only -- No price listed\n")

        text_file.write("\n")


# Scrape first page of items
scrapeItems()
counter = 0

# Iterate through the rest of the pages
while 1:
    try:
        paging_elem = browser.find_element_by_class_name("paging")
        link = paging_elem.find_element_by_class_name("forward")
        link.click()
        counter = counter + 1
        scrapeItems()
    except:
        break
