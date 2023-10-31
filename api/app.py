from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler
from utils import compress_image, delete_old_images


app = Flask(__name__)

CORS(app)


@app.route("/", methods=["GET"], strict_slashes=False)
def index():
    return '<h1 style="font-family:monospace">Welcome to ImgKmprssr&#174;</h1>'


@app.route("/compress", methods=["POST"], strict_slashes=False)
def handle_compress():
    if "image" not in request.files:
        return jsonify({"error": "No Image provided"}), 400

    image = request.files.get("image")

    if image.filename == "":
        return jsonify({"error": "No selected image file"}), 400
    try:
        new_filename = f"images/{image.filename.split('.')[0]}_cmprssd.jpeg"

        compressed_path = compress_image(image, new_filename)

        if compressed_path:
            # Set the correct MIME type for JPEG
            mimetype = "image/jpeg"

            return jsonify(
                {
                    "success": True,
                    "result": send_file(
                        compressed_path,
                        as_attachment=True,
                        mimetype=mimetype,
                        download_name=new_filename,
                    ),
                }
            )
    except Exception as e:
        return jsonify({"error": f"{str(e)}"}), 400


scheduler = BackgroundScheduler(daemon=True)
scheduler.add_job(delete_old_images, "interval", days=1)  # Run daily


if __name__ == "__main__":
    scheduler.start()
    app.run(host="0.0.0.0", port=5000, threaded=True, debug=True)
