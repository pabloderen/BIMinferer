from pymongo import MongoClient
import pandas as pd


client = MongoClient('localhost', 27017)
db = client['bimferer']
collection_models = db['models']



def savetoDataBase(object):
    df = pd.json_normalize(object).to_dict("records")
    #sanitaze jsons
    dicto =   []
    for e in df:
        newElement = {}
        for key in e:
            newElement[key.replace(".","_")] = e[key]
        dicto.append(newElement)

    collection_models.insert_many(dicto)
    return True
