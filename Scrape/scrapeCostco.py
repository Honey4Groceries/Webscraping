import requests
import urllib.request
from bs4 import BeautifulSoup

url = 'https://www.costco.com/cakes-cookies.html'
headers = {'User-Agent':'Wget/1.11.4', 'Accept':'*/*', 'Connection':'Keep-Alive'}
r = requests.get(url, headers=headers)

# r.text contains the html code associated with this url
soup = BeautifulSoup(r.text, 'html.parser')
# print(soup.prettify())

