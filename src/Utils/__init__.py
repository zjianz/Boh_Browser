import os.path as path
import json

module_dir = path.dirname(__file__)
repository_dir = path.dirname(path.dirname(module_dir))
config_dir = path.join(repository_dir,'config.json')

with open(config_dir, 'r') as config_file:
    config_data = json.load(config_file)

game_folder = config_data['game_folder']

core_dir = path.join(game_folder,r'bh_Data/StreamingAssets/bhcontent/core')
zh_dir = path.join(game_folder,r'bh_Data/StreamingAssets/bhcontent/loc_zh-hans')

storage_dir = path.join(repository_dir, 'data')

texture_dir = path.join(repository_dir, 'Texture2D')