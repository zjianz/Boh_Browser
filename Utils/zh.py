from . import data_miner as DATA
from . import browser
import os
import re

def get_value(tar_dict, tar_key): # damn A.K.
    # search for damn UPPER/lower case
    if tar_key == 'id':
        value = tar_dict.get('id') or tar_dict.get('Id')
    if tar_key == 'label':
        value = tar_dict.get('label') or tar_dict.get('Label')

    if value != None:
        value = re.sub(' ', '', value) # remove damn space
    return value

def update_from_game_folder():
    for root, dirs, files in os.walk(DATA.zh_dir):
            for file in files:
                if file.endswith('.json'):
                    file_path = os.path.join(root, file)
                    temp_json = DATA.raw_json_reader(file_path)
                    temp_folder = next(iter(temp_json.keys()))
                    temp_dist = temp_json[temp_folder]
                    temp_dist = [{'id': get_value(d, 'id'), 'label': get_value(d, 'label')} for d in temp_dist]
                    DATA.write_to_storage(['zh',temp_folder,file],temp_dist)

def get_zh(tar_file, tar_id):
    tar_list = DATA.read_from_storage(tar_file)
    result = browser.get_key_value(tar_list, "id", tar_id)
    return result['label']

def from_zh(tar_file, tar_zh):
    tar_list = DATA.read_from_storage(tar_file)
    result = browser.get_key_value(tar_list, "label", tar_zh)
    return result['id'] if result != None else None