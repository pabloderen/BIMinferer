
from forge import Authenticate, getHub, getProjects, getFolderContent


if __name__ == '__main__':
    access_token = Authenticate()
    if access_token:
        hubId = getHub(access_token, 'ADN')
        if hubId:
            projects = getProjects(hubId)
            for project in projects:
                content = getFolderContent('urn:adsk.wipprod:fs.folder:co.9lgC_unGTT-cHObgGRatgA', project, access_token)
                