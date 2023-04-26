import os
# pip install pillow
from PIL import Image

from flask import current_app

def add_novel_pic(pic_upload, novelTitle):

    filename = pic_upload.filename
    ext_type = filename.split('.')[-1]
    storage_filename = str(novelTitle) + '.' +ext_type
    filepath = os.path.join(current_app.root_path, 'static\images', storage_filename)

    output_size = (200, 200)

    pic = Image.open(pic_upload)
    pic.thumbnail(output_size)
    pic.save(filepath)

    storage_area = "static\images\\"

    return storage_area + storage_filename
