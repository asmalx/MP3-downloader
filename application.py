from flask import Flask, render_template, request, url_for, flash

import functions


app = Flask(__name__)
app.config['SECRET_KEY'] = 'GdOR27zTVl2Rm0VTHkeM'

videos_list, urls = [], []
ptr, lng  = 0, 'en'


@app.route('/') 
@app.route('/index')
def index():
    global videos_list
    return render_template("index.html", tracks=False)


@app.route('/submit', methods=["POST"])
def submit():
    # reset all old videos 
    global videos_list, urls, ptr
    videos_list, urls = [], []
    # at the start, process first 5 videos
    ptr = 0

    title = request.form["search_input"]
    # entered link
    if "http" in  title:
        video = functions.search_video_data(title)
        video['number'] = len(videos_list) + 1
        videos_list.append(video)
    # entered text
    else:
        urls = functions.get_linklist_by_title(title)
        for i in range(ptr, min(ptr+5, len(urls))):
            video = functions.search_video_data(urls[i])
            video['number'] = i+1
            videos_list.append(video)           
    return render_template("index.html", videos = videos_list)

@app.route('/videos', methods=["POST"])
def video():
    action, video_number = request.form["button"], int(request.form["data"])
    #print("Entered action:", action, "entered video id", video_number)

    # validate nubber
    if video_number < 0 or video_number > len(videos_list): # do nothing, for safety
        return render_template("index.html", videos = videos_list)

    if action == "Show":
        videos_list[video_number-1]["show_video"] = "Hide";
    elif action == "Hide":
        videos_list[video_number-1]["show_video"] = "Show";
    elif action == "Download":
        #print("downloading")
        functions.download_track(videos_list[video_number-1])
    return render_template("index.html", videos = videos_list)


@app.route('/more', methods=["GET"])
def more():
    return render_template("index.html", videos = videos_list)

