
from selenium import webdriver

browser = webdriver.Chrome()
url = "https://www.costco.com/cakes-cookies.html"
browser.get(url)

items = browser.find_elements_by_class_name("product")

text_file = open("output.txt", "w")

for x in range (0, len(items)):
    element_name = items[x].find_element_by_class_name("description")
    element_price = items[x].find_element_by_class_name("price")

    text_file.write("%s\n" % element_name.text)
    text_file.write("%s\n" % element_price.text)
    text_file.write("\n")
