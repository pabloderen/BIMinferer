
from forge import Authenticate, getHub, getProjects, getRevitFiles


if __name__ == '__main__':
    access_token = Authenticate()
    if access_token:
        hubId = getHub(access_token, 'ADN')
        if hubId:
            projects = getProjects(hubId)
            for project in projects:
                getRevitFiles(project, access_token)
                