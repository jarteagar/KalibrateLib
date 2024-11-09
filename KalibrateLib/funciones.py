import requests
import json

def getToken(client_id,client_secret,scope,auth_url):

    post_body = {
        'client_id': client_id,
        'client_secret': client_secret,
        'scope': scope,
        'grant_type': 'client_credentials'
    }

    response = requests.post(auth_url, data=post_body)
    token = response.json().get('access_token')
    return token

def getData(urlApi,urlFilter,token):

    authHeader = {"Authorization": "Bearer %s" %token, 'User-Agent': 'API-CLIENT'}
    queryURL = f'https://eu2.data.kalibrate.cloud{urlApi}{urlFilter}'
    response = requests.get(queryURL,headers=authHeader)

    if response.status_code != 200:
        return ""
    else:
        rawdata = json.loads(response.text)
        return rawdata

def getColumnsProd(rawdata):
    #selecciona unas columnas de toda la cadena de api
    extracted_data = []
    for item in rawdata:  
        data_dict = {
            "OwnProductId": item["data"].get("ownProductId"),
            "EntityId": item["id"].get("entityId"),
            "GlobalProductEntityId": item["data"]["product"].get("entityId"),
            "SiteId": item["data"]["site"].get("entityId")
        }
        extracted_data.append(data_dict)
    return extracted_data

def getColumnsGlobal(rawdata):
    #selecciona unas columnas de toda la cadena de api
    extracted_data = []
    for item in rawdata:  
        data_dict = {
            "GlobalProductId": item["data"].get("globalProductId"),
            "EntityId": item["id"].get("entityId"),
            "ProductName": item["data"].get("name")
        }
        extracted_data.append(data_dict)
    return extracted_data
