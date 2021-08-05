"use strict"


function search_click(){
    document.getElementById("loading").style.display = "block";
    document.getElementById("message_text").innerHTML = "Loading videos...";

}


function download_click(){
    document.getElementById("loading").style.display = "block";
    document.getElementById("message_text").innerHTML = "File is getting ready...";
}

function show_click(video_id, link){
    video_id = video_id.toString()
    if(document.getElementById("show_button".concat(video_id)).value == "Show"){
        document.getElementById("video".concat(video_id)).style.display = "block";
        document.getElementById("show_button".concat(video_id)).value = "Hide"
    }
    else{
        document.getElementById("video".concat(video_id)).style.display = "none";
        document.getElementById("show_button".concat(video_id)).value = "Show"
    }
}

