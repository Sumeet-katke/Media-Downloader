# 1. Imports
from flask import Flask, request, jsonify, send_file
import yt_dlp, os

# 2. Create app instance
app = Flask(__name__)

# Describing the Download folder 
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOAD_DIR = os.path.join(BASE_DIR, "downloads")

# 3. Routes
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Server is running"})


@app.route("/download", methods=["POST"])
def download():
    # 4. Get JSON data
    data = request.get_json()

    # 5. Extract URL
    url = data.get("url")

    # 6. Debug print
    print("Received URL:", url)

    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    file_path = download_video(url)

    print("Downloaded file:", file_path)

    response = send_file(file_path, as_attachment=True)

    os.remove(file_path)

    return response 

def download_video(url):
    ydl_opts = {
        "outtmpl": os.path.join(DOWNLOAD_DIR, "%(id)s.%(ext)s"),
        "format": (
            "bestvideo[vcodec^=avc1]+bestaudio[acodec^=mp4a]/"
            "bestvideo[ext=mp4]+bestaudio[ext=m4a]/"
            "best[ext=mp4]"
        ),
        "merge_output_format": "mp4"
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)

        # YOU need to understand this line
        file_path = ydl.prepare_filename(info)

        return file_path

# 8. Run server
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )