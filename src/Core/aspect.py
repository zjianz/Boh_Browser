from . import base
from Utils import browser as br
import re

from Utils.data_miner import read_from_storage
aspect_dict = read_from_storage(['elements','aspects.json'])

class aspect(base):
    def __init__(self, id: str):
        dict_id = aspect_dict.get(id)

        super().__init__(id, dict_id)
        self.pic_dir = self.get_pic_dir()

    def get_pic_dir(self):
        tran_dict = {
            'moon': 'moon #248',
            'winter': 'winter #422'
        }
        id_dir = self.id
        if id_dir in tran_dict:
            id_dir = tran_dict[id_dir]
        id_dir = re.sub(r'^e\.', r'w.', id_dir)
        return super().get_pic_dir(id_dir)


if __name__ == '__main__':
    a = aspect("moon")