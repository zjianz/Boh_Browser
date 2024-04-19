from . import base
from Utils import browser as br
import re

from Utils.data_miner import read_from_storage
sill_dict = read_from_storage(['elements','skills.json'])

class skill(base):
    def __init__(self, id: str):
        dict_id = sill_dict.get(id)

        super().__init__(id, dict_id)

        self.hints = dict_id['hints']
        self.slots = dict_id['slots']
        self.aspects = dict_id['aspects']

if __name__ == '__main__':
    a = skill("library.altar.ascite")