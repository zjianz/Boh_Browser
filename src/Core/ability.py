from . import BaseItem
from Utils import browser as br
import re

from Utils.data_miner import read_from_storage
ability_dict = read_from_storage(['elements','abilities.json'])

class Ability(BaseItem):
    def __init__(self, id: str):
        dict_id = ability_dict.get(id)
        super().__init__(id, dict_id)

        if dict_id is not None:
            self.aspects = br.index_with_re(dict_id['aspects'], re.compile(r'(?!boost).*$'), False)

if __name__ == '__main__':
    a = Ability("xcho4")