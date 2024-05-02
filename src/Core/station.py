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
        self.item:BaseItem = None

    def judge(self, item:BaseItem):
        aspects = br.add_dict(item.aspects, {item.id: 1})
        is_essential = essential(aspects, self.essential)
        is_required  = required(aspects, self.required)
        is_forbidden = forbidden(aspects, self.forbidden)
        return is_essential and is_required and is_forbidden

    def is_filled(self) -> bool:
        return self.item != None

    def fill(self, item) -> bool:
        if self.is_filled():
            return False
        self.item = item
        return True

    def remove(self):
        item = self.item
        self.item = None
        return item

class Station(BaseItem):
    def __init__(self, id: str):
        dict_id = station_dict.get(id)

        if dict_id is not None:
            super().__init__(id, dict_id)

            self.hints = dict_id['hints']
            self.slots = { key: Slot(value) for key,value in dict_id['slots'].items() }
            self.aspects = br.index_with_re(dict_id.get('aspects',{}), re.compile(r'(?!difficulty).*$'), False)
            self.UpdateTotal()

    def UpdateTotal(self):
        self.total = { 'aspects':{}, 'item':{} }
        for key in self.slots:
            item = self.slots[key].item
            if item is not None:
                self.total['item'] = br.add_dict(self.total['item'], {item.id: 1})
                self.total['aspects'] = br.add_dict(self.total['aspects'], item.aspects)


    def reset(self, key_list:list=None):
        if key_list == None:
            for key in self.slots:
                self.slots[key].remove()
        else:
            for key in key_list:
                if not key in self.slots:
                    continue
                self.slots[key].remove()
        self.UpdateTotal()

    def apply(self,item:BaseItem) -> bool:
        if 'numen' in self.total['aspects'] and 'numen' in item.aspects:
            return False
        if 'memory' in item.aspects and any([slot.item.id == item.id for slot in self.slots.values() if slot.item]):
            return False
        for key in self.slots:
            if self.slots[key].judge(item):
                if not self.slots[key].is_filled():
                    return True
        return False

    def fill(self, item:BaseItem, locked = []):
        if 'numen' in self.total['aspects'] and 'numen' in item.aspects:
            return False
        if 'memory' in item.aspects and any([slot.item.id == item.id for slot in self.slots.values() if slot.item]):
            return False
        for key in self.slots:
            if self.slots[key].judge(item):
                if self.slots[key].is_filled():
                    if not key in locked:
                        origin_item = self.slots[key].remove()
                        self.slots[key].fill(item)
                        self.UpdateTotal()
                        if not self.fill(origin_item, locked+[key]):
                            self.slots[key].remove()
                            self.slots[key].fill(origin_item)
                            continue
                        else:
                            return True
                    continue
                self.slots[key].fill(item)
                self.UpdateTotal()
                return True
        return False

    def is_full(self):
        return all([ slot.is_filled() for slot in self.slots.values() ])

if __name__ == '__main__':
    a = Station("library.telescope")
    from Core.item import Item
    ite1 = Item('mazarine.fife')
    ite2 = Item('mazarine.fife')
    mem  = Item('ascendant.harmony')