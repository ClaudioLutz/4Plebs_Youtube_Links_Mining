# %%
from __future__ import unicode_literals
import numpy as np
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import time
import pickle
import os
from os import listdir
from os.path import isfile, join
from yt_dlp import YoutubeDL

pickles_folder = './pickles_thread'
if os.path.exists(pickles_folder) == False:
    os.mkdir(pickles_folder)

YT_pickles_folder = './YT_pickles'
if os.path.exists(YT_pickles_folder) == False:
    os.mkdir(YT_pickles_folder)

youtube_links_folder = './youtube_links'
if os.path.exists(youtube_links_folder) == False:
    os.mkdir(youtube_links_folder)

starts_with = 'https://archive.4plebs.org/pol/thread/'
youtube = 'https://www.youtube.com'
thread_set = set()

for page in range(1,56):
    if os.path.exists(pickles_folder + '/' +str(page)+'.pkl') == False:
        links = []
        time.sleep(1)   
        site= "https://archive.4plebs.org/pol/search/subject/pol%20music/page/"+str(page)+"/"
        hdr = {'User-Agent': 'Mozilla/5.0'}
        req = Request(site,headers=hdr)
        wpage = urlopen(req)
        soup = BeautifulSoup(wpage,"lxml")
        for link in soup.findAll('a'):
            links.append(link.get('href'))
        result = list(filter(lambda x: x.startswith(starts_with)if x else '', links))
        link_set = set(result)
        thread_set.update(link_set)   

        thread_file_name = pickles_folder + '/' +str(page)+'.pkl'

        with open(thread_file_name, 'wb') as handle:
            pickle.dump(link_set, handle, protocol=pickle.HIGHEST_PROTOCOL)

    if os.path.exists(YT_pickles_folder + '/' +str(page)+'.pkl') == False:        
        thread_file_name = pickles_folder + '/' +str(page)+'.pkl'
        with open(thread_file_name, 'rb') as handle:
            thread_set = pickle.load(handle)
            if os.path.exists(YT_pickles_folder + '/' +str(page)+'.pkl') == False:
                yt_set = set()

                for thread in thread_set:                
                    #time.sleep(3)
                    YT_links = []
                    site= thread
                    hdr = {'User-Agent': 'Mozilla/5.0'}
                    req = Request(site,headers=hdr)
                    wpage = urlopen(req)
                    soup = BeautifulSoup(wpage,"lxml")
                    for link in soup.findAll('a'):
                        YT_links.append(link.get('href'))
                    result = list(filter(lambda x: x.startswith(youtube)if x else '', YT_links))
                    yt_set.update(result)

                yt_file_name = YT_pickles_folder + '/' +str(page)+'.pkl'

                with open(yt_file_name, 'wb') as handle:
                    pickle.dump(yt_set, handle, protocol=pickle.HIGHEST_PROTOCOL)                
                
                with open(yt_file_name, 'rb') as handle:
                    youtube_set = pickle.load(handle)
 
YT_pickles_folder = './YT_pickles'
complete_yt_set = set()
for filename in os.listdir(YT_pickles_folder):
    with open(YT_pickles_folder+'/'+filename, 'rb') as handle:
        complete_yt_set.update(pickle.load(handle))

complete_yt_set = {x for x in complete_yt_set if "playlist" not in x }
complete_yt_set = {x for x in complete_yt_set if "playlist" not in x }
complete_yt_set = {x for x in complete_yt_set if "channel" not in x} 
complete_yt_set = {x for x in complete_yt_set if "index" not in x }
complete_yt_set = {x for x in complete_yt_set if "start" not in x }
complete_yt_set = {x for x in complete_yt_set if "search" not in x }
complete_yt_set = {x for x in complete_yt_set if "list" not in x }
complete_yt_set = {x for x in complete_yt_set if "feature" not in x }

def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')

download_songs_folder ='./download_songs/'

ydl_opts = {
    'format':'bestaudio/best',
    'extractaudio':True,
    'audioformat':'mp3',
    'outtmpl': download_songs_folder + '%(title)s-%(id)s.%(ext)s',         #name the file the ID of the video
    'noplaylist':True,
    'nocheckcertificate':True,
    'proxy':"",
    'progress_hooks': [my_hook],  
    'addmetadata':True,
    'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        },
        {
            'key': 'FFmpegMetadata'
        }]
}

for yt_link in complete_yt_set:
    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([yt_link])
    except:
        pass

# %%

#split set in 16 even sized .csv

complete_yt_list = list(complete_yt_set)

complete_yt_list_split = np.array_split(complete_yt_list, 16)

for array in complete_yt_list_split:
    print(list(array))

filenr = 1

for array in complete_yt_list_split:

    np.savetxt(youtube_links_folder +"\youtube_links_"+str(filenr)+".csv", 
           array,
           delimiter =", ", 
           fmt ='% s')
    filenr +=1

