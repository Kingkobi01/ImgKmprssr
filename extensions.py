from flask import Flask
from PIL import Image
from flask_uploads import UploadSet, IMAGES, configure_uploads
from flask_sqlalchemy import SQLAlchemy

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
