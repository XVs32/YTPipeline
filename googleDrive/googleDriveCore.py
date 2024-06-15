import os
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import googleapiclient
import googleapiclient


class googleDriveCore():
    
    service = None 
    
    def __init__(self):
        self._SCOPES=['https://www.googleapis.com/auth/drive']

        _base_path = os.path.dirname(__file__)
        _credential_path=os.path.join(_base_path, '../assets/credential.json')
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = _credential_path

    def build(self):
        creds = ServiceAccountCredentials.from_json_keyfile_name(os.getenv("GOOGLE_APPLICATION_CREDENTIALS"), self._SCOPES)
        self.service = build('drive', 'v3', credentials=creds)
        return
    
    def findRootFolderByEmail(self, email):

        query = f"mimeType='application/vnd.google-apps.folder' and name='YTPipeline' and '{email}' in owners"
        
        #retry if failed to get folderList
        retry = 0
        while retry < 5:
            try:
                folderList=self.service.files().list(\
                    q=query,
                    fields="files(id, name, owners)",\
                    ).execute()
                break
            except:
                self.build()
                retry += 1
            
        return folderList["files"][0]["id"]
    
    def findFolderByName(self, parentFolderId, folderName):

        query = f"mimeType='application/vnd.google-apps.folder' and name='{folderName}' and '{parentFolderId}' in parents"

        #retry if failed to get folderList
        retry = 0
        while retry < 5:
            try:
                folderList=self.service.files().list(\
                    q=query,
                    fields="files(id, name, owners)",\
                    ).execute()
                break
            except:
                self.build()
                retry += 1

        if len(folderList["files"]) == 0:
            return None
        else:
            return folderList["files"][0]["id"]
    
    def createFolder(self, parentFolderId, folderName):
        
        isExist = self.findFolderByName(parentFolderId, folderName)
        
        if isExist != None:
            print("folder already exist")
            return isExist
        
        #retry if failed to create folder
        retry = 0
        while retry < 5:
            try:
                folder = self.service.files().create(body={
                    'name': folderName,
                    'mimeType': 'application/vnd.google-apps.folder',
                    'parents': [parentFolderId]
                }).execute()
                print("create success")
                break
            except:
                self.build()
                retry += 1

        return folder["id"]
    
