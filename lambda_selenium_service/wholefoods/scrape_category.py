from selenium import webdriver
from urllib import parse
import requests
import time
import json
from urllib.parse import urlparse
from urllib.parse import quote

def main(event, context):
    if 'queryStringParameters' not in event.keys() or 'url' not in event['queryStringParameters'].keys():
        failedResponse = {
            "headers": {'Content-Type': 'application/json'},
            "isBase64Encoded": False,
            "statusCode": 406,
            "body": json.dumps({"store": "Wholefoods","url": [],"data": 'URL must be specified!'})
        }
        return failedResponse

    url = event['queryStringParameters']['url']

    if "https://products.wholefoodsmarket.com/api/search?" not in url: 
        failedResponse = {
            "headers": {'Content-Type': 'application/json'},
            "isBase64Encoded": False,
            "statusCode": 406,
            "body": json.dumps({"store": "Wholefoods","url": [],"data": 'invalid URL: URL must be Wholefoods URL!'})
        }
        return failedResponse

    product_data = scrape_category(url)
    #print(product_data)
    response = {
        "headers": {'Content-Type': 'application/json'},
        "isBase64Encoded": False,
        "statusCode": 200,
        "body": json.dumps({"store": "Wholefoods","url": url,"data": product_data})
    }

    return response

def scrape_category(url):

    data = []

    headers = {'User-Agent':'Wget/1.11.4', 'Accept':'*/*', 'Connection':'Keep-Alive'}

    # First page of data
    skip = 0
    info = requests.get(url, headers=headers)
    loaded_json = json.loads(info.text)
    load_more = True
    #add the jsons to the data list
    data.extend(loaded_json["list"])
    print(data)

    #while there is still data to scrape for that category
    while(load_more):
        #update skip
        skip = skip + 20
        #update url by putting it into a dictionary
        parsedDict = parse.parse_qs(url)
        parsedDict['skip'] = [str(skip)]
        #for each value in the dictionary, remove the brackets
        for item in parsedDict:
            parsedDict[item] = parsedDict[item][0]
        #put the url back together
        url=parse.urlencode(parsedDict)
        url=parse.unquote(url)
        #get next page
        info = requests.get(url, headers=headers)
        loaded_json = json.loads(info.text)
        load_more = loaded_json["hasLoadMore"]
        print(url)
        #add the jsons to the data list
        data.extend(loaded_json["list"])

    return data
