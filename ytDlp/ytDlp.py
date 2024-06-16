import yt_dlp
from slugify import slugify
import ffmpeg

class ytDlpCore():
    
    def getVideoId(self, url):
        idStart = url.find("?v=")
        
        id = 'default_id'
        
        if idStart != -1:
            id = url[idStart:idStart+14]
            id = id[3:]
        
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
        title, ext = self.getVideInfo(url)
        
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'download/' + title + '.' + ext,
        }
        
        yt_dlp.YoutubeDL(ydl_opts).download([id])
       
        #convert downloaded file to "format" type 
        self.formatConvert('download/' + title, '.' + ext, '.' + format)
        
        return 'download/' + title + '.' + format
        
    def formatConvert(self, file_path, extIn, extOut):
        #convert file from extIn type to extOut type using ffmpeg
        ffmpeg.input(file_path + "." + extIn).output(file_path + "." + extOut).run()
        return
            