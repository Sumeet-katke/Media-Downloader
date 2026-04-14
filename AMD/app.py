# 1. Imports
from flask import Flask, request, jsonify, send_file
import yt_dlp, os, glob

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

    if not url:
        return jsonify({"error": "Missing url"}), 400

    # 6. Debug print
    print("Received URL:", url)

    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    file_path = download_video(url)

    print("Downloaded file:", file_path)

    response = send_file(file_path, as_attachment=True)

    def cleanup():
        if os.path.exists(file_path):
            os.remove(file_path)

    response.call_on_close(cleanup)

    return response 

def download_video(url):
    ydl_opts = {
        "outtmpl": os.path.join(DOWNLOAD_DIR, "%(id)s.%(ext)s"),
        "format": (
            "bestvideo[vcodec^=avc1]+bestaudio[acodec^=mp4a]/"
            "bestvideo[ext=mp4]+bestaudio[ext=m4a]/"
            "best[ext=mp4]"
        ),
        "merge_output_format": "mp4",
        "recodevideo": "mp4",
        "postprocessors": [{
            "key": "FFmpegVideoConvertor",
            "preferedformat": "mp4"
        }],
        "cookiefile": "cookies.txt"
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)

        # Prefer the final MP4 output path.
        file_id = info["id"]
        expected_mp4 = os.path.join(DOWNLOAD_DIR, f"{file_id}.mp4")

        if os.path.exists(expected_mp4):
            return expected_mp4

        # Fallback: pick the newest file for this id if mp4 wasn't produced.
        matches = glob.glob(os.path.join(DOWNLOAD_DIR, f"{file_id}.*"))

        if not matches:
            raise FileNotFoundError(f"Downloaded file not found for id {file_id}")

        file_path = max(matches, key=os.path.getmtime)

        return file_path

# 8. Run server
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )