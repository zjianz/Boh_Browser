from . import *
import json
import os.path as path
import os
from datetime import date
import shutil
import chardet
import re

with open(path.join(game_folder,'version.txt')) as f:
    GAME_VER = f.read()

def detect_encoding(file_path): # Foolish...
    with open(file_path, 'rb') as f:
        raw_data = f.read()
        result = chardet.detect(raw_data)
        return result['encoding']

def raw_json_reader(rel_dir):
    file_dir = path.join(core_dir,rel_dir)
    with open(file_dir, 'r', encoding=detect_encoding(file_dir)) as f:
        file = f.read()
        file_fixed = re.sub(r'\.[ ]\n', r'.', file)
        file_fixed = re.sub('ID', 'id', file_fixed)
        file_fixed = re.sub(r'\n', r'', file_fixed) # Foolish...
        data = json.loads(file_fixed)
    return data

def write_to_storage(tar_file,tar_dist,version=GAME_VER,keep=5):

    storage_dir_ver = path.join(storage_dir, version)
    storage_dir_date = path.join(storage_dir_ver, str(date.today()))
    if isinstance(tar_file,list):
        file_dir = path.join(storage_dir_date, *tar_file)
    else:
        file_dir = path.join(storage_dir_date, tar_file)

    # create nessary path
    file_parent = path.dirname(file_dir)
    if not path.exists(file_parent):
        os.makedirs(file_parent, exist_ok=True)

    # overwrite file
    with open(file_dir, 'w+', encoding='utf-8') as file:
        json.dump(tar_dist, file, skipkeys=True, ensure_ascii=False, indent=4)

    # delete old folders
    subdirs = [d for d in os.listdir(storage_dir_ver) if path.isdir(path.join(storage_dir_ver, d))]
    subdirs.sort(key=lambda x: path.getmtime(path.join(storage_dir_ver, x)), reverse=True)
    for subdir in subdirs[keep:]:
        subdir_path = path.join(storage_dir_ver, subdir)
        try:
            shutil.rmtree(subdir_path)
        except OSError as e:
            print(f"Error: {subdir_path} : {e.strerror}")

def read_from_storage(tar_file,version=GAME_VER):
    storage_dir_ver = path.join(storage_dir, version)

    subdirs = [d for d in os.listdir(storage_dir_ver) if path.isdir(path.join(storage_dir_ver, d))]
    subdirs.sort(key=lambda x: path.getmtime(path.join(storage_dir_ver, x)), reverse=True)
    newest = subdirs[0]
    storage_dir_date = path.join(storage_dir_ver, newest)

    if isinstance(tar_file,list):
        file_dir = path.join(storage_dir_date, *tar_file)
    else:
        file_dir = path.join(storage_dir_date, tar_file)

    with open(file_dir, 'r', encoding='utf-8') as file:
        result = json.load(file)
    return result