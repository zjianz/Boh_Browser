from Utils.data_miner import read_from_storage
from Utils import browser as br
import re

from Core.item    import Item,    item_dict
from Core.aspect  import Aspect,  aspect_dict
from Core.skill   import Skill,   sill_dict
from Core.tome    import Tome,    tome_dict
from Core.station import Station, station_dict

def reach(a:dict[str: int], target:dict[str: int], forbid:dict[str: int]):
    if not all(key in a for key in target):
        return False
    if any(key in a for key in forbid):
        return False
    return all(a[key] >= target[key] for key in target)

def get_zh_of_class(id: str, class_list:list[type]) -> str:
    for cls in class_list:
        test_obj = cls(id)
        if test_obj.zh != '':
            return test_obj.zh
    return ''

def print_item(item:Item, print_source:bool = True):
    aspect_item = item.aspects
    aspect_text = '+'.join([ f'{value}'+Aspect(aspect_id).zh for aspect_id, value in aspect_item.items() if Aspect(aspect_id).zh != '' ])
    print(item.zh + f'({aspect_text})')

    # print source
    if print_source:
        if not hasattr(item, 'source'):
            item.source = {}
        for type, source_list in item.source.items():
            match type:
                case 'reading':
                    print('\t读书')
                    for source in source_list:
                        print('\t\t' + Tome(source).zh)
                case 'recipe':
                    print('\t合成')
                    for source in source_list:
                        skill_dict = br.index_with_re(source, re.compile(r'^s\.'), False)
                        skill_id = br.get_first_key(skill_dict)
                        aspect_dict = br.index_with_re(source, re.compile(r'^(?!s\.)(?!ability).*$'), False)
                        aspect_text = ' + '.join([ f'{value}'+get_zh_of_class(aspect_id, [Aspect, Item]) for aspect_id, value in aspect_dict.items() ])
                        print('\t\t' + Skill(skill_id).zh + ' + ' + aspect_text)
                case 'scrutiny':
                    print('\t检查')
                    for source in source_list[:5]:
                        print('\t\t' + Item(source).zh)
                case 'deck':
                    print('\t卡池')
                    for source in source_list:
                        print('\t\t' + source)

def get_item_list_by_aspect(aspect_list: dict, forbid_list: dict={}, is_print:bool = False):
    result = []
    for item_id in item_dict:
        item = Item(item_id)
        aspect_item = item.aspects
        if item.zh == '':
            continue
        if reach(aspect_item, aspect_list, forbid_list):
            result.append(item)
            if is_print:
                print_item(item)
    return result

if __name__ == '__main__':
    a = get_item_list_by_aspect({'grail': 1, 'tool': 1}, is_print=True)