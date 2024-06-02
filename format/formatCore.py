# -*- coding: utf-8 -*-

import yt_dlp

from slugify import slugify
import subprocess
import threading
import os
import re

def get_yt_video_id(url):
    yt_id_index = url.find("?v=")
    
    yt_id = 'default_id'
    
    if yt_id_index != -1:
        yt_id = url[yt_id_index:yt_id_index+14]
        yt_id = yt_id[3:]
    
    return yt_id

def get_yt_video_info(yt_id):
    
    ydl_opts = {
        'format': 'bestaudio/best',
    }
    
    info = yt_dlp.YoutubeDL(ydl_opts).extract_info(yt_id, download=False)
    
    info['title'] = slugify(info['title'], allow_unicode=True)
    
    return info['title'], info['ext']
