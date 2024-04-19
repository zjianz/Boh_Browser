import re
from . import data_miner as DATA

def get_key_with_value(tar_list, tar_key, tar_value):
    result = next((d for d in tar_list if d.get(tar_key) == tar_value), None)
    if(result == None):
        print("{0}: \"{1}\" not found in list!".format(tar_key,tar_value))
    return result

def keep_key(tar_dict, key_list):
    full_pattern = '|'.join(key_list)
    for key,value in tar_dict.items():
        new_value = {v_key: value.get(v_key) for v_key in value.keys() if re.match(full_pattern, v_key)}
        tar_dict[key] = new_value

def is_greater_than(a, b):
    if not all(key in a for key in b):
        return False
    return all(a[key] > b[key] for key in b)

def search_by_aspect(tar_list, tar_aspect_dict):
    # all target that has aspect higher than tar_aspect_dict
    result = [d for d in tar_list if is_greater_than(d.get("aspects"), tar_aspect_dict)]
    return result

def add_dict(prev: dict, adder: dict) -> dict:
    result = prev.copy()
    for key_add, value_add in adder.items():
        if not key_add in result:
            result[key_add] = value_add
        elif not type(result[key_add]) == type(value_add):
            raise TypeError
        else:
            if isinstance(result[key_add], list):
                result[key_add] += value_add
            if isinstance(result[key_add], dict):
                result[key_add] = add_dict(result[key_add], value_add)
    return result

def get_first_key(tar_dict: dict):
    return next(iter(tar_dict.keys()))

def get_first_value(tar_dict: dict):
    return tar_dict[get_first_key(tar_dict)]

def index_with_re(tar_dict: dict, tar_id: re.Pattern, catch = True, repl = r'\1') -> dict:
    matched_items = {}
    for key in tar_dict:
        if tar_id.match(key):
            if catch:
                tar_key = re.sub(tar_id, repl, key)
            else:
                tar_key = key
            matched_items[tar_key] = tar_dict[key]
    return matched_items

def add_zh(tar_dict: dict):
    for key in tar_dict:
        zh_v = get_zh(key)
        if zh_v != None:
            tar_dict[key]['zh'] = zh_v

def get_zh(tar_id: str):
    zh_dict = DATA.read_from_storage('zh.json')
    return zh_dict.get(tar_id, None)