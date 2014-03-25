PORTALS_SECTION_LABEL="portals"
BOOKMARKS_SECTION_LABEL="bkmrk"

def loadBookmarks(allBookmarks,folderName):
    '''
    Pulls the bookmarks contained in the folder with the given name.  If no name
	is provided, then the root "Other" folder is used.  If there are multiple
	folders with the given name, then the first one encountered will be used.
	This is unpredictable, therefore it is advised to not give multiple folders
	the same name.
    '''
    portals = allBookmarks[PORTALS_SECTION_LABEL]
    folderId = getFolderId(portals, folderName)
    print("FolderId = "+folderId)
    return portals[folderId][BOOKMARKS_SECTION_LABEL]

def getFolderId(portals, folderName):
    if folderName != None:    
        for folders in portals:
            if portals[folders]["label"] == folderName:
                return folders
    return 'idOther'