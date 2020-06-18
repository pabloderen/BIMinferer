import requests
import json
from glob import iglob
import shutil
import os

credentials_file = r"src\Credentials.txt"
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
	Hubs = json.loads(response.text.encode('utf8'))['data']
	for hub in Hubs:
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
	Projects = json.loads(response.text.encode('utf8'))['data']
	for project in Projects:
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

def visitFoldersForRvtsURN(folderId , projectId, access_token, result):
	content = getFolderContent(folderId, projectId, access_token)
	for c  in content:
		if c['type'] == 'folders':
			visitFoldersForRvtsURN(c['id'], projectId, access_token, result)
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
	Folders = json.loads(response.text.encode('utf8'))['data']
	for folder in Folders:
		if folder['attributes']['displayName']=="Project Files":
			return folder["id"]

def getItemDerivativeURN(project_id, item_id, access_token):
	"""Returns the item derivative urn

	project_id : id of the project
	
	item_id : id of the item
		
	access_token : access token from credentials
	"""
	url = base_url + '/data/v1/projects/%s/items/%s' % (project_id, item_id['id'])
	payload = {}
	headers = {
		'Authorization': 'Bearer %s' % access_token
	}
	response = requests.get( url, headers=headers, data = payload)
	content = json.loads(response.text.encode('utf8'))
	return content['included'][0]['relationships']['derivatives']['data']['id']

def getObjectDerivativeUrn(urn, access_token, type = None):
	"""Returns the derivative url of one object in the item
	
	urn : urn of the model
	
	access_token : access token from credentials
	
	type : type of element to search in model
	"""

	url = base_url + '/modelderivative/v2/designdata/%s/manifest' % urn
	payload = {}
	headers = {
		'Authorization': 'Bearer %s' % access_token
	}
	response = requests.get( url, headers=headers, data = payload)
	derivatives = json.loads(response.text.encode('utf8'))['derivatives']

	contentType = 'application/autodesk-db'

	#If we are looking for a svf element
	if type == 'svf':
		contentType = 'geometry'
		for children in derivatives[0]['children']:
			if children['type'] == contentType :
				for c  in children['children']:
					if c['mime'] == 'application/autodesk-svf':
						return c['urn']

	if type == 'db':
		contentType = 'application/autodesk-db'
	if type == 'json':
		contentType = 'application/json'


	for children in derivatives['derivatives'][0]['children']:
		if children['mime'] == contentType :
			return children['urn']
	return None

def createChunks(contentByteSize, ByteSizeLimit  = 20000000):
	"""
	Create range chunks for the header based on the content length and a base size limit
	(default 20mb)

	contentByteSize : size of content in bytes

	ByteSizeLimit : size of chunks in bytes (default = 20000000)
	"""
	
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

def downloadDerivativeObject(urn, derivativeUrn, access_token, fileName):
	"""Download the object from its derivative urn

	urn : urn of the model
	
	derivativeUrn: urn of the object to download

	access_token : access token from credentials

	fileName : name of the file once it's downloaded
	
	"""
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
			response = session.get( url, headers=headers)

			if response.status_code != 200:
				with open('db\\%s.part' % i, 'wb') as f:
					f.write(response.content)


	#Join parts
	dbFolder = 'db\\'
	dbDestinationPath = r'db\\%s.sdb' % fileName.replace("urn:adsk.wipprod:dm.lineage:","")
	destination = open(dbDestinationPath, 'wb')
	for filename in iglob(os.path.join(dbFolder, '*.part')):
		shutil.copyfileobj(open(filename, 'rb'), destination)
		os.remove(filename)
	destination.close()

	if destination.closed():
		return True
	return False



def getRVTObject( projectId, RVTurn):
	global access_token
	access_token = Authenticate()
	urn  = getItemDerivativeURN(projectId, RVTurn, access_token)
	dbUrn = getObjectDerivativeUrn(urn, access_token, 'json')
	isDownloaded = downloadDerivativeObject(urn, dbUrn, access_token, RVTurn['id']+".json" )
	if isDownloaded:
		print("Model %s object Downloaded" % RVTurn)


def getDBFilesFromHub():
	"""Download all Revit models DB files from the hub

	"""
	global access_token

	access_token = Authenticate()
	if not access_token:
		print("Error retriving token")
		return
	print("Credentials OK")

	hubId = getHub(access_token, 'ADN')
	if not hubId:
		print("Error retriving hub")
		return
	print("Hub OK")

	projects = getProjects(hubId)
	if not projects:
		print("Error retriving projects")
		return


	print("Projects OK")
	for project in projects:
		projectfolder=get_topfolders(hubId,project,access_token)
		projectRVTs = []
		visitFoldersForRvtsURN(projectfolder, project, access_token, projectRVTs)
		[getRVTObject( project, RVTUrn) for RVTUrn in projectRVTs]
