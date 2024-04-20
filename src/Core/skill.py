from . import BaseItem
from Utils import browser as br
import re

from Utils.data_miner import read_from_storage
sill_dict = read_from_storage(['elements','skills.json'])

class Skill(BaseItem):
    def __init__(self, id: str):
        dict_id = sill_dict.get(id)

        if dict_id is not None:
            super().__init__(id, dict_id)
            self.aspects = dict_id['aspects']

if __name__ == '__main__':
    a = Skill("library.altar.ascite")