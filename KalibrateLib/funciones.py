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

def getColumnsPrice(rawdata):
    extracted_data=[]
    for item in rawdata:
        data_dic ={
           "priceId":item['data'].get('priceId'),
           "effectiveTime": item['data'].get("effectiveTime"),
           "idProduct": item['data']['product'].get('entityId'),
           "origin":item['data'].get("origin"),
           "price":item['data'].get("price")
        }
        extracted_data.append(data_dic)
    return extracted_data

def getColumnsArea(rawdata):
    extracted_data =[]
    for item in rawdata:
        data_dic ={
            "areaId":item['data'].get('areaId'),
            "entityId":item['id'].get('entityId'),
            "name":item['data'].get('name'),
            "_ts":item['id'].get('_ts')
        }
        extracted_data.append(data_dic)
    return extracted_data

def getColumnsVolumen(rawdata):
    extracted_data =[]
    for item in rawdata:
        data_dic={
            "idVolume":item['id'].get('entityId'),
            "idProduct":item['data']['product'].get('entityId'),
            "volume":item['data'].get('volume'),
            "startTime":item['data'].get('startTime'),
            "_ts":item['id'].get('_ts')

        }

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
        data_dic = {
            "EntityId": item.get("id", {}).get("entityId", None),
            "Adress": item.get('data', {}).get('address', None),
            "Adress2": item.get('data', {}).get('address2', None),
            "Adress3": item.get('data', {}).get('address3', None),
            "Adress4": item.get('data', {}).get('address4', None),
            "networkId": item.get('data', {}).get('network', {}).get('entityId', None),  # Maneja el caso cuando 'network' no existe
            "Latitud": item.get('data', {}).get('latitude', None),
            "Longitud": item.get('data', {}).get('longitude', None),
            "name": item.get('data', {}).get('name', None),
            "achievedVolume": item.get('data', {}).get('achievedVolume', None),
            "areaEntityId": item.get('data', {}).get('area', {}).get('entityId', None),
            "brandEntityId": item.get('data', {}).get('brand', {}).get('entityId', None),
            "channelOfTradeEntityId": item.get('data', {}).get('channelOfTrade', {}).get('entityId', None),
            "distanceToNearestOwnSite": item.get('data', {}).get('distanceToNearestOwnSite', None),
            "SiteType2": item.get("id", {}).get("entityVariant", None)
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