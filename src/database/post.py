from pymongo import MongoClient
import pandas as pd


client = MongoClient('localhost', 27017)
db = client['bimferer']
collection_models = db['models']

def processObjectAsDictionary(object):
        #TODO process faster
        objAsDictionary = pd.json_normalize(object).to_dict("records")[0]
        d  =  {key.replace('.','_'): value for key, value in objAsDictionary.items()}
        return d


def savetoDataBase(jsonObject):

    processJsonObject = [processObjectAsDictionary(o) for o in jsonObject]


    collection_models.insert_many(processJsonObject)
    return True
