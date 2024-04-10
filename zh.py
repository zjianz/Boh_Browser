import Utils
import os

translation_dir = r'D:/SoftWare/Steam/steamapps/common/Book of Hours/bh_Data/StreamingAssets/bhcontent/loc_zh-hans/'

zh_text = {}

for root, dirs, files in os.walk(translation_dir):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                temp_json = Utils.json_reader(file_path)
                temp_folder = next(iter(temp_json.keys()))
                if temp_folder in zh_text:
                    zh_text[temp_folder] += temp_json[temp_folder]
                else:
                    zh_text[temp_folder] = temp_json[temp_folder]

def get_zh(tar_class, tar_id):
    tar_list = zh_text[tar_class]
    result = Utils.search_by_id(tar_list, tar_id)
    return result['label']