from flask import Flask, request, render_template, send_file
import os
import uuid
import yt_dlp

app = Flask(__name__)
DOWNLOAD_DIR = "/tmp"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
from urllib.parse import urlparse, parse_qs

raw_url = request.form["url"]
parsed = urlparse(raw_url)
query = parse_qs(parsed.query)
video_id = query.get("v", [None])[0]
url = f"https://www.youtube.com/watch?v={video_id}" if video_id else raw_url
        temp_id = uuid.uuid4().hex
        mp3_path = os.path.join(DOWNLOAD_DIR, f"{temp_id}.%(ext)s")

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': mp3_path,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        final_mp3 = os.path.join(DOWNLOAD_DIR, f"{temp_id}.mp3")
        return send_file(final_mp3, as_attachment=True, download_name="audio.mp3")

    return render_template("index.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
