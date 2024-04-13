import re

def get_value_of_key(tar_dict:dict, tar_key:str): # damn A.K.
    # search for damn UPPER/lower case
    if tar_key == 'id':
        value = tar_dict.get('id') or tar_dict.get('Id')
    if tar_key == 'label':
        value = tar_dict.get('label') or tar_dict.get('Label')
    value = tar_dict.get(tar_key)
    if value != None and isinstance(value, str):
        value = re.sub(' ', '', value) # remove damn space
    return value

def get_key_with_value(tar_list, tar_key, tar_value):
    result = next((d for d in tar_list if d.get(tar_key) == tar_value), None)
    if(result == None):
        print("{0}: \"{1}\" not found in list!".format(tar_key,tar_value))
    return result

def keep_key(tar_dict, key_list):
    result = {key: get_value_of_key(tar_dict, key) for key in tar_dict.keys() if key in key_list}
    return result

def is_greater_than(a, b):
    if not all(key in a for key in b):
        return False
    return all(a[key] > b[key] for key in b)

def search_by_aspect(tar_list, tar_aspect_dict):
    # all target that has aspect higher than tar_aspect_dict
    result = [d for d in tar_list if is_greater_than(d.get("aspects"), tar_aspect_dict)]
    return result