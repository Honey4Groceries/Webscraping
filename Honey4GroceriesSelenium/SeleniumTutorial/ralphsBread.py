from selenium import webdriver
from fake_useragent import UserAgent

# cookies = {'dtLatC': '1', 'dtPC': '4$206664633_783h-vIOMURKMCDFGGPAJILNAAFKEMHFHLKLOB',
#             'dtSa': '-', 'rxVisitor': '1548806664642Q7OQ0L2MOHKO5FOQOQQCKEODHVNRAN8K',
#             'rxvt': '1548808469921|1548806664647'}

cookies = {'ev_sync_dd': '20190130', 'everest_g_v2': 'g_surferid~XFDpPQAAD_u0aye-', 'everest_session_v2': 'XFDpPQAAD@u0bCe-'}


from selenium.webdriver.chrome.options import Options
# while True:
#     opts = Options()
#     ua = UserAgent()

#     opts.add_argument("user-agent="+ua.random)
    # browser = webdriver.Chrome(chrome_options=opts)
browser = webdriver.Chrome()



url = "https://www.ralphs.com"
url = "https://www.ralphs.com/pl/artisan-breads/14162"
browser.get(url)

#     for key, value in cookies.items():
#         browser.add_cookie({'name': key, 'value': value, 'path':'/'})

# browser.implicitly_wait(10)
# browser.refresh()

# url = "https://www.reddit.com"
# browser = webdriver.Chrome()
# browser.get(url)
# browser.implicitly_wait(2)
# browser.refresh()




# browser.execute_script()


#probably because there is no header
#note it is hard to have a header in chrome so may do firefox browser instead
#however firefox needs gecko webdriver (which is a pain to install i think)
#and also needs to add extension
#will maybe check on this?
# dtLatC 1
# dtPC 4$206664633_783h-vIOMURKMCDFGGPAJILNAAFKEMHFHLKLOB
# dtSa -
# rxVisitor 1548806664642Q7OQ0L2MOHKO5FOQOQQCKEODHVNRAN8K
# rxvt 1548808469921|1548806664647
