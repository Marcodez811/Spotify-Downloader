from flask import Flask, render_template, request, redirect, send_file
from main_app import SpotifyDownloader

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "GET":
        return render_template("index.html")
    if request.method == "POST":
        playlist_url = request.form.get("url")
        downloader = SpotifyDownloader(playlist_url)
        downloader.download_musics()
        playlist = downloader.generate_lists()
        return render_template("index.html", data=playlist)

if __name__ == '__main__':
    app.run()