from flask import Flask, render_template, request, redirect
from youtubesearchpython import Video, Channel, Playlist, playlist_from_channel_id
from json import load, dumps

app = Flask(__name__)

def first_live(playlist):
    for video in playlist['videos']:
        if video['liveStreamingDetails']['actualStartTime'] != None:
            return video

def gen_link(id, phone="pc", short=False):
    print(f"phone is {phone}")
    if phone == "android":
        link = f"vnd.youtube:{id}"
    elif phone == "iphone":
        link = f"youtube://watch?v={id}"
    else:
        link = f"https://www.youtube.com/watch?v={id}"
    print(link)
    return link

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
    ctype = ctype.lower()
    playlist = Playlist(playlist_from_channel_id(channel))
    video_data = Video.get(playlist.videos[0]['id'])

    with open("video_data.json", "w") as f:
        f.write(dumps(video_data, indent=4))
    
    if ctype in ["live", "stream", "streaming", "l"]:
        for video in playlist.videos:
            if "streamed" in video["accessibility"]["title"].lower():
                return redirect(gen_link(video["id"], phone=phone), code=302)
    else:
        for video in playlist.videos:
            video_data = Video.get(video["id"])
            if ctype in ["video", "videos", "vid", "vids", "v"]:
                if video_data["isLiveContent"] == False and "short" not in video_data["title"].lower():
                    gen_link(video["id"], phone)
                    return redirect(gen_link(video["id"], phone=phone), code=302)
            elif ctype in ["shorts", "short", "s"]:
                if video_data["isLiveContent"] == False and "shorts" in video_data["title"].lower() + " " + video_data["description"].lower() and int(video_data["duration"]["secondsText"]) < 60:
                    return redirect(gen_link(video["id"], phone=phone), code=302)
    return redirect(f"https://youtube.com/channel/{channel}", code=302)

@app.route("/")
def empty():
    return redirect("https://google.com", code=302)


@app.route("/<channel>")
def channel(channel):
    return main(channel, "live")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")