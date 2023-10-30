from PIL import Image

import os
from datetime import datetime, timedelta


def compress_image(input_path, output_path, format="JPEG", quality=65):
    try:
        img = Image.open(input_path)
        img.save(output_path, format, quality=quality)
        return output_path
    except Exception as e:
        print(f"Image compression failed:{str(e)}")
        return False


def delete_old_images():
    folder = "uploads"
    days_to_keep = 30  # Adjust as needed
    now = datetime.now()

    try:
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            file_time = datetime.fromtimestamp(os.path.getctime(file_path))
            if (now - file_time) > timedelta(days=days_to_keep):
                os.remove(file_path)
    except Exception as e:
        print(f"Error deleting old files: {str(e)}")
