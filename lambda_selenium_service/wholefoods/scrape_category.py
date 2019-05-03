from selenium import webdriver
from urllib import parse
import requests
import time
import json
from urllib.parse import urlparse

def main(event, context):
    if 'queryStringParameters' not in event.keys() or 'url' not in event['queryStringParameters'].keys():
        failedResponse = {
            "headers": {'Content-Type': 'application/json'},
            "isBase64Encoded": False,
            "statusCode": 406,
            "body": json.dumps({"data": 'URL must be specified!',"store": "Wholefoods","url": []})
        }
        return failedResponse

    url = event['queryStringParameters']['url']

    product_data = scrape_category(url)
    #print(product_data)
    response = {
        "headers": {'Content-Type': 'application/json'},
        "isBase64Encoded": False,
        "statusCode": 200,
        "body": json.dumps({"data": product_data,"store": "Wholefoods","url": url})
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
        #update url
        parsedDict = parse.parse_qs(url)
        parsedDict['skip'] = [str(skip)]
        url = parse.urlencode(parsedDict)
        url = parse.unquote(url)
        #get next page
        info = requests.get(url, headers=headers)
        loaded_json = json.loads(info.text)
        load_more = loaded_json["hasLoadMore"]
        print("actual return = "+ str(loaded_json["hasLoadMore"]))
        print("load_more = " + str(load_more))
        #add the jsons to the data list
        data.extend(loaded_json["list"])

    return data
