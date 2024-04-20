from . import *
import re
from Utils import browser as br

from Utils.data_miner import read_from_storage
tome_dict = read_from_storage(['elements','tome.json'])

class Tome(BaseItem):
    def __init__(self, id: str):
        dict_id = tome_dict.get(id)

        if dict_id is not None:
            super().__init__(id, dict_id)
            self.pic_dir = self.get_pic_dir()

            mystery_re = re.compile(r'^mystery\.(.*)$')
            self.challenge = br.index_with_re(dict_id['aspects'], mystery_re)

            award_re = re.compile(r'^mastering\.(.*)$')
            award_list = br.get_first_value(br.index_with_re(dict_id['xtriggers'], award_re))
            self.award = [ { re.sub(r'^x', r's', item.get('id')): item.get('level') } for item in award_list]

            self.language = find_language(dict_id)

    def get_pic_dir(self):
        pic1 = super().get_pic_dir(self.id+'_')
        pic2 = super().get_pic_dir()
        return [pic1, pic2]

def find_language(tar_dict: dict):
    if not 'slots' in tar_dict:
        return None
    if not 'language' in tar_dict['slots']:
        return None
    return br.get_first_key(tar_dict['slots'][0]['required'])

if __name__ == '__main__':
    a=Tome("t.apolloandmarsyas")