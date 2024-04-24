from Utils import texture_dir
from os import path

class BaseItem():
    def __init__(self, id: str, dict_id: dict):
        self.id = id
        if dict_id is not None:
            self.zh = dict_id.get('zh', '')
            self.aspects = dict_id.get('aspects')
        else:
            self.zh = ''
        self.pic_dir = self.get_pic_dir()

    def get_pic_dir(self, id = None):
        if id == None:
            id = self.id
        dir = path.join(texture_dir, id + '.png')
        if path.exists(dir):
            return dir
        return None

    def print(self):
        pass

def get_zh_with_class(id: str, class_list:list[type]) -> str:
    for cls in class_list:
        test_obj = cls(id)
        if test_obj.zh != '':
            return test_obj.zh
    return ''