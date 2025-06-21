from flask import Flask, request, render_template, send_file
from pytube import YouTube
import os
import uuid
import subprocess

app = Flask(__name__)
DOWNLOAD_DIR = "/tmp"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form["url"]
        yt = YouTube(url)
        audio_stream = yt.streams.filter(only_audio=True).first()
        temp_id = uuid.uuid4().hex
        mp4_path = os.path.join(DOWNLOAD_DIR, f"{temp_id}.mp4")
        mp3_path = os.path.join(DOWNLOAD_DIR, f"{temp_id}.mp3")

        audio_stream.download(filename=mp4_path)

        subprocess.run(["ffmpeg", "-i", mp4_path, "-vn", "-ab", "192k", "-ar", "44100", "-y", mp3_path])

        os.remove(mp4_path)

        return send_file(mp3_path, as_attachment=True, download_name=f"{yt.title}.mp3")

    return render_template("index.html")
