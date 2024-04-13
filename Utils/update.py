from . import zh, data_miner as DATA, browser as br
from . import *
import os,re

# convert raw data to storage
def add_source(mem_list, mem_id, source_type, source_id):
    for mem in mem_list:
        if br.get_value_of_key(mem, 'id') == mem_id:
            if not 'source' in mem:
                mem['source'] = {}
            if source_type in mem['source']:
                mem['source'][source_type].append(source_id)
            else:
                mem['source'][source_type] = [source_id]
    return mem_list



def storage_zh():
    for root, dirs, files in os.walk(DATA.zh_dir):
            for file in files:
                if file.endswith('.json'):
                    file_path = os.path.join(root, file)
                    temp_json = DATA.raw_json_reader(file_path)
                    temp_folder = next(iter(temp_json.keys()))
                    temp_dist = temp_json[temp_folder]
                    temp_dist = [{'id': br.get_value_of_key(d, 'id'), 'label': br.get_value_of_key(d, 'label')} for d in temp_dist]
                    DATA.write_to_storage(['zh',temp_folder,file],temp_dist)
    return

def storage_aspected_items():# and aspects
    aspect_list = DATA.raw_json_reader(r'elements/_aspects.json')['elements']
    aspected_items_list = DATA.raw_json_reader(r'elements/aspecteditems.json')['elements']

    # beast, beverage, blank, bust, cache, candle... are separated by "inherits"
    aspected_items_classed = {}
    for item in aspected_items_list:
        inherit = item.get('inherits')
        if inherit != None:
            inherit = 'else' if inherit == '_' else re.sub('_([^\.]*).*',r'\1',inherit)
            if not inherit in aspected_items_classed:
                aspected_items_classed[inherit] = []
            aspected_items_classed[inherit].append(item)


    # modify memory
    memory_list = aspected_items_classed['memory']
    tome_list = DATA.raw_json_reader(r'elements/tomes.json')['elements']

    # keep id, unique, aspects
    memory_list = [br.keep_key(mem, ['id','unique','aspects']) for mem in memory_list]

    # add tome to memory as a source
    for tome in tome_list:
        xtriggers = tome["xtriggers"]
        mem_id = next((value for key, value in xtriggers.items() if key.startswith('reading.')),[{'id':None}])[0]['id']
        memory_list = add_source(memory_list, mem_id, 'reading', br.get_value_of_key(tome,'id'))

    aspected_items_classed['memory'] = memory_list


    # modify others
    for inherit in aspected_items_classed.keys():
        if inherit == 'memory':
            continue
        for i,item in enumerate(aspected_items_classed[inherit]):
            new_item = br.keep_key(item, ['id', 'aspects', 'xtriggers'])
            aspected_items_classed[inherit][i] = new_item
            item_id = br.get_value_of_key(item, 'id')
            trig = new_item.get('xtriggers')
            if trig != None:
                for trig_type, trig_result in trig.items():
                        #         "scrutiny": [
                        #              {
                        #                  "id": "mem.hindsight",
                        #                  "morpheffect": "spawn",
                        #                  "level": 1
                        #              },
                        #              {
                        #                  "id": "numen.unde",
                        #                  "morpheffect": "transform"
                        #              }
                        #          ]
                        result_ids = [br.get_value_of_key(result, 'id') for result in trig_result] if isinstance(trig_result, list) else [trig_result]
                        for result_id in result_ids:
                            memory_list = add_source(memory_list, result_id, trig_type, item_id)


    # write data to storage
    for inherit in aspected_items_classed.keys():
        DATA.write_to_storage(['elements', inherit+".json"], aspected_items_classed[inherit])
    DATA.write_to_storage(['elements','tome.json'], tome_list)
    return aspected_items_classed