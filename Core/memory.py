from . import core

class memory(core):
    def __init__(self, dist):
        self.id = dist['id']
        self.aspect = dist['aspect']
        self.zh = dist['zh']
        self.source = dist['source']