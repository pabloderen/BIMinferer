
from forge import Authenticate, getHub, getProjects, getRevitFiles,get_topfolders


if __name__ == '__main__':
    access_token = Authenticate()
    if access_token:
        hubId = getHub(access_token, 'ADN')
        if hubId:
            projects = getProjects(hubId)
            for project in projects:
                projectfolder=get_topfolders(hubId,project,access_token)
                getRevitFiles(projectfolder, project, access_token)
                