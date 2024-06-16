import yt_dlp
from slugify import slugify
import ffmpeg
import os

class ytDlpCore():
    
    def getVideoId(self, url):
        idStart = url.find("?v=")
        
        id = 'default_id'
           
        if idStart != -1:
            yt_id = url[idStart:idStart+14]
            yt_id = yt_id[3:]
           
        return id

    def getVideInfo(self, yt_id):
        
        ydl_opts = {
            'format': 'bestaudio/best',
        }
    
        info = yt_dlp.YoutubeDL(ydl_opts).extract_info(yt_id, download=False)
        
        
        info['title'] = slugify(info['title'], allow_unicode=True)
        
        return info['title'], info['ext']

    def download(self, url, format):
        #download video in best quality
        #output to "download" folder
        
        id = self.getVideoId(url)
        title, ext = self.getVideInfo(id)
        
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'download/' + title + '.' + ext,
        }
        
        yt_dlp.YoutubeDL(ydl_opts).download([id])
       
        #convert downloaded file to "format" type 
        self.formatConvert('download/' + title, ext, format)
        
        return 'download/' + title + '.' + format
        
    def formatConvert(self, filePath, extIn, extOut):
        #convert file from extIn type to extOut type using ffmpeg
        ffmpeg.input(filePath + "." + extIn).output(filePath + "." + extOut).run()
        
        # Remove original file
        os.remove(filePath + "." + extIn)
        
        return
            