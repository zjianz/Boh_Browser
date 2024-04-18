from . import *
import re
from Utils import browser as br

from Utils.data_miner import read_from_storage
tome_dist = read_from_storage(['elements','tome.json'])

class tome(base):
    def __init__(self, id: str):
        dist = tome_dist.get(id)
        super().__init__(id, dist)
        self.pic_dir = self.get_pic_dir()

        mystery_re = re.compile(r'^mystery\.(.*)$')
        self.challenge = br.index_with_re(dist['aspects'], mystery_re)

        award_re = re.compile(r'^mastering\.(.*)$')
        award_list = br.get_first_value(br.index_with_re(dist['xtriggers'], award_re))
        self.award = [ { re.sub(r'^x', r's', item.get('id')): item.get('level') } for item in award_list]

        self.language = find_language(dist)

    def get_pic_dir(self):
        pic1 = super().get_pic_dir(self.id+'_')
        pic2 = super().get_pic_dir()
        return [pic1, pic2]

def find_language(tar_dist: dict):
    if not 'slots' in tar_dist:
        return None
    if not 'language' in tar_dist['slots']:
        return None
    return br.get_first_key(tar_dist['slots'][0]['required'])

if __name__ == '__main__':
    a=tome("t.apolloandmarsyas")