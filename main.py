from flask import Flask, render_template, request, redirect
from youtubesearchpython import Video, Channel, Playlist, playlist_from_channel_id
from json import load, dumps
from datetime import datetime

app = Flask(__name__)

# time, channel_id, resultant_id, type
logs = []

livee_accepted = ["live", "stream", "streaming", "l"]
short_accepted = ["short", "s", "shorts", "shortlink", "shortlink", "shortlinks", "shortlinks"]
video_accepted = ["video", "videos", "vid", "vids", "v"]

def gen_link(id, phone="pc", channel=False):
    if channel:
        if phone == "android":
            return f"vnd.youtube://channel/{id}"
        elif phone == "iphone":
            return f"youtube://www.youtube.com/channel/{id}"    
        else:
            return f"https://www.youtube.com/channel/{id}"
    print(f"phone is {phone}")
    if phone == "android":
        link = f"vnd.youtube:{id}"
    elif phone == "iphone":
        link = f"youtube://watch?v={id}"
    else:
        link = f"https://www.youtube.com/watch?v={id}"
    print(link)
    return link

def get_live(playlist):
    for video in playlist.videos:
        video_data = Video.get(video["id"])
        if not video_data["isLiveContent"]:
            continue
        return video["id"]
    return ""

def get_short(playlist):
    for video in playlist.videos:
        video_data = Video.get(video["id"])
        video_reso = video_data["streamingData"]["adaptiveFormats"][0] 
        if video_data["isLiveContent"]:
            print("is live content")
            continue
        if int(video_reso["width"]) > int(video_reso["height"]):
            print("is not vertical")
            continue
        if int(video_data["duration"]["secondsText"]) > 61:
            print("is longer than 60 seconds")
            continue

        return video["id"]
    return ""

def get_video(playlist, phone="pc"):
    for video in playlist.videos:
        video_data = Video.get(video["id"])
        video_reso = video_data["streamingData"]["adaptiveFormats"][0] 
        if(video_data["isLiveContent"]):
            print("is live content")
            continue
        if int(video_reso["width"]) < int(video_reso["height"]) or int(video_data["duration"]["secondsText"]) < 61:
            print("is vertical or shorter than 60 seconds")
            continue
        return video["id"]
    return ""

@app.route("/<channel>", methods=["GET", "POST"])
def channel_only(channel):
    print("channel_only")
    return main(channel, "v")
@app.route("/<channel>/<ctype>", methods= ["GET", "POST"])
def main(channel, ctype):    
    #print methods used
    print(request.method)
    #find if the request is from a phone or a computer
    if "Android" in request.headers.get('User-Agent'):
        phone = "android"
    elif "iPhone" in request.headers.get('User-Agent'):
        phone = "iphone"
    else:
        phone = "pc"
        print(request.user_agent.platform)
        print(request.user_agent)
    print(phone)
    if not ctype:
        return redirect(gen_link(channel, phone, channel=True))
    ctype = ctype.lower()
    playlist = Playlist(playlist_from_channel_id(channel))
    video_data = Video.get(playlist.videos[0]['id'])

    with open("video_data.json", "w") as f:
        f.write(dumps(video_data, indent=4))
    
    vid = ""
    ctype = ctype[0]
    for prev in logs:
        if ctype == prev["type"] and channel == prev["channel_id"] and (datetime.now() - prev["time"]).seconds < 300:
            print("found in previous attempt")
            vid = prev["resultant_id"]
            return redirect(gen_link(vid, phone))
            break
    if ctype in livee_accepted:
        vid = get_live(playlist=playlist)
    elif ctype in short_accepted:
        vid = get_short(playlist=playlist)
    elif ctype in video_accepted:
        vid = get_video(playlist=playlist)
    else:
        return empty(channel)
    print(vid)
    ch = False

    if not vid:
        vid = channel
        ch = True

    dic = {"time": datetime.now(), "channel_id": channel, "resultant_id": vid, "type": ctype}
    logs.append(dic)
    print("added to logs cuz not found")
    return redirect(gen_link(vid, phone, ch))

@app.route("/", methods=["POST", "GET"])
def empty():
    # take input from a text box id = " input"
    if request.method == "GET":
        return render_template("index.html", show=False)
    
    channel = request.form["channel_id"]
    print(f"channel is {channel}")
    if not channel:
        return render_template("index.html", show=False)

    playlist = Playlist(playlist_from_channel_id(channel))
    last_live = get_live(playlist)
    last_short = get_short(playlist)
    last_video = get_video(playlist)
    return render_template("index.html", last_live=last_live, last_short=last_short, last_video=last_video, show=True)

# who wrote this garbage code anyway :P 

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)