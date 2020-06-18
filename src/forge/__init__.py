import requests
import json
from glob import iglob
import shutil
import os

credentials_file = "src\Credentials.txt"
base_url = 'https://developer.api.autodesk.com/'
access_token = None
current_hub_name = "ADN" 
current_hub_id = ""
projects = {}

def parse_credentials(filename):
    "Parse credentials from given text file."
    f = open( filename )
    lines = f.readlines()
    f.close()
    credentials = []
    for line in lines:
        i = line.find('#')
        if -1 < i: line = line[0:i]
        i = line.find(':')
        if -1 < i: line = line[i+1:]
        line = line.strip()
        if 0 < len(line):
            print(line)
            line = line.strip("\"'")
            credentials.append(line)

    if 2 != len(credentials):
        credentials = None
        raise "Invalid credentials: expected two entries, consumer key and secret;\nread %s lines, %s after stripping comments." % (len(lines),len(credentials))
        

    return credentials


def Authenticate():
	'''Authenticate to Forge'''

	global access_token
	global credentials_file
	global base_url
	global current_hub_name

	credentials = parse_credentials(credentials_file)

	consumer_key = credentials[0]
	consumer_secret = credentials[1]
	url = base_url + 'authentication/v1/authenticate'

	data = {
	'client_id' : consumer_key,
	'client_secret' : consumer_secret,
	'grant_type' : 'client_credentials',
	'scope':    'data:read data:write bucket:create bucket:read'

	}

	headers = {
	'Content-Type' : 'application/x-www-form-urlencoded'
	}

	r = requests.post(url, data=data, headers=headers)
	content = eval(r.content)

	if r.status_code != 200:
			print("Authentication returned status code %s." % r.status_code)
			return None

	access_token = content['access_token']
	return access_token

def getHub(access_token, current_hub_name):
    '''Return true if hub was found by name and saves if to global parameter'''
    global base_url
    global current_hub_id

    url = base_url + 'project/v1/hubs'

    payload = {}
    headers = {
        'Authorization': 'Bearer %s' % access_token
    }

    response = requests.get( url, headers=headers, data = payload)
    content = json.loads(response.text.encode('utf8'))
    for hub in content['data']:
        if hub['attributes']['name'] == current_hub_name:
            current_hub_id = hub['id']
            return  hub['id']
    return None

def getProjects(hubId):
    '''Return all projects in hub'''
    global access_token
    global current_hub_id
    global projects

    current_hub_id = hubId
    url = base_url + 'project/v1/hubs/%s/projects' % current_hub_id

    payload = {}
    headers = {
        'Authorization': 'Bearer %s' % access_token
    }

    response = requests.get( url, headers=headers, data = payload)
    content = json.loads(response.text.encode('utf8'))
    for project in content['data']:
        projects[project['id']] = project['attributes']['name']

    return projects

def getFolderContent(folderId, projectId, access_token):
    url = base_url + 'data/v1/projects/%s/folders/%s/contents' % (projectId, folderId)
    payload = {}
    headers = {
        'Authorization': 'Bearer %s' % access_token
    }

    response = requests.get( url, headers=headers, data = payload)
    content = json.loads(response.text.encode('utf8'))
    return content['data']

def travelFoldersForRvts(folderId , projectId, access_token, result):
    content = getFolderContent(folderId, projectId, access_token)
    for c  in content:
        if c['type'] == 'folders':
            travelFoldersForRvts(c['id'], projectId, access_token, result)
        elif (c['type'] == 'items' 
        and ".rvt"  in c['attributes']['displayName']
        ): # and '.rvt' in c['attributes']['displayName']
            result.append(c)

def get_topfolders(hub_id,project_id,access_token):
    url= base_url + "/project/v1/hubs/%s/projects/%s/topFolders" % (hub_id, project_id)
    payload = {}
    headers = {
        'Authorization': 'Bearer %s' % access_token
    }

    response = requests.get( url, headers=headers, data = payload)
    content = json.loads(response.text.encode('utf8'))
    for folder in content['data']:
        if folder['attributes']['displayName']=="Project Files":
            return folder["id"]

def getForgeItem(project_id, item_id, access_token):
    url = base_url + '/data/v1/projects/%s/items/%s' % (project_id, item_id['id'])
    payload = {}
    headers = {
        'Authorization': 'Bearer %s' % access_token
    }
    response = requests.get( url, headers=headers, data = payload)
    content = json.loads(response.text.encode('utf8'))
    return content['included'][0]['relationships']['derivatives']['data']['id']

def getDBDerivativeUrn(urn, access_token):
    url = base_url + '/modelderivative/v2/designdata/%s/manifest' % urn
    payload = {}
    headers = {
        'Authorization': 'Bearer %s' % access_token
    }
    response = requests.get( url, headers=headers, data = payload)
    content = json.loads(response.text.encode('utf8'))
    for c in content['derivatives'][0]['children']:
        if c['mime'] == 'application/autodesk-db':
            return c['urn']
    return None

def createChunks(contentByteSize):

    ByteSizeLimit  = 20000000
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

def downloadDerivative(urn,derivativeUrn, access_token, projectId):
    
    url = base_url+  '/modelderivative/v2/designdata/%s/manifest/%s' % (urn, derivativeUrn)
    headers = {
        'Authorization': 'Bearer %s' % access_token
    }
    response = requests.head( url, headers=headers)

    if response.status_code != 200:
        print("Error retrieving derivative heads")
        return None
    content = int(response.headers._store['content-length'][1])
    chunks = createChunks(content)

    with requests.Session() as session:
        for i, chunk in enumerate(chunks):
            url = base_url+  '/modelderivative/v2/designdata/%s/manifest/%s' % (urn, derivativeUrn)
            headers = {
                'Authorization': 'Bearer %s' % access_token,
                'Range': chunk
            }
            response = requests.get( url, headers=headers)

            if response.status_code != 200:
                with open('db\\%s.part' % i, 'wb') as f:
                    f.write(response.content)


    #Join parts
    dbFolder = 'db\\'
    dbDestinationPath = r'db\\%s.sdb' % projectId.replace("urn:adsk.wipprod:dm.lineage:","")
    destination = open(dbDestinationPath, 'wb')
    for filename in iglob(os.path.join(dbFolder, '*.part')):
        shutil.copyfileobj(open(filename, 'rb'), destination)
        os.remove(filename)
    destination.close()



def getRevitFiles( projectfolder, projectId, access_token):
    projectRVTs = []
    access_token = Authenticate()
    travelFoldersForRvts(projectfolder, projectId, access_token, projectRVTs)
    for RVTurn in projectRVTs:
        urn  = getForgeItem(projectId, RVTurn, access_token)
        dbUrn = getDBDerivativeUrn(urn, access_token)
        downloadDerivative(urn, dbUrn, access_token, RVTurn['id'])