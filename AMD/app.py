# 1. Imports
from flask import Flask, request, jsonify, send_file
import yt_dlp

# 2. Create app instance
app = Flask(__name__)

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

    file_path = download_video(url)

    print("Downloaded file:", file_path)

    return send_file(file_path, as_attachment=True)

def download_video(url):
    ydl_opts = {
        "outtmpl": "downloads/%(id)s.%(ext)s",
        "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]",
        "merge_output_format": "mp4"
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)

        # YOU need to understand this line
        file_path = ydl.prepare_filename(info)

        return file_path

# 8. Run server
if __name__ == "__main__":
    app.run(debug=True)