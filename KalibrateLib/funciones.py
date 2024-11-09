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

def getColumnsSite(rawdata):
    extracted_data = []
    

    for item in rawdata:
        id_ = item["id"].get("entityId") #id para las subtablas competitors sites y groupings
        extracted_comp_sites =[]
        extracted_comp_groups =[]
        data_dic ={
            "EntityId":item["id"].get("entityId"),
            "Adress":item['data'].get('address'),
            "Adress2":item['data'].get('address2'),
            "Adress3":item['data'].get('address3'),
            "Adress4":item['data'].get('address4'),
            "networkId":item['data']['network'].get('entityId'),
            "Latitud":item['data'].get('latitude'),
            "Longitud":item['data'].get('longitude'),
            "name":item['data'].get('name'),
            "achievedVolume":item['data'].get('achievedVolume'),
            "areaEntityId":item['data']['area'].get('entityId'),
            "brandEntityId":item['data']['brand'].get('entityId'),
            "channelOfTradeEntityId":item['data']['channelOfTrade'].get('entityId'),
            "distanceToNearestOwnSite":item['data'].get('distanceToNearestOwnSite'),
            "SiteType2":item['id'].get('entityVariant')
        }

        #SITES DE COMPETIDORES
        rawdata2 = item['data'].get('competitorSites')
        if rawdata2:
            for item2 in rawdata2:
                data_dic2 ={
                    "EntityId":id_,
                    "competitorSitesId":item2.get('entityId')
                }
                extracted_comp_sites.append(data_dic2)

        #GRUPOS
        rawdata3 = item['data'].get('siteGroupings')
        if rawdata3:
            for item3 in rawdata3:
                data_dic3 ={
                    "EntityId":id_,
                    "name":item3.get('name'),
                    "type":item3.get('type'),
                    "optionName":item3.get('optionName')
                }
                extracted_comp_groups.append(data_dic3)

        record = {
            "SiteInfo": data_dic,
            "CompetitorSites": extracted_comp_sites,
            "SiteGroupings": extracted_comp_groups
        }

        extracted_data.append(record)
    return extracted_data