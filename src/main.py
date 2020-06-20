from forge import Authenticate, getHub, getProjects, get_topfolders, getJsonFiles, visitFoldersForRvtsURN, access_token

from database import savetoDataBase




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

    projects = getProjects(access_token, hubId)
    if not projects:
        print("Error retriving projects")
        return


    print("Projects OK")
    for project in projects:
        projectfolder=get_topfolders(hubId,project,access_token)
        projectRVTs = []
        visitFoldersForRvtsURN(projectfolder, project, access_token, projectRVTs)
        for  RVTUrn in projectRVTs:
            savetoDataBase(getJsonFiles( project, RVTUrn))


if __name__ == '__main__':
    getDBFilesFromHub()