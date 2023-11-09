from flask import render_template, url_for, send_from_directory, request
from extensions import app, photos, compress_image, allowed_filenames, init_scheduler
from forms import UploadForm
import os


# Initialize the scheduler
scheduler = init_scheduler(app)


@app.route("/", strict_slashes=False)
def index():
    return render_template("index.html")


@app.route("/about", strict_slashes=False)
def about():
    return render_template("about.html")


# @app.route("/upload")
# def upload_form():
#     form = UploadForm()
#     return render_template("upload.html", form=form, img_url=None)


@app.route("/image/<filename>", strict_slashes=False)
def get_image(filename):
    return send_from_directory(app.config["UPLOADED_PHOTOS_DEST"], filename)


@app.route("/compress", methods=["GET", "POST"], strict_slashes=False)
def upload():
    form = UploadForm()

    if request.method == "POST" and form.validate_on_submit():
        image = form.image.data
        filename = image.filename

        if allowed_filenames(filename):
            _, new_filename = compress_image(image, filename)
            img_url = url_for("get_image", filename=new_filename)

            # image_description = describe_image(
            #     img_path=f"{app.config['UPLOADED_PHOTOS_DEST']}/{new_filename}"
            # )
    else:
        img_url = None

    return render_template("upload.html", form=form, img_url=img_url)


if __name__ == "__main__":
    if not os.path.exists(app.config["UPLOADED_PHOTOS_DEST"]):
        os.makedirs(app.config["UPLOADED_PHOTOS_DEST"])
    app.run()
