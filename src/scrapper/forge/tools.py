import os
from glob import iglob
import json 
import pandas as pd

def createChunks(contentByteSize, ByteSizeLimit  = 20000000):
    '''
    Create range chunks for the header based on the content length and a base size limit
    (default 20mb)

    contentByteSize : size of content in bytes

    ByteSizeLimit : size of chunks in bytes (default = 20000000)
    '''

    if contentByteSize < ByteSizeLimit:
        return ['bytes=0-%s' % contentByteSize]
    
    minChunkRange = 0
    resultChunks = []
    for s in range(ByteSizeLimit,contentByteSize, ByteSizeLimit):
        if s> contentByteSize:
            s = contentByteSize
        _range = 'bytes=%s-%s' % (minChunkRange,s)
        resultChunks.append(_range)
        minChunkRange = s+1

    _range = 'bytes=%s-%s' % (minChunkRange,contentByteSize)
    resultChunks.append(_range)
    return resultChunks




categoryList = ["Air Terminals",
"Analytical Beams",
"Analytical Braces",
"Analytical Columns",
"Analytical Floors",
"Analytical Foundation Slabs",
"Analytical Isolated Foundations",
"Analytical Nodes",
"Analytical Wall Foundations",
"Analytical Walls",
"Area Loads",
"Area Schemes",
"Areas",
"Assemblies",
"Cable Tray Fittings",
"Cable Tray Runs",
"Cable Trays",
"Casework",
"Ceilings",
"Columns",
"Communication Devices",
"Conduit Fittings",
"Conduit Runs",
"Conduits",
"Curtain Grids",
"Curtain Panels",
"Curtain Panels",
"Curtain Systems",
"Curtain Wall Mullions",
"Data Devices",
"Detail Components",
"Detail Items",
"Detail Items",
"Detail Items",
"Doors",
"Duct Accessories",
"Duct Fittings",
"Duct Insulations",
"Duct Linings",
"Duct Placeholders",
"Duct Systems",
"Ducts",
"Electrical Circuits",
"Electrical Equipment",
"Electrical Fixtures",
"Entourage",
"Entourage",
"Existing",
"Fabrication Parts",
"Fascias",
"Fire Alarm Devices",
"Flex Ducts",
"Flex Pipes",
"Floors",
"Furniture",
"Furniture Systems",
"Generic Annotations",
"Generic Models",
"Generic Models",
"Grids",
"Gutters",
"HVAC Zones",
"Imports",
"Imports in Families",
"Internal Area Loads",
"Internal Line Loads",
"Internal Point Loads",
"Levels",
"Levels",
"Lighting Devices",
"Lighting Fixtures",
"Lines",
"Lines",
"Line Loads",
"Mass Floors",
"Mass",
"Mass",
"Materials",
"Mechanical Equipment",
"Model Groups",
"Model Text",
"Nurse Call Devices",
"Pads",
"Parking",
"Parts",
"Pipe Accessories",
"Pipe Fittings",
"Pipe Insulations",
"Pipe Placeholders",
"Pipes",
"Piping Systems",
"Planting",
"Planting",
"Plumbing Fixtures",
"Point Clouds",
"Point Loads",
"Project Information",
"Profiles",
"Property Line Segments",
"Property Lines",
"Railings",
"Railings",
"Railings",
"Railings",
"Ramps",
"Raster Images",
"Repeating Details",
"Revision Clouds",
"Revisions",
"Roads",
"Roofs",
"Roof Soffits",
"Rooms",
"RVT Links",
"Security Devices",
"Shaft Openings",
"Sheets",
"Site",
"Slab Edges",
"Spaces",
"Specialty Equipment",
"Sprinklers",
"Stairs (created by Sketch)",
"Stairs (Component)",
"Stairs",
"Stairs",
"Stairs",
"Structural Area Reinforcement",
"Structural Beam Systems",
"Structural Columns",
"Structural Connection Handler",
"Structural Connections",
"Structural Fabric Areas",
"Structural Fabric Reinforcement",
"Structural Foundations",
"Structural Framing",
"Structural Path Reinforcement",
"Structural Rebar",
"Structural Stiffeners",
"Structural Trusses",
"Supports",
"Switch Systems",
"Telephone Devices",
"Topography",
"Wall Sweeps",
"Walls",
"Walls",
"Walls",
"Windows",
"Wires",]

def applyCategory(collection, projectId, modelId):
    resultCollection = []
    category = "Model"
    for element in collection:
        if 'properties' not in element and element['name'] in categoryList:
            category = element['name']
        else:
            if category not in "Model":
                element['projectId'] = projectId
                element["Category"] = category
                element['modelId'] = modelId
                resultCollection.append(element)
    
    return resultCollection