from extensions import photos
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import SubmitField


class UploadForm(FlaskForm):
    image = FileField(
        validators=[
            FileAllowed(photos, "Only images are allowed"),
            FileRequired("Please insert an image before submitting"),
        ]
    )
    submit = SubmitField(label="Submit and Compress")
