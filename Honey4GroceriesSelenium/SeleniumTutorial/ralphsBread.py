from selenium import webdriver

browser = webdriver.Chrome()
url = "https://www.ralphs.com/pl/bakery-bread/01002"
browser.get(url)




broswer.execute_script()


#probably because there is no header
#note it is hard to have a header in chrome so may do firefox browser instead
#however firefox needs gecko webdriver (which is a pain to install i think)
#and also needs to add extension
#will maybe check on this?
