from . import *
import re
from Utils import browser as br

from Utils.data_miner import read_from_storage
tome_dict = read_from_storage(['elements','tome.json'])

class Tome(BaseItem):
    def __init__(self, id: str):
        dict_id = tome_dict.get(id)
        super().__init__(id, dict_id)

        if dict_id is not None:
            self.pic_dir = self.get_pic_dir()

            mystery_re = re.compile(r'^mystery\.(.*)$')
            self.challenge = br.index_with_re(dict_id['aspects'], mystery_re)

            self.lesson = self.get_lesson(dict_id)

            self.language = find_language(dict_id)

    def get_pic_dir(self):
        pic1 = super().get_pic_dir(self.id+'_')
        pic2 = super().get_pic_dir()
        return [pic1, pic2]

    def get_lesson(self, dict_id):
        master_re = re.compile(r'^mastering\.(.*)$')
        lesson_re  = re.compile(r'^x\.(.*)$')
        lesson_dict = br.index_with_re(
                    br.get_first_value(br.index_with_re(dict_id['xtriggers'], master_re)),
                    lesson_re, True, r's.\1'
                )
        lesson = br.get_first_key(lesson_dict)
        count = br.get_first_value(lesson_dict)['level']
        return {lesson: count}

def find_language(tar_dict: dict):
    if not 'slots' in tar_dict:
        return None
    if not 'language' in tar_dict['slots']:
        return None
    return br.get_first_key(tar_dict['slots']['language']['required'])

if __name__ == '__main__':
    a=Tome("t.apolloandmarsyas")