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


#def getSubData(urlApi,token):
#    authHeader = {"Authorization": "Bearer %s" %token, 'User-Agent': 'API-CLIENT'}
#    queryURL = f'https://eu2.data.kalibrate.cloud{urlApi}'
#    response = requests.get(queryURL,headers=authHeader)

#    if response.status_code != 200:
#        return ""
#    else:
#        rawdata = json.loads(response.text)
#        return rawdata

def getSubData(urlApi, token):
    authHeader = {"Authorization": "Bearer %s" % token, 'User-Agent': 'API-CLIENT'}
    queryURL = f'https://eu2.data.kalibrate.cloud{urlApi}'
    response = requests.get(queryURL, headers=authHeader)

    if response.status_code != 200:
        print(f"Error {response.status_code}: No se pudo obtener datos de {queryURL}")
        return {}  # Retornar un diccionario vacío en lugar de una cadena vacía
    else:
        try:
            return response.json()  # Usa .json() en lugar de json.loads(response.text)
        except json.JSONDecodeError as e:
            print(f"Error al decodificar JSON: {e}")
            return {}


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
            "SiteId": item["data"]["site"].get("entityId"),
            "active": 1 if item["data"].get("active",False) else 0, #nuevo
            "deleted": 1 if item["id"].get("deleted",False) else 0 #nuevo

        }
        extracted_data.append(data_dict)
    return extracted_data

#precios para el own
def getColumnsPrice(rawdata):
    extracted_data=[]
    for item in rawdata:
        data_dic ={
           "priceId":item['data'].get('priceId'),
           "effectiveTime": item['data'].get("effectiveTime"),
           "idProduct": item['data']['product'].get('entityId'),
           "origin":item['data'].get("origin"),
           "price": float(item['data'].get("price", 0)) if item['data'].get("price") is not None else None
        }
        extracted_data.append(data_dic)
    return extracted_data

#precios para el competitor
def getColumnsPriceCom(rawdata):
    extracted_data=[]
    for item in rawdata:
        data_dic ={
           "priceId":item['data'].get('priceId'),
           "effectiveTime": item['data'].get("effectiveTime"),
           "idProduct": item['data']['product'].get('entityId'),
           "origin":item['data'].get("origin"),
           "price": float(item['data'].get("price", 0)) if item['data'].get("price") is not None else None,
           "site":item['data']['site'].get("entityId")
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
            "volume": float(item['data'].get("volume", 0)) if item['data'].get("volume") is not None else None,
            #"volume":item['data'].get('volume'),
            "startTime":item['data'].get('startTime'),
            "_ts":item['id'].get('_ts')

        }
        extracted_data.append(data_dic)
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
            "SiteType2": item.get("id", {}).get("entityVariant", None),
            "importCode": item.get('data', {}).get('importCode', None),  #nuevo atributo solicitado 27.03.2025
            "deleted": 1 if item.get('id', {}).get('deleted', False) else 0 #nuevo
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
                    "siteGroupingValueId":item3.get('siteGroupingValueId'),
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


