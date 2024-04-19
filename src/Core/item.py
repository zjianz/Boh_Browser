from . import base
from Utils import browser as br
import re

from Utils.data_miner import read_from_storage
item_dict = read_from_storage(['elements','aspecteditems.json'])

class item(base):
    def __init__(self, id: str):
        dict_id = item_dict.get(id)

        super().__init__(id, dict_id)
        self.source = dict_id.get('source')
        self.aspects = br.index_with_re(dict_id['aspects'], re.compile(r'(?!boost).*$'), False)

if __name__ == '__main__':
    a = item("numen.thre")