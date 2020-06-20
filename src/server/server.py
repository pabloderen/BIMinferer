from flask import Flask, jsonify ,request
from bson import json_util, ObjectId
import json
app = Flask(__name__)
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['bimferer']
collection_models = db['models']

@app.route('/')
def hello_world():
    body = '''
    Return elements per category</br>
    /api/1/elements/$category </br></br>
    
    Return all MEP elements </br>
    /api/1/elements/mep</br>

    '''
    return body


@app.route('/api/1/elements/<string:category>', methods=['GET'])
def get_Category(category):
    result = collection_models.find({'Category': category})
    response = app.response_class(
        response=json_util.dumps(result),
        mimetype='application/json'
    )
    return response

@app.route('/api/1/elements/bycategories', methods=['GET', 'POST'])
def get_Categories():
    content = request.json
    if not content:
        return "Error in the json file"
    find = {}
    find['$or'] = []
    for category in content['categories']:
            find['$or'].append( {'Category':category})

    result = collection_models.find(find)
    response = app.response_class(
        response=json_util.dumps(result),
        mimetype='application/json'
    )
    return response


@app.route('/api/1/elements/mep', methods=['GET'])
def get_MEPCategory():
    result = collection_models.find({ '$or': [{'Category':'Ducts'},{'Category':'Pipes'} ,{'Category':'Pipe Fittings'},{'Category':'Duct Fittings'}]})
    response = app.response_class(
        response=json_util.dumps(result),
        mimetype='application/json'
    )
    return response

if __name__ == "__main__":
    app.run()