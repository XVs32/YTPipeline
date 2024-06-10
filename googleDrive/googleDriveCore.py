import os
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials


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
            
        return folderList
    
    def createFolder(self, parentFolderId, folderName):

        #retry if failed to create folder
        retry = 0
        while retry < 5:
            try:
                folder = self.service.files().create(body={
                    'name': folderName,
                    'mimeType': 'application/vnd.google-apps.folder',
                    'parents': [parentFolderId]
                }).execute()
                break
            except:
                self.build()
                retry += 1

        return folder
