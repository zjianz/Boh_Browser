import json
import os.path as path
import chardet
import re

base_dir = r'D:/SoftWare/Steam/steamapps/common/Book of Hours/bh_Data/StreamingAssets/bhcontent/core'

def detect_encoding(file_path): # Foolish...
    with open(file_path, 'rb') as f:
        raw_data = f.read()
        result = chardet.detect(raw_data)
        return result['encoding']

def json_reader(rel_dir):
    file_dir = path.join(base_dir,rel_dir)
    with open(file_dir, 'r', encoding=detect_encoding(file_dir)) as f:
        file = f.read()
        file_fixed = re.sub(r'\.[ ]\n', r'.', file)
        file_fixed = re.sub('ID', 'id', file_fixed)
        file_fixed = re.sub(r'\.\n', r'.', file_fixed)
        file_fixed = re.sub(r'\.\n', r'.', file_fixed) # Foolish...
        data = json.loads(file_fixed)
    return data

def search_by_id(tar_list, tar_id):
    result = next((d for d in tar_list if d.get('id') == tar_id), None)
    if(result == None):
        print("id \"{0}\" not found in list!".format(tar_id))
    return result

def is_greater_than(a, b):
    if not all(key in a for key in b):
        return False
    return all(a[key] > b[key] for key in b)

def search_by_aspect(tar_list, tar_aspect_dict):
    # all target that has aspect higher than tar_aspect_dict
    result = [d for d in tar_list if is_greater_than(d.get("aspects"), tar_aspect_dict)]
    return result