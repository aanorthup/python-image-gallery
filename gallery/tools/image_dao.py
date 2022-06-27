from gallery.tools.db import *
from gallery.tools.image import Image
from gallery.tools.image_helper import ImageHelper
from gallery.tools.s3 import put_object


class ImageDao(ImageHelper):

    def __init__(self):
        pass

    def get_images_for_username(self, username):
        result = []
        cursor = db.execute("select img_name from s3_imgs where username=%s;", (username,))
        for t in cursor.fetchall():
           result.append(t[0])
        return result

    def add_image(self, bucket, location, username, image):
        res = execute("INSERT INTO images (file, owner) VALUES (%s, %s)", (location, username))
        put_object(bucket, location, image)

        return res
