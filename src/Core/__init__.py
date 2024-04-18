from Utils import textrue_dir
from os import path

class base():
    def __init__(self, id: str, dist: dict):
        self.id = id
        self.zh = dist['zh']
        self.pic_dir = self.get_pic_dir()

    def get_pic_dir(self, id = None):
        if id == None:
            id = self.id
        dir = path.join(textrue_dir, id + '.png')
        if path.exists(dir):
            return dir
        return None
