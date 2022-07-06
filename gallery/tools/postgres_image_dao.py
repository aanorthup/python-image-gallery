from gallery.tools.db import *
from gallery.tools.image import Image
from gallery.tools.image_dao import ImageDAO
from gallery.tools.s3 import *

class PostgresImageDAO(ImageDAO):
    def __init__(self):
        pass

    def get_images_by_username(self, username):
        result = []
        cursor = execute("select title, username from images where username=%s;", (username,))
        for t in cursor.fetchall():
            result.append(Image(t[0], t[1]))
        return result

    def add_image(self, image):
        query = "insert into images (title, username) values(%s, %s);"
        try:
            return execute(query, (image.title, image.username))
        except:
            print("Unexpected error: ")
