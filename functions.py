import os
import requests
import re
from bs4 import BeautifulSoup

from pytube import YouTube
#from moviepy.editor import *



def get_linklist_by_title(searh_request):
    urls, plst, urls_emb = [], set(), []
    #convert to querry view and get response
    resp = requests.get('https://www.youtube.com/results?search_query=' + searh_request.replace(' ', '+'))

    lst_match_obj = re.findall(r'"videoId":".{11}"',resp.text)    # searching video id`s from <script> tag
    for obj in lst_match_obj:
        link = "https://www.youtube.com/watch?v="+obj[11:22]      #create working link from id
        if link not in plst:
            urls.append(link)
        plst.add("https://www.youtube.com/watch?v="+obj[11:22])   # set is need for checking links repeating
    del plst
    return urls


def search_video_data(link):
    video = {'ready':False}
    # convert link to embedded type
    video["link_internal"] = link
    video["link"] = "https://www.youtube.com/embed/"+link[link.find("v=")+2:]
    yt = YouTube(video["link_internal"])
    video["title"] = yt.title

    video["description"] = "Duration: {}".format(get_str_time_from_seconds(yt.length))

    return video

    
def get_stream(video):
    # get_highest_resolution
   # yt = YouTube(video["link_internal"])
    yt = YouTube("SUCK")
    streams = yt.streams.filter(only_audio=True).order_by('abr')
    if not streams:
        video['description'] = video['description'] + ' | unavailable to download'
    return streams[-1], streams[-1].title+'.mp3' 
    
   # video = VideoFileClip("temp.mp4")
   # video.audio.write_audiofile(video['title']+".mp3")


def get_str_time_from_seconds(seconds):
    if seconds // 3600 > 0:
        hours = str(seconds // 3600) + ':'
    else:
        hours = ''
    if (seconds // 60) % 60 < 10:
        mins = '0' + str((seconds // 60)% 60 )
    else:
        mins = str((seconds // 60)% 60 )
    if seconds % 60 < 10:
        sec = '0' + str(seconds % 60)
    else:
        sec = str(seconds % 60)
    return hours + mins + ':' + sec

