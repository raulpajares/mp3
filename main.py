
from flask import Flask, request, render_template, send_file
import yt_dlp
import tempfile
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url")
        if not url:
            return render_template("index.html", error="Por favor ingresa un enlace de YouTube.")

        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "audio.mp3")
            ydl_opts = {
                "format": "bestaudio/best",
                "outtmpl": filepath,
                "postprocessors": [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }],
                "quiet": True,
            }

            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                return send_file(filepath, as_attachment=True, download_name="audio.mp3")
            except Exception as e:
                return render_template("index.html", error=f"Error: {e}")
    return render_template("index.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
