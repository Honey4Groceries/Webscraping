import json
def main(event, context):
    response = {
        "headers": {'Content-Type': 'application/json'},
        "isBase64Encoded": False,
        "statusCode": 200,
        "body": json.dumps(normalize_data(event))
    }
    return response

def normalize_data(jsonData):
    #create a list to store normalized products
    clean_list = []
    #load json from request body key that contains json string
    myJson = json.loads(jsonData['body'])
    #normalize each product
    for product in myJson['data']:
        #create a json
        clean_product = {
        "product_name": product['name'],
        "price": product['store']['price'],
        "categories": product['categories'],
        "serving_info": product['servingInfo']
        }
        #add it to clean_list
        clean_list.append(clean_product)
    return clean_list

"""for testing
with open('example.json', 'r') as myfile:
    myJsonData=myfile.read()
obj = json.loads(myJsonData)
returnObj = normalize_data(obj)

with open('data.txt', 'w') as outfile:  
    json.dump(returnObj, outfile)
"""






