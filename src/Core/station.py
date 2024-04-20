from . import BaseItem
from Utils import browser as br
import re

from Utils.data_miner import read_from_storage
station_dict = read_from_storage(['verbs','library_world.json'])

class Station(BaseItem):
    def __init__(self, id: str):
        dict_id = station_dict.get(id)

        if dict_id is not None:
            super().__init__(id, dict_id)

            self.hints = dict_id['hints']
            self.slots = dict_id['slots']
            self.aspects = br.index_with_re(dict_id['aspects'], re.compile(r'(?!difficulty).*$'), False)

if __name__ == '__main__':
    a = Station("library.altar.ascite")