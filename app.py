from flask import Flask, render_template, request, url_for, send_file, flash
import functions

app = Flask(__name__)
app.config['SECRET_KEY'] = '2c7f07064e05560b9745cfef4fda2b7307aaf3f7'

# videos vost for current client
videos_list, urls = [], []
# current video title to download
current_title = ""

@app.route('/') 
@app.route('/index')
def index():
    global videos_list, urls, current_title
    # if main page - clear data
    videos_list = urls = []
    current_title = ""
    return render_template("index.html", tracks=False)


@app.route('/submit', methods=["POST"])
def submit():
    global videos_list, urls, current_title
    # reset all old videos 
    videos_list, urls = [], []
    # no chosen video 
    current_title = ""

    title = request.form["search_input"]
    # entered link
    if "http" in  title:
        video = functions.search_video_data(title)
        video['number'] = len(videos_list) + 1
        videos_list.append(video)
    # entered text
    else:
        urls = functions.get_linklist_by_title(title)
        for i in range(len(urls)):
            video = functions.search_video_data(urls[i])
            video['number'] = i+1
            videos_list.append(video)           
    return render_template("index.html", videos = videos_list)

@app.route('/download', methods=["POST"])
def download():
    global current_title, videos_list
    
    action, video_number = request.form["button"], int(request.form["data"])
    #print("Entered action:", action, "entered video id", video_number)

    # validate number
    if video_number < 0 or video_number > len(videos_list): # do nothing, for safety
        return render_template("index.html", videos = videos_list)

    if action == "Download":
        #print("downloading")
        stream, current_title = functions.get_stream(videos_list[video_number-1])
        stream.download(filename='temp-download.txt', timeout=60)
        # only one file can be downloaded at moment
        for each in videos_list:
            each['ready'] = False
        videos_list[video_number-1]['ready'] = True

        flash('File is ready. You can download it pushind button "Save"')
        return render_template("index.html", videos = videos_list)

    elif action == "Save":
        return send_file('temp-download.txt', as_attachment=True, attachment_filename = current_title)


#@app.route('/more', methods=["GET"])
#def more():
#    return render_template("index.html", videos = videos_list)

if __name__ == "__main__":
    app.run(debug=True)  
