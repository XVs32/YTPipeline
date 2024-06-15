from dataclasses import fields
from flask import Flask, request
from googleDrive.googleDriveCore import googleDriveCore 
from waitress import serve

from user.user import userCore

app=Flask(__name__)

app=Flask(__name__)

service=googleDriveCore()
service.build()

@app.route('/request', methods=['POST'])
def main():
    
    #print request body
    user = request.form.get('user')
    print(user)
    email = request.form.get('email')
    print(email)
    url = request.form.get('url')
    print(url)
    
    user = userCore(email)
    email = user.getAuthorizedEmail(email)
    
    rootFolderId = service.findRootFolderByEmail(email)
    print(rootFolderId)
    
    parentFolderId = service.createFolder(rootFolderId, "testFolder")
    
    return service.uploadFile(parentFolderId, "download/AllMyself.wav", "AllMyself.wav")

@app.route('/userList', methods=['GET'])
def createFolder():
    pass


@app.get('/files-with-id/<file_id>/')
def get_files_with_id(file_id):
    pass

@app.get('/files-in-folder/<folder_id>/')
def get_files_in_folder(folder_id):
    pass

@app.get('/files-with-type')
def get_files_with_type():
    pass


@app.get('/files-with-limit-offset')
def get_files_with_limit_offset():
    pass


@app.get('/files-with-limit-offset-order')
def get_files_with_limit_offset_order():
    pass

if __name__=="__main__":  
    # app.run(debug=True, host="0.0.0.0", port=8080)
    serve(app, host="0.0.0.0", port=8080)