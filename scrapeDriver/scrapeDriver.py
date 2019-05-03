from selenium import webdriver
from bse4 import BeautifulSoup

class scrapeDriver:
		#Constructor with URL, desired capabilities=False
		def __init__(self, desired_capabilities=False):
      	self.url = url

      	#Add all chrome options
      	options = webdriver.ChromeOptions()
      	options.binary_location = '/opt/headless-chromium'
      	options.add_argument('headless')
      	options.add_argument('single-process')
      	options.add_argument('disable-dev-shm-usage')
      	options.add_argument('no-sandbox')
      	options.add_argument('homedir=/tmp')
      	options.add_argument('data-path=/tmp/data-path')
      	options.add_argument('disk-cache-dir=/tmp/cache-dir')

      	#Add the additional desired_capabilities in if the optional param is true
      	if desired_capabilities:
      			desired_capabilities = webdriver.DesiredCapabilities.CHROME.copy()
      			desired_capabilities['loggingPrefs'] = {'performance': 'INFO'}
      			self.driver = webdriver.Chrome('/opt/chromedriver', 
      					chrome_options=options, desired_capabilities=desired_capabilities)
      	else:
      			self.driver = webdriver.Chrome('/opt/chromedriver', chrome_options=options)

    def get(self, url):
    		try:
    				self.browser.get(url)
    		except:
    				print('Error running driver.get() on the input URL')
    				traceback.print_exc()

    def pageSource(self):
    		return self.browser.page_source

    def quit(self):
        if self.driver:
            try:
    		        self.browser.quit()
            except:
                print('Error quitting driver')
                traceback.print_exc()
        else:
            print('Driver does not exist or has already quitted')

    def scroll(self):
		    """scroll down on page 
		    
		    Arguments:
		        self {scrapeDriver} -- scrapeDriver to be scrolled down on
		    """

        
		    last_height = self.driver.execute_script(
            "return document.documentElement.scrollHeight")

		    while True:
		        # execute js to scroll
		        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
		        time.sleep(.5)

		        # Calculate new scroll height and compare with last scroll height
		        new_height = self.driver.execute_script(
		        		"return document.documentElement.scrollHeight")

		        if new_height == last_height:
		            return

		        last_height = new_height    		
