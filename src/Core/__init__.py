from Utils import textrue_dir
from os import path

class BaseItem():
    def __init__(self, id: str, dict_id: dict):
        self.id = id
        if dict_id is not None:
            self.zh = dict_id.get('zh', '')
        else:
            self.zh = ''
        self.pic_dir = self.get_pic_dir()

    def get_pic_dir(self, id = None):
        if id == None:
            id = self.id
        dir = path.join(textrue_dir, id + '.png')
        if path.exists(dir):
            return dir
        return None
