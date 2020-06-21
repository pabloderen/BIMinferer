from flask import Flask, jsonify ,request
from flasgger import Swagger
from bson import json_util, ObjectId
import json
from pymongo import MongoClient

app = Flask(__name__)
swagger = Swagger(app)


client = MongoClient('localhost', 27017)
db = client['bimferer']
collection_models = db['models']

@app.route('/')
def hello_world():
    body = '''
    Hello! Go check the API
    '''
    return body


@app.route('/api/1/elements/<string:category>', methods=['GET'])

def get_Category(category):
    """Get all parameters of elements from category.
    ---
    tags:
      - All Categories
    parameters:
      - name: category
        in: path
        type: string
        enum: [Air Terminals,
                Assemblies,
                Cable Tray Fittings,
                Cable Tray Runs,
                Cable Trays,
                Casework,
                Ceilings,
                Columns,
                Communication Devices,
                Conduit Fittings,
                Conduits,
                Curtain Panels,
                Data Devices,
                Detail Components,
                Detail Items,
                Doors,
                Duct Accessories,
                Duct Fittings,
                Duct Insulations,
                Duct Linings,
                Duct Placeholders,
                Ducts,
                Electrical Circuits,
                Electrical Equipment,
                Electrical Fixtures,
                Entourage,
                Fabrication Parts,
                Fascias,
                Fire Alarm Devices,
                Flex Ducts,
                Flex Pipes,
                Floors,
                Furniture,
                Furniture Systems,
                Generic Models,
                Grids,
                Gutters,
                Imports in Families,
                Levels,
                Lighting Devices,
                Lighting Fixtures,
                Line Loads,
                Mass Floors,
                Mass,
                Materials,
                Mechanical Equipment,
                Model Groups,
                Pads,
                Parking,
                Parts,
                Pipe Accessories,
                Pipe Fittings,
                Pipe Insulations,
                Pipe Placeholders,
                Pipes,
                Planting,
                Plumbing Fixtures,
                Property Lines,
                Railings,
                Ramps,
                Roads,
                Roofs,
                Roof Soffits,
                Security Devices,
                Shaft Openings,
                Site,
                Slab Edges,
                Specialty Equipment,
                Sprinklers,
                Stairs,
                Structural Area Reinforcement,
                Structural Beam Systems,
                Structural Columns,
                Structural Connection Handler,
                Structural Connections,
                Structural Fabric Areas,
                Structural Fabric Reinforcement,
                Structural Foundations,
                Structural Framing,
                Structural Path Reinforcement,
                Structural Rebar,
                Structural Stiffeners,
                Structural Trusses,
                Supports,
                Switch Systems,
                Telephone Devices,
                Topography,
                Walls,
                Windows]
        required: true
        default: Walls
      - name: limit
        in: query
        type: integer
        description: The numbers of items to return.
        default: 100
    
    responses:
      200:
        description: A list of elements from a specific category with parameters

    """
    limit = request.args.get('limit')
    if not limit:

        limit = 100
    else:
         limit = int(limit)
    result = collection_models.find({'Category': category})
    response = app.response_class(
        response=json_util.dumps(result),
        mimetype='application/json'
    )
    return response

@app.route('/api/1/elements/bycategories', methods=['POST'])
def get_Categories():
    """
    Get all elements from a Specific category
    ---
    tags:
      - All Categories
    parameters:
      - name: limit
        in: query
        type: integer
        description: The numbers of items to return.
        default: 100
      - name: body
        in: body
        required: true
        schema:
          id: Categories
          type: object
          example: { "categories": ["Ducts", "Pipes"]}
          properties:
            Categories_list:
              type: array
              items:
                schema:
                  id: Category
                  type: string
                  
              
        
    responses:
      200:
        description: Elements from said categories
    examples:
        categories: ["Ducts", "Pipes"]

    """
    limit = request.args.get('limit')
    if not limit:

        limit = 100
    else:
         limit = int(limit)

    content = request.json
    if not content:
        return "Error in the json file"
    find = {}
    find['$or'] = []
    for category in content['categories']:
            find['$or'].append( {'Category':category})

    result = collection_models.find(find).limit(limit)
    response = app.response_class(
        response=json_util.dumps(result),
        mimetype='application/json'
    )
    return response

@app.route('/api/1/elements/mep/', methods=['GET'])
def get_MEPCategory():
    """Get Ducts and Pipes System Classification, Size, Length, Material and Category.
    ---
    tags:
      - MEP
    parameters:
      - name: limit
        in: query
        type: integer
        description: The numbers of items to return.
        default: 100
    
    responses:
      200:
        description: A list of pipes and ducts with parameters

    """
    limit = request.args.get('limit')
    if not limit:

        limit = 100
    else:
         limit = int(limit)
    result = collection_models.find({ '$or': [{'Category':'Ducts'},{'Category':'Pipes'} ]},  
    { "properties_Mechanical_System Classification": 1,
     "properties_Dimensions_Size": 1 ,
     "properties_Dimensions_Length": 1,
     "properties_Mechanical_Material" : 1, 
      "Category": 1 ,
       "modelId":1,
        "projectId":1 }).limit( limit )
    response = app.response_class(
        response=json_util.dumps(result),
        mimetype='application/json'
    )
    return response

@app.route('/api/1/elements/pipes/', methods=['GET'])
def get_PIPECategory():
    """Get pipes System Classification, Size, Length, Material and Category.
    ---
    tags:
      - MEP
    parameters:
      - name: limit
        in: query
        type: integer
        description: The numbers of items to return.
        default: 100
    
    responses:
      200:
        description: A list of pipes with parameters

    """

    limit = request.args.get('limit')
    if not limit:

        limit = 100
    else:
         limit = int(limit)
    result = collection_models.find({ '$or': [{'Category':'Pipes'} ]},  
    { "properties_Mechanical_System Classification": 1,
    "properties_Dimensions_Size": 1 ,
    "properties_Dimensions_Length": 1,
    "properties_Mechanical_Material" : 1, 
    "Category": 1 ,
    "modelId":1,
        "projectId":1 }).limit( limit )
    response = app.response_class(
        response=json_util.dumps(result),
        mimetype='application/json'
    )
    return response


if __name__ == "__main__":
    app.run()