#se modifico esta funcion para ajustar la data del id correcto del Competitor respecto al Own
def getColumnsSiteOwn(rawdata,token):
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
            "SiteType2": item.get("id", {}).get("entityVariant", None),
            "importCode":item.get('data', {}).get('importCode', None), #este dato antes conversaba con el SITEID
            "gpcGroup":item.get('data', {}).get('gpcGroup', None),
            "deleted": 1 if item.get('id', {}).get('deleted', False) else 0,
            "sapSiteId":None
            #"deleted":item.get('id', {}).get('deleted', None) ##nuevo
        }

        #codigo DANAUS(SITEIDSAP)
        rawdata4 = item['data'].get('alternateImportCodes')
        if rawdata4:
            for item3 in rawdata4:
                url_reference = f"/api/{item3.get('reference')}"
         
                #obteniendo el siteidsap
                rawdata5 = getSubData(url_reference,token)
                
                # Verifica que rawdata3 es un diccionario antes de acceder
                if isinstance(rawdata5, dict) and isinstance(rawdata5.get('data'), dict):
                    SiteIdsap_ = rawdata5['data'].get('importCode', {})
                    data_dic["sapSiteId"] = SiteIdsap_

        #SITES DE COMPETIDORES
        rawdata2 = item['data'].get('competitorSites',{})
        if rawdata2:

            for item2 in rawdata2:
                data_dic2 ={
                    "EntityId":id_,
                    "competitorEntityId":item2.get('entityId'), #solo sirve para usar el endpoint de referncia
                    "competitorSitesId":None, #aqui pondremos el idsite que si conversa con la maestra de competitors
                    "distance":None, #nuevo 27.03.25
                    "distanceUnit":None #nuevo 27.03.25
                }

                url_reference = f"/api/{item2.get('reference')}"

                #obteniendo el idsite del competitor
                rawdata3 = getSubData(url_reference,token)

                # Verifica que rawdata3 es un diccionario antes de acceder
                if isinstance(rawdata3, dict) and isinstance(rawdata3.get('data'), dict):
                    SiteId_ = rawdata3['data'].get('competitorSite', {})

                    distance_ = rawdata3['data'].get('distance', None)
                    distanceUnit_  = rawdata3['data'].get('distanceUnit', None)

                    #delta_  = rawdata3['data'].get('delta', None)
                    #marginDelta_  = rawdata3['data'].get('marginDelta', None)
                    #edlDelta_  = rawdata3['data'].get('edlDelta', None)
                    #nmDelta_  = rawdata3['data'].get('nmDelta', None)

                    SiteId = SiteId_.get('entityId', None)
                    data_dic2["competitorSitesId"] = SiteId

                    #nuevo: 28.03.25 completando datos de distancia y margenes
                    data_dic2["distance"] = distance_ 
                    data_dic2["distanceUnit"] = distanceUnit_ 
                    #data_dic2["delta"] = delta_ 
                    #data_dic2["marginDelta"] = marginDelta_ 
                    #data_dic2["edlDelta"] = edlDelta_ 
                    #data_dic2["nmDelta"] = nmDelta_ 

         

        #        SiteId_ = rawdata3['data'].get('competitorSite',{})
        #        SiteId = SiteId_.get('entityId',None)
        #        data_dic2["competitorSitesId"] = SiteId 


                extracted_comp_sites.append(data_dic2)

        #GRUPOS
        rawdata3 = item['data'].get('siteGroupings')
        if rawdata3:
            for item3 in rawdata3:
                data_dic3 ={
                    "EntityId":id_,
                    "siteGroupingValueId":item3.get('siteGroupingValueId'),
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

#main marker y alternative marker esta en esta maestra de grupos
def getColumnsProductsGroup(rawdata):
    #selecciona unas columnas de toda la cadena de api
    extracted_data = []
    for item in rawdata:  
        data_dict = {
            "EntityId": item["id"].get("entityId"),
            "entityVariant": item["id"].get("entityVariant"), #own / COMPETITOR
            "ownProductGroupId": item["data"].get("ownProductGroupId"),
            "includeInOptimise": 1 if item["data"].get("includeInOptimise",False) else 0, #nuevo - optimizacion
            "globalProductGroupId": item["data"].get("globalProductGroupId"),
            "ownSiteId": item.get("data", {}).get("ownSite", {}).get("entityId", None), #id del own
            "alternativeMainMarker": item.get("data", {}).get("alternativeMainMarker", {}).get("entityId", None), #id competitor -alternative marker
            "ownSiteCompetitor": item.get("data", {}).get("ownSiteCompetitor", {}).get("entityId", None), #id competitor - marker
            "autoImplement": 1 if item["data"].get("autoImplement",False) else 0, #item["data"].get("autoImplement"),
            "active": 1 if item["data"].get("active",False) else 0
        }
        extracted_data.append(data_dict)
    return extracted_data