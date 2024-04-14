from . import data_miner as DATA, browser as br
from . import *
import os,re

# convert raw data to storage

def add_source(opt_dist, item):
    key, value = list(item.items())[0]
    trig = value.get('xtriggers')
    if trig != None:
        for trig_type, trig_result in trig.items():
                result_ids = [result.get('id') for result in trig_result] if isinstance(trig_result, list) else [trig_result]
                trig_type = re.sub('^([^.]*)(?:\..*)?$', r'\1', trig_type)
                for result_id in result_ids:
                    if result_id in opt_dist:
                        opt_item = opt_dist[result_id]
                        if not 'source' in opt_item:
                            opt_item['source'] = {}
                        if trig_type in opt_item['source']:
                            opt_item['source'][trig_type].append(key)
                        else:
                            opt_item['source'][trig_type] = [key]

def add_zh(tar_dist: dict):
    zh_dist = DATA.read_from_storage('zh.json')
    for key in tar_dist.keys():
        zh_v = zh_dist.get(key)
        if zh_v != None:
            label = zh_v.get('label')
            if label != None:
                tar_dist[key]['zh'] = label
                continue
        if 'aspects' in tar_dist[key]:
            tar_dist[key]['aspects']['no_zh'] = 1

def storage_zh():
    zh_files = []
    for root, dirs, files in os.walk(DATA.zh_dir):
            for file in files:
                if file.endswith('.json'):
                    file_path = os.path.join(root, file)
                    zh_files.append(file_path)
    zh_data = DATA.raw_json_reader(zh_files)
    br.keep_key(zh_data, ['label'])
    DATA.write_to_storage(['zh.json'],zh_data)
    return

def storage_core():
    # need to excute after storage_zh

    aspect_dict = DATA.raw_json_reader(r'elements/_aspects.json', 'elements')
    tome_dict = DATA.raw_json_reader(r'elements/tomes.json', 'elements')
    aspecteditems_dict = DATA.raw_json_reader(r'elements/aspecteditems.json', 'elements')
    ability_dirs = [r'elements/abilities.json',r'elements/abilities2.json',r'elements/abilities3.json',r'elements/abilities4.json']
    abilities_dict = DATA.raw_json_reader(ability_dirs, 'elements')
    assistance_dict = DATA.raw_json_reader(r'elements/assistance.json', 'elements')

    protoptype_dict = DATA.raw_json_reader(r'elements/_prototypes.json', 'elements')

    # separate memory out of aspected items
    memory_dict = {}
    for key,value in aspecteditems_dict.items():
        if not 'inherits' in value:
            continue
        inherit = value.pop('inherits')
        if inherit != None and inherit != '_':
            inherit = re.sub('_([^\.]*).*',r'\1',inherit)
            value['aspects'][inherit] = 1
            if inherit == 'memory':
                memory_dict[key] = aspecteditems_dict[key]


    # keep id, unique, aspects
    br.keep_key(memory_dict        , [ 'aspects'])
    br.keep_key(aspect_dict        , [ 'ishidden'])
    br.keep_key(tome_dict          , [ 'aspects', 'slots', 'xtriggers'])
    br.keep_key(abilities_dict     , [ 'aspects', 'xtriggers'])
    br.keep_key(assistance_dict    , [ 'aspects', 'slots', 'xtriggers', 'inherits'])
    br.keep_key(aspecteditems_dict , [ 'aspects', 'xtriggers'])

    # add tome to memory as a source
    for id,tome in tome_dict.items():
        add_source(memory_dict, {id: tome})
    for id,aspected_item in aspecteditems_dict.items():
        add_source(memory_dict, {id: aspected_item})
    for id, abi in abilities_dict.items():
        add_source(memory_dict, {id: abi})
    for id, ass in assistance_dict.items():
        add_source(memory_dict, {id: ass})


    # assistance inherits -> asstype via prototypes
    for key,value in assistance_dict.items():
        inherit = value.get('inherits')
        if inherit != None:
            asstype = protoptype_dict[inherit]
            value['assistance_type'] = asstype.get('slots')
            value.pop('inherits')
            assistance_dict[key] = value


    # add zh to items
    add_zh(aspecteditems_dict)
    add_zh(aspect_dict)
    add_zh(tome_dict)
    add_zh(abilities_dict)
    add_zh(memory_dict)
    add_zh(assistance_dict)

    # write data to storage
    DATA.write_to_storage(["aspecteditems.json"], aspecteditems_dict)
    DATA.write_to_storage(['tome.json'], tome_dict)
    DATA.write_to_storage(['abilities.json'], abilities_dict)
    DATA.write_to_storage(['assistance.json'], assistance_dict)
    DATA.write_to_storage(['memory.json'], memory_dict)
    DATA.write_to_storage(['aspects.json'], aspect_dict)
    return

def Update():
    storage_zh()
    storage_core()