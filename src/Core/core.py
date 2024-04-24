from Utils.data_miner import read_from_storage
from Utils import browser as br
import re

from Core.item    import Item,    item_dict
from Core.aspect  import Aspect,  aspect_dict
from Core.skill   import Skill,   skill_dict
from Core.tome    import Tome,    tome_dict
from Core.station import Station, station_dict
from Core.recipe  import Recipe,  recipe_dict
from Core.condition import Condition as Cd, CompositeCondition

def get_item_list_by_aspect(cond: CompositeCondition, is_print: bool=False, print_source: bool=False):
    result = []
    for item_id in item_dict:
        item = Item(item_id)
        aspect_item = item.aspects
        if item.zh == '':
            continue
        if cond.evaluate(aspect_item):
            result.append(item)
            if is_print:
                item.print(print_source)
    return result

if __name__ == '__main__':
    print("a = get_item_list_by_aspect((Cd('memory') | Cd('tool') | Cd('sustenance')) & Cd('grail'), is_print=True, print_source=False)")