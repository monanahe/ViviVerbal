# -*- coding: utf-8 -*-
"""
Created on Fri Jun  2 17:29:45 2017

@author: Monana serena9636@163.com
"""

import urllib
import os,sys,stat
def apicatch(word,cuntry="2"):
    headers = {"User-Agent":"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)"}
     
    url = "http://dict.youdao.com/dictvoice"
     
#    word = "hello"#你要查的单词
#    cuntry = "2" #美式为2，英式为1
    params = {"audio":word, "type":cuntry}
    data = urllib.parse.urlencode(params).encode(encoding='UTF8')
     
    #response = urllib.request.urlopen(url, data, headers)
    request = urllib.request.Request(url, data, headers)  
    try:
        response = urllib.request.urlopen(request)  
    except NameError:
        pass
    try:
        fs = open("audio/"+word+".mp3", 'wb')
        
        fs.write(response.read())#response.read()即是返回的音频流，你可以直接发给前台不用保存
        fs.close()
    except PermissionError:
        pass
#    return response.read()