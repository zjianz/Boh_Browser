from . import data_miner as DATA
from . import browser as br

def get_zh(tar_file, tar_id):
    tar_list = DATA.read_from_storage(tar_file)
    result = br.get_key_with_value(tar_list, "id", tar_id)
    return result['label']

def from_zh(tar_file, tar_zh):
    tar_list = DATA.read_from_storage(tar_file)
    result = br.get_key_with_value(tar_list, "label", tar_zh)
    return result['id'] if result != None else None