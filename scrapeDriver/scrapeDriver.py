from selenium import webdriver
from bse4 import BeautifulSoup

class scrapeDriver:
        #Constructor with URL, desired capabilities=False
        def __init__(self, enable_logging=False):

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
            if enable_logging:
                    desired_capabilities = webdriver.DesiredCapabilities.CHROME.copy()
                    desired_capabilities['loggingPrefs'] = {'performance': 'INFO'}
                    self.driver = webdriver.Chrome('/opt/chromedriver', 
                            chrome_options=options, desired_capabilities=desired_capabilities)
            else:
                    self.driver = webdriver.Chrome('/opt/chromedriver', chrome_options=options)

    def get(self, url):
            assert self.driver
            try:
                    self.driver.get(url)
            except Exception as error:
                    console.log("Error getting url")
                    raise error

    def getPageSource(self):
            assert self.driver
            return self.driver.page_source

    def quit(self):
            assert self.driver
            try:
                    self.driver.quit()
            except Exception as error:
                    console.log('Error quitting driver')
                    raise error

    def infiniteScroll(self, sleep_time=0.5):
            """
            Infinitely scroll down on page until the page can no longer scroll.
            
            Arguments:
                self {scrapeDriver} -- scrapeDriver to be scrolled down on
                double {scrapeDriver} -- time to pause between each scroll
            """
            assert self.driver
        
            last_height = self.driver.execute_script(
                "return document.documentElement.scrollHeight")

            while True:
                    # execute js to scroll
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
                    time.sleep(sleep_time)

                    # Calculate new scroll height and compare with last scroll height
                    new_height = self.driver.execute_script(
                        "return document.documentElement.scrollHeight")

                    if new_height == last_height:
                            return

                    last_height = new_height            
