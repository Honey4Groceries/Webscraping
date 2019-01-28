
from selenium import webdriver

browser = webdriver.Chrome()
url = "https://shop.vons.com/aisles/bread-bakery/bakery-bread.2118.html"
browser.get(url)

zipcode = browser.find_element_by_id("zipcode") #username form field

zipcode.send_keys("92122")

getStartedButton = browser.find_element_by_css_selector \
("#zipcodeform > input.btn.btn-default")
getStartedButton.click()

#if comment next line out is able to get into home page
browser.get("https://shop.vons.com/aisles/bread-bakery/bakery-bread.2118.html")
