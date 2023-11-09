from apscheduler.schedulers.background import BackgroundScheduler
import datetime
from flask import Flask
from PIL import Image
from flask_uploads import UploadSet, IMAGES, configure_uploads
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = "secretKey"
app.config["UPLOADED_PHOTOS_DEST"] = "static/uploads"


photos = UploadSet("photos", IMAGES)
configure_uploads(app, photos)


def allowed_filenames(filename):
    not_hidden = filename.split(".")[0] != ""
    allowed_extensions = filename.split(".")[1] in ["jpg", "jpeg", "png", "gif"]

    return not_hidden and allowed_extensions


def compress_image(image, filename):
    name, extension = filename.split(".")
    new_filename = f"{name}_cmprssd.{extension}"
    img = Image.open(image)
    file_path = f'{app.config["UPLOADED_PHOTOS_DEST"]}/{new_filename}'
    img.save(file_path, optimize=True, quality=45)
    return (img, new_filename)


# extensions.py


def cleanup_expired_files(app):
    with app.app_context():
        # Define the expiration period (e.g., 7 days)
        expiration_period = datetime.timedelta(days=7)

        # Get the current time
        current_time = datetime.datetime.now()

        # Set the path to the uploads folder
        upload_folder = app.config["UPLOAD_FOLDER"]

        # Loop through files in the upload folder
        for filename in os.listdir(upload_folder):
            file_path = os.path.join(upload_folder, filename)

            # Check if the file has an expiry timestamp
            try:
                timestamp_str = filename.split("_")[1].split(".")[0]
                upload_time = datetime.datetime.strptime(timestamp_str, "%Y%m%d%H%M%S")
            except (ValueError, IndexError):
                # Skip files without a valid timestamp
                continue

            # Check if the file has expired
            if current_time - upload_time > expiration_period:
                os.remove(file_path)
                print(f"Deleted expired file: {filename}")


def init_scheduler(app):
    scheduler = BackgroundScheduler()

    # Schedule the cleanup task to run every day
    scheduler.add_job(
        cleanup_expired_files, trigger="interval", minutes=30, args=(app,)
    )

    # Start the scheduler
    scheduler.start()

    return scheduler
