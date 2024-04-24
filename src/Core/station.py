from . import BaseItem
from Utils import browser as br
import re

from Utils.data_miner import read_from_storage
station_dict = read_from_storage(['verbs','library_world.json'])

def essential(a:dict, target:dict):
    return all([ (key in a and a[key] >= target[key]) for key in target ])

def required(a:dict, target:dict):
    return any([ (key in a and a[key] >= target[key]) for key in target ])

def forbidden(a:dict, target:dict):
    return not required(a, target)

class Slot(object):
    def __init__(self, dict_id:dict) -> None:
        self.essential = dict_id.get('essential',{})
        self.required  = dict_id.get('required', {})
        self.forbidden = dict_id.get('forbidden',{})
        self.filled = False

    def judge(self, item:BaseItem):
        aspects = item.aspects
        is_essential = essential(aspects, self.essential)
        is_required  = required(aspects, self.required)
        is_forbidden = forbidden(aspects, self.forbidden)
        return is_essential and is_required and is_forbidden

class Station(BaseItem):
    def __init__(self, id: str):
        dict_id = station_dict.get(id)

        if dict_id is not None:
            super().__init__(id, dict_id)

            self.hints = dict_id['hints']
            self.slots = { key: Slot(value) for key,value in dict_id['slots'].items() }
            self.aspects = br.index_with_re(dict_id.get('aspects',{}), re.compile(r'(?!difficulty).*$'), False)
            self.total = { 'aspects':{}, 'item':{} }

    def reset(self):
        self.total = { 'aspects':{}, 'item':{} }
        for key in self.slots:
            self.slots[key].filled = False

    def fill(self, item:BaseItem):
        for key in self.slots:
            if not self.slots[key].judge(item):
                continue
            else:
                self.slots[key].filled = True
                self.total['item'] = br.add_dict(self.total['item'], {item.id: 1})
                self.total['aspects'] = br.add_dict(self.total['aspects'], item.aspects)
                return True
        return False

if __name__ == '__main__':
    a = Station("library.altar.ascite")