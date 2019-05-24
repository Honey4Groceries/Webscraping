import requests
import json

with open('example.json', 'r') as myfile:
    myJsonData=myfile.read()
myJson = json.loads(myJsonData)

response = requests.post(url='https://zq06asxiqc.execute-api.us-east-1.amazonaws.com/dev/normalize', json=myJson)

print(response.text)