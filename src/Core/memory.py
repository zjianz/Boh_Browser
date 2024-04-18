from . import base
from Utils import browser as br
import re

from Utils.data_miner import read_from_storage
memory_dist = read_from_storage(['elements','memory.json'])

class memory(base):
    def __init__(self, id: str):
        dist = memory_dist.get(id)

        super().__init__(id, dist)
        self.source = dist['source']
        self.aspects = br.index_with_re(dist['aspects'], re.compile(r'(?!boost).*$'), False)


if __name__ == '__main__':
    a = memory("music.beguiling")