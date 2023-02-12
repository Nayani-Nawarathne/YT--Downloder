import logging

from flask import *
from flask import Flask, render_template,request,redirect

import re
import time
import pytube.exceptions

from pytube import YouTube
from pytube import Playlist



app=Flask(__name__)

Link=[]
Name=[]


@app.route('/')
def home():
    return render_template("index.html")

@app.route('/features')
def features():
    return render_template("features.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route('/error')
def error():
    return render_template("error.html")

@app.route('/download',methods=["POST","GET"])
def download():
    url=request.form["url"]
    #print(url)
    res=request.form.get('res')
    #print(res)
    #print("Someone just tried to download ",url)

    try:
        grab_video=YouTube(url)

    except pytube.exceptions.RegexMatchError:
        print(f'Video {url} is invalid, skipping.')
        return render_template("error.html")
               
    
    else:
        if(res=="1"):
            try:
                video_res= grab_video.streams.filter(progressive=True).get_lowest_resolution()
                download_video = video_res.url
                video_name = video_res.title
                video_name = video_name.replace(" ", " ")
                download_link = download_video+'&title='+video_name
                #print(video_res.title, "Download OK")
                return redirect(download_link)

            except AttributeError:
                #print(f'Video {url} selected resolution is unavaialable, skipping.')
                return render_template("error.html")



        if(res=="2"):
            try:
                video_res= grab_video.streams.filter(progressive=True).get_by_resolution('720p')
                download_video = video_res.url
                video_name = video_res.title
                video_name = video_name.replace(" ", " ")
                download_link = download_video+'&title='+video_name
                #print(video_res.title, "Download OK")
                return redirect(download_link)

            except AttributeError:
                #print(f'Video {url} selected resolution is unavaialable, skipping.')
                return render_template("error.html")


        if(res=="3"):
            try:
                video_res= grab_video.streams.filter(progressive=True).get_highest_resolution()
                download_video = video_res.url
                video_name = video_res.title
                video_name = video_name.replace(" ", " ")
                download_link = download_video+'&title='+video_name
                #print(video_res.title, "Download OK")
                return redirect(download_link)

            except AttributeError:
                #print(f'Video {url} selected resolution is unavaialable, skipping.')
                return render_template("error.html")

        if(res=="4"):
            try:
                audio_res= grab_video.streams.filter(only_audio=True).first()
                download_audio = audio_res.url
                audio_name = audio_res.title
                audio_name = audio_name.replace(" ", " ")
                download_link = download_audio+'&title='+audio_name
                #print(audio_res.title, "Download OK")
                return redirect(download_link)

            except AttributeError:
                #print(f'Video {url} selected resolution is unavaialable, skipping.')
                return render_template("error.html")

    return redirect('/')


@app.route('/playlist',methods=["POST","GET"])
def playlist_download():
    url=request.form["url"]
    #print(url)
    res=request.form.get('res')
    #print(res)
    playlist = Playlist(url)
    playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")
    for url in playlist.video_urls:
            #print("Someone just tried to download ",url)
            try:
                grab_video=YouTube(url)
                #time.sleep(1)

            except pytube.exceptions.RegexMatchError:
                print(f'Video {url} is invalid, skipping.')
                return render_template("error.html")

            else:
                    if(res=="1"):
                        try:
                            video_res= grab_video.streams.filter(progressive=True).get_lowest_resolution()

                        except AttributeError:
                            #print(f'Video {url} selected resolution is unavaialable, skipping.')
                            continue
                        

                    if(res=="2"):
                        try:
                            video_res= grab_video.streams.filter(progressive=True).get_by_resolution('720p')

                        except AttributeError:
                            #print(f'Video {url} selected resolution is unavaialable, skipping.')
                            continue

                    if(res=="3"):
                        try:
                            video_res= grab_video.streams.filter(progressive=True).get_highest_resolution()

                        except AttributeError:
                            #print(f'Video {url} selected resolution is unavaialable, skipping.')
                            continue

                    if(res=="4"):
                        try:
                            video_res= grab_video.streams.filter(only_audio=True).first()

                        except AttributeError:
                            #print(f'Video {url} selected format is unavaialable, skipping.')
                            continue

            download_video = video_res.url
            video_name = video_res.title
            video_name = video_name.replace(" ", "_")
            download_link = download_video+'&title='+video_name
            #print(video_res.title, "Download OK")
            Name.append(video_name)
            Link.append(download_link)


    zip_Arr=zip(Name,Link)
    Playlist_data=dict(zip_Arr)
    #print(Playlist_data)


    return render_template('playlist.html',Playlist_data = Playlist_data)


if __name__ == '__main__':
    app.run(debug=True)