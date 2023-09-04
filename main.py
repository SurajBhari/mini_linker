from flask import Flask, render_template, request, redirect, url_for
from youtubesearchpython import Video, Channel, Playlist, playlist_from_channel_id
from json import load, dumps
from datetime import datetime

import scrapetube

app = Flask(__name__)

# time, channel_id, resultant_id, type
logs = []

livee_accepted = ["live", "stream", "streaming", "l"]
short_accepted = [
    "short",
    "s",
    "shorts",
    "shortlink",
    "shortlink",
    "shortlinks",
    "shortlinks",
]
video_accepted = ["video", "videos", "vid", "vids", "v"]


def gen_link(id, phone="pc", channel=False):
    if channel:
        if phone == "android":
            return f"vnd.youtube://channel/{id}"
        elif phone == "iphone":
            return f"youtube://www.youtube.com/channel/{id}"
        else:
            return f"https://www.youtube.com/channel/{id}"
    if phone == "android":
        link = f"vnd.youtube:{id}"
    elif phone == "iphone":
        link = f"youtube://watch?v={id}"
    else:
        link = f"https://www.youtube.com/watch?v={id}"
    return link


def get_live(c_id):
    return scrapetube.get_channel(c_id, content_type="streams")


def get_short(c_id):
    return scrapetube.get_channel(c_id, content_type="shorts")


def get_video(c_id):
    return scrapetube.get_channel(channel_id=c_id, content_type="videos")


@app.route("/<channel>", methods=["GET", "POST"])
def channel_only(channel):
    return redirect(gen_link(channel, channel=True))


@app.route("/<channel>/<ctype>", methods=["GET", "POST"])
def main(channel, ctype):
    if "Android" in request.headers.get("User-Agent"):
        phone = "android"
    elif "iPhone" in request.headers.get("User-Agent"):
        phone = "iphone"
    else:
        phone = "pc"
    if not ctype:
        return redirect(gen_link(channel, phone, channel=True))
    ctype = ctype.lower()

    vid = ""
    ctype = ctype[0]
    for prev in logs:
        if (datetime.now() - prev["time"]).seconds > 360:
            logs.remove(prev)
            # clean to keep up performance
            continue
        if (
            ctype == prev["type"]
            and channel == prev["channel_id"]
            and (datetime.now() - prev["time"]).seconds < 300
        ):
            vid = prev["resultant_id"]
            return redirect(gen_link(vid, phone))
    if ctype in livee_accepted:
        vid = get_live(channel)
    elif ctype in short_accepted:
        vid = get_short(channel)
    elif ctype in video_accepted:
        vid = get_video(channel)
    else:
        return empty(channel)
    ch = False

    if not vid:
        vid = channel
        ch = True
    else:
        try:
            vid = str(next(vid)["videoId"])
        except StopIteration:
            return f"Nothing found for {ctype} for this channel | Are you sure you are not in wrong place ?"
    dic = {
        "time": datetime.now(),
        "channel_id": channel,
        "resultant_id": vid,
        "type": ctype,
    }
    logs.append(dic)
    return redirect(gen_link(vid, phone, ch))


@app.route("/", methods=["POST", "GET"])
def empty():
    # take input from a text box id = " input"
    if request.method == "GET":
        return render_template("index.html", show=False)

    channel = request.form["channel_id"]
    if not channel:
        return render_template("index.html", show=False)

    last_live = url_for("main", channel=channel, ctype="l")
    last_short = url_for("main", channel=channel, ctype="s")
    last_video = url_for("main", channel=channel, ctype="v")
    return render_template(
        "index.html",
        last_live=last_live,
        last_short=last_short,
        last_video=last_video,
        show=True,
    )


# who wrote this garbage code anyway :P

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5555)
