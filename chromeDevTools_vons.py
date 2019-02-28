import time
from selenium import webdriver
import pychrome
import json

requestIDs= []
data = []
url = 'https://shop.vons.com/aisles/bread-bakery/bakery-bread.2832.html?zipcode=91007'

desired_capabilities = webdriver.DesiredCapabilities.CHROME.copy()
desired_capabilities['loggingPrefs'] = {'performance': 'INFO'}

options = webdriver.ChromeOptions()

options.add_argument('headless')
options.add_argument('single-process')
options.add_argument('disable-dev-shm-usage')
options.add_argument('no-sandbox')
options.add_argument('homedir=/tmp')
options.add_argument('data-path=/tmp/data-path')
options.add_argument('disk-cache-dir=/tmp/cache-dir')

driver = webdriver.Chrome(chrome_options=options, desired_capabilities=desired_capabilities)
driver.command_executor._commands.update({'getLog': ('POST', '/session/$sessionId/log')})

driver.get(url)
logs = driver.execute('getLog', {'type': 'performance'})['value']
for log in logs:
    parsed_log = json.loads(log['message'])['message']
    if parsed_log['method'] == "Network.requestWillBeSent":
        if 'aemaisle' in parsed_log['params']['request']['url']:
            requestIDs.append(parsed_log['params']['requestId'])

for requestID in requestIDs:
    data.append(json.loads(driver.execute_cdp_cmd('Network.getResponseBody', {'requestId':requestID})['body'])))

print(data)


# def request_will_be_sent(**kwargs):
#     if 'aemaisle' in kwargs.get('request').get('url'):
#         requestIDs.append(kwargs.get('requestId'))

# url = 'https://shop.vons.com/aisles/bread-bakery/bakery-bread.2832.html?zipcode=91007'

# options = webdriver.ChromeOptions()

# options.add_argument('headless')

# desired_capabilities = webdriver.DesiredCapabilities.CHROME.copy()
# desired_capabilities['loggingPrefs'] = {'performance': 'INFO'}

# driver = webdriver.Chrome(chrome_options=options, desired_capabilities=desired_capabilities)

# driver.execute_cdp_cmd('Network.enable', {})

# driver.command_executor._commands.update({'getLog': ('POST', '/session/$sessionId/log')})

# driver.get(url)

# logs = driver.execute('getLog', {'type': 'performance'})['value']
# for log in logs:
#     parsed_log = json.loads(log['message'])['message']
#     if parsed_log['method'] == "Network.requestWillBeSent":
#         if 'aemaisle' in parsed_log['params']['request']['url']:
#             print(parsed_log['params']['request'])
#             requestIDs.append(parsed_log['params']['requestId'])

# for requestID in requestIDs:
#     print(json.dumps(json.loads(driver.execute_cdp_cmd('Network.getResponseBody', {'requestId':requestID})['body']), indent=4))


# driver.quit()
# # return 1

# # tab = browser.new_tab()

# # tab.set_listener('Network.requestWillBeSent', request_will_be_sent)

# # tab.start()
# # tab.call_method('Network.enable')
# # tab.call_method('Page.navigate', url=url, _timeout=10)

# # tab.wait(10)

# # for requestID in requestIDs:
# #     print(json.dumps(json.loads(tab.call_method('Network.getResponseBody', requestId=requestID)['body']), indent=4))
# # tab.stop()

# # driver.quit()
