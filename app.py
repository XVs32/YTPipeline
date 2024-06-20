from dataclasses import fields
from flask import Flask, request
from googleDrive.googleDriveCore import googleDriveCore 
from waitress import serve
import threading

from user.user import userCore
from autoTag.autoTag import autoTagCore
from ytDlp.ytDlp import ytDlpCore

app=Flask(__name__)


@app.route('/request', methods=['POST'])
def main():
    
    #print request body
    email = request.form.get('email')
    print(email)
    url = request.form.get('url')
    print(url)
   
    t_yt_download = threading.Thread(target=download, args=(email, url))
    t_yt_download.start()
    
    return "<script>window.close();</script>" 

def download(email, url):
  
    downloader = ytDlpCore()
    service=googleDriveCore()
    service.build()
    tagAi = autoTagCore()

    user = userCore(email)
    email = user.getAuthorizedEmail(email)

    rootFolderId = service.findRootFolderByEmail(email)
    print(rootFolderId)
 
    filePath = downloader.download(url, "aac")
    fileName = filePath.split("/")[-1]
    
    tagAi.load_audio(fileName)
    tag = tagAi.tag()
    
    parentFolderId = service.createFolder(rootFolderId, tag)
    
    
    service.uploadFile(parentFolderId, filePath, fileName)
    
    return

if __name__=="__main__":  
    # app.run(debug=True, host="0.0.0.0", port=8080)
    serve(app, host="0.0.0.0", port=8080)