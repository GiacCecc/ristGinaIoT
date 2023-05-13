
# umongo.py - v 0.01
#
# MongoDB Data API
#
# Giacomo Ceccarelli
# Berlin, 07.05.2023
# ---------------------------------------------------------

import urequests as requests
import json

from libs.uutil import print_response_info

from utils.secrets import DEVICE_ID, MONGO_APP_ID, MONGO_API_KEY, MONGO_SRC


# Data API url endpoints
actions = {
    'FIND_ONE'    : 'https://data.mongodb-api.com/app/{}/endpoint/data/v1/action/findOne'.format(MONGO_APP_ID),
    'FIND'        : 'https://data.mongodb-api.com/app/{}/endpoint/data/v1/action/find'.format(MONGO_APP_ID),
    'INSERT_ONE'  : 'https://data.mongodb-api.com/app/{}/endpoint/data/v1/action/insertOne'.format(MONGO_APP_ID),
    'INSERT_MANY' : 'https://data.mongodb-api.com/app/{}/endpoint/data/v1/action/insertMany'.format(MONGO_APP_ID),
    'UPDATE_ONE'  : 'https://data.mongodb-api.com/app/{}/endpoint/data/v1/action/updateOne'.format(MONGO_APP_ID),
    'UPDATE_MANY' : 'https://data.mongodb-api.com/app/{}/endpoint/data/v1/action/updateMany'.format(MONGO_APP_ID),
    'REPLACE_ONE' : 'https://data.mongodb-api.com/app/{}/endpoint/data/v1/action/replaceOne'.format(MONGO_APP_ID),
    'DELETE_ONE'  : 'https://data.mongodb-api.com/app/{}/endpoint/data/v1/action/deleteOne'.format(MONGO_APP_ID),
    'DELETE_MANY' : 'https://data.mongodb-api.com/app/{}/endpoint/data/v1/action/deleteMany'.format(MONGO_APP_ID),
    'AGGREGATE'   : 'https://data.mongodb-api.com/app/{}/endpoint/data/v1/action/aggregate'.format(MONGO_APP_ID)
}

HEADERS = {'Content-Type': 'application/json',
           'Access-Control-Request-Headers': '*',
           'api-key': MONGO_API_KEY}   # print(HEADERS)


# BASE REQUESTS
# ------------------------------------------------------------------------

def mrequest(action, data, pprint=True):
    url = actions[action]
    response = requests.request("POST", url, headers=HEADERS, data=data)
    if pprint:
        print_response_info(response)
        
    return response

def findOne(data, pprint=False):
    r = mrequest('FIND_ONE', data, pprint=pprint)
    return r

def find(data, pprint=False):
    r = mrequest('FIND', data, pprint=pprint)
    return r

def insertOne(data, pprint=False):
    r = mrequest('INSERT_ONE', data, pprint=pprint)
    return r

def insertMany(data, pprint=False):
    r = mrequest('INSERT_MANY', data, pprint=pprint)
    return r

def updateOne(data, pprint=False):
    r = mrequest('UPDATE_ONE', data, pprint=pprint)
    return r

def updateMany(data, pprint=False):
    r = mrequest('UPDATE_MANY', data, pprint=pprint)
    return r

def replaceOne(data, pprint=False):
    r = mrequest('REPLACE_ONE', data, pprint=pprint)
    return r

def deleteOne(data, pprint=False):
    r = mrequest('DELETE_ONE', data, pprint=pprint)
    return r

def deleteMany(data, pprint=False):
    r = mrequest('DELETE_MANY', data, pprint=pprint)
    return r

# TODO::: Something doesn´t work with MongoDB Aggregation
def aggregate(data, pprint=False):
    r = mrequest('AGGREGATE', data, pprint=pprint)
    return r


# PROJECT ORIENTED FUNCTIONS
# ------------------------------------------------------------------------
def get_OTA_TRIGGER(pprint=False):
    payload = json.dumps( { "dataSource": MONGO_SRC.dataSource,
                            "database":   MONGO_SRC.database,
                            "collection": MONGO_SRC.Collections.configSet,
                            "filter": { "configType" : "OTA Update" },
                            "projection" : { "OTA_TRIGGER": 1, "_id": 0 } } )
    
    r = findOne(data=payload, pprint=pprint)
    OTA_TRIGGER = json.loads(r.text)['document']['OTA_TRIGGER']
    r.close()
    return OTA_TRIGGER


def update_OTA_TRIGGER(value=False, pprint=False):
    # ------------------ UPDATE
    payload_updateOne = json.dumps({"dataSource": MONGO_SRC.dataSource,
                                    "database":   MONGO_SRC.database,
                                    "collection": MONGO_SRC.Collections.configSet,
                                    "filter": { "configType" : "OTA Update" },
                                    "update": { "$set": { "OTA_TRIGGER": value } } } )
    
    response_update = updateOne(data=payload_updateOne, pprint=pprint)
    response_update.close()


def insert_temp(temp, pprint=False):
    # ------------------------------------ INSERT
    payload_insertOne = json.dumps( { "dataSource": MONGO_SRC.dataSource,
                                      "database":   MONGO_SRC.database,
                                      "collection": MONGO_SRC.Collections.logs,
                                      "document": { "deviceId": DEVICE_ID,
                                                    "logTime": "-",
                                                    "temp": temp,
                                                    "unit": "Celsius",
                                                    "nodeId": "DS18B20",
                                                    "dataType": "Temperature" } } )
    response_insert = insertOne(data=payload_insertOne, pprint=pprint)
    response_dict = json.loads(response_insert.text)
    response_insert.close()
    # ------------------ UPDATE with $currentDate
    payload_updateOne = json.dumps({"dataSource": MONGO_SRC.dataSource,
                                    "database":   MONGO_SRC.database,
                                    "collection": MONGO_SRC.Collections.logs,
                                    "filter": { "_id": { "$oid": str(response_dict['insertedId'] ) } },
                                    "update": { "$currentDate": { "logTime": { "$type": "date" } } } } )
    
    response_update = updateOne(data=payload_updateOne, pprint=pprint)
    response_update.close()



def insert_error(err_str, pprint=False):
    # ------------------------------------ INSERT
    payload_insertOne = json.dumps({"dataSource": MONGO_SRC.dataSource,
                                    "database":   MONGO_SRC.database,
                                    "collection": MONGO_SRC.Collections.errors,
                                    "document": { "deviceId": DEVICE_ID,
                                                  "errTime": "-",
                                                  "errStr": err_str } } )
    response_insert = insertOne(data=payload_insertOne, pprint=pprint)
    response_dict = json.loads(response_insert.text)
    response_insert.close()
    # ------------------ UPDATE with $currentDate
    payload_updateOne = json.dumps({"dataSource": MONGO_SRC.dataSource,
                                    "database":   MONGO_SRC.database,
                                    "collection": MONGO_SRC.Collections.errors,
                                    "filter": { "_id": { "$oid": str(response_dict['insertedId'] ) } },
                                    "update": { "$currentDate": { "errTime": { "$type": "date" } } } } )
    response_update = updateOne(data=payload_updateOne, pprint=pprint)
    response_update.close()



def insert_msg(msg, pprint=False):
    # ------------------------------------ INSERT
    payload_insertOne = json.dumps({"dataSource": MONGO_SRC.dataSource,
                                    "database":   MONGO_SRC.database,
                                    "collection": MONGO_SRC.Collections.messages,
                                    "document": { "deviceId": DEVICE_ID,
                                                  "msgTime" : "-",
                                                  "msgStr": msg } } )
    response_insert = insertOne(data=payload_insertOne, pprint=pprint)
    response_dict = json.loads(response_insert.text)
    response_insert.close()
    # ------------------ UPDATE with $currentDate
    payload_updateOne = json.dumps({"dataSource": MONGO_SRC.dataSource,
                                    "database":   MONGO_SRC.database,
                                    "collection": MONGO_SRC.Collections.messages,
                                    "filter": { "_id": { "$oid": str(response_dict['insertedId'] ) } },
                                    "update": { "$currentDate": { "msgTime": { "$type": "date" } } } } )
    
    response_update = updateOne(data=payload_updateOne, pprint=pprint)
    response_update.close()



def insert_update(pprint=False):
    # ------------------------------------ INSERT
    payload_insertOne = json.dumps({"dataSource": MONGO_SRC.dataSource,
                                    "database":   MONGO_SRC.database,
                                    "collection": MONGO_SRC.Collections.updates,
                                    "document": { "deviceId": DEVICE_ID,
                                                  "updateTime" : "-",
                                                  "updateStr": "Software has been updated" } } )
    response_insert = insertOne(data=payload_insertOne, pprint=pprint)
    response_dict = json.loads(response_insert.text)
    response_insert.close()
    # ------------------ UPDATE with $currentDate
    payload_updateOne = json.dumps({"dataSource": MONGO_SRC.dataSource,
                                    "database":   MONGO_SRC.database,
                                    "collection": MONGO_SRC.Collections.messages,
                                    "filter": { "_id": { "$oid": str(response_dict['insertedId'] ) } },
                                    "update": { "$currentDate": { "updateTime": { "$type": "date" } } } } )
    
    response_update = updateOne(data=payload_updateOne, pprint=pprint)
    response_update.close()



def last_log(collection, field, pprint=False):
    payload = json.dumps( {
        "dataSource": MONGO_SRC.dataSource,
        "database":   MONGO_SRC.database,
        "collection": collection,
        "filter": { },
        "sort": {"_id": -1},
        "projection": { field: 1, "_id": 0 },
        "limit": 1 } )
    
    r = find(data=payload, pprint=pprint)
    r_dict = json.loads(r.text)
    r.close()
    return r_dict['documents'][0][field]

def last_nlogs(collection, nlogs, field, pprint=False):
    payload = json.dumps( {
        "dataSource": MONGO_SRC.dataSource,
        "database":   MONGO_SRC.database,
        "collection": collection,
        "filter": { },
        "sort": { "_id": -1 },
        "projection": { field: 1, "_id": 0 },
        "limit": nlogs } )
    
    r = find(data=payload, pprint=pprint)
    r_dict = json.loads(r.text)
    r.close()
    fields = [doc[field] for doc in r_dict['documents']]
    return fields
