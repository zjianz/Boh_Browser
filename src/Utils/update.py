from . import data_miner as DATA, browser as br
from . import *
import os,re

# convert raw data to storage

def add_source(opt_dist:dict, source_dist:dict):
    for key, value in source_dist.items():
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

def add_source_of_recipe(opt_dist:dict, recipe_dist:dict):
    for key, value in recipe_dist.items():
        effects = value.get('effects')
        if effects != None:
            for effect in effects.keys():
                if effect in opt_dist:
                    opt_item = opt_dist[effect]
                    if not 'source' in opt_item:
                        opt_item['source'] = {}
                    if 'recipe' in opt_item['source']:
                        opt_item['source']['recipe'].append(value.get('reqs'))
                    else:
                        opt_item['source']['recipe'] = [value.get('reqs')]

def storage_zh():
    zh_files = []
    for root, dirs, files in os.walk(DATA.zh_dir):
            for file in files:
                if file.endswith('.json'):
                    file_path = os.path.join(root, file)
                    zh_files.append(file_path)
    zh_data = DATA.raw_json_reader(zh_files)

    new_zh_data = {}
    for id in zh_data:
        if 'label' in zh_data[id]:
            new_zh_data[id] = zh_data[id]['label']
        else:
            new_zh_data[id] = ''

    DATA.write_to_storage(['zh.json'],new_zh_data)
    return

def storage_core():
    # need to excute after storage_zh

    aspect_dict = DATA.raw_json_reader(r'elements/_aspects.json', 'elements')
    tome_dict = DATA.raw_json_reader(r'elements/tomes.json', 'elements')
    aspecteditems_dict = DATA.raw_json_reader(r'elements/aspecteditems.json', 'elements')
    ability_dirs = [r'elements/abilities.json',r'elements/abilities2.json',r'elements/abilities3.json',r'elements/abilities4.json']
    abilities_dict = DATA.raw_json_reader(ability_dirs, 'elements')
    assistance_dict = DATA.raw_json_reader(r'elements/assistance.json', 'elements')
    skill_dict = DATA.raw_json_reader(r'elements/skills.json', 'elements')

    # recipes
    craft_skill_relate_dirs = [r'recipes/crafting_2_keeper.json',r'recipes/crafting_3_scholar.json',r'recipes/crafting_4b_prentice.json',]
    craft_skill_aspect_relate_dirs = [r'recipes/crafting_1_chandlery.json']
    craft_skill_relate_dict = DATA.raw_json_reader(craft_skill_relate_dirs, 'recipes')

    talk_beast_dict = DATA.raw_json_reader(r'recipes/beasts.json', 'recipes')

    # work station
    bed_dict = DATA.raw_json_reader(r'verbs/workstations_beds.json', 'verbs')
    gathering_dict = DATA.raw_json_reader(r'verbs/workstations_gathering.json', 'verbs')
    library_world_dict = DATA.raw_json_reader(r'verbs/workstations_library_world.json', 'verbs')

    # unstoraged
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
    br.keep_key(memory_dict,             [ 'aspects' ])
    br.keep_key(aspect_dict,             [ 'ishidden' ])
    br.keep_key(tome_dict,               [ 'aspects', 'slots', 'xtriggers' ])
    br.keep_key(abilities_dict,          [ 'aspects', 'xtriggers' ])
    br.keep_key(assistance_dict,         [ 'aspects', 'slots', 'xtriggers', 'inherits' ])
    br.keep_key(aspecteditems_dict,      [ 'aspects', 'xtriggers' ])
    br.keep_key(skill_dict,              [ 'aspects', 'ambits' ])
    br.keep_key(craft_skill_relate_dict, [ 'reqs', 'effects', 'craftable' ])
    br.keep_key(library_world_dict,      [ 'hints', 'slots', 'aspects' ])
    br.keep_key(gathering_dict,          [ 'hints', 'slots' ])

    # add to memory as a source
    add_source(memory_dict, tome_dict)
    add_source(memory_dict, aspecteditems_dict)
    add_source(memory_dict, abilities_dict)
    add_source(memory_dict, assistance_dict)

    add_source_of_recipe(memory_dict,        craft_skill_relate_dict)
    add_source_of_recipe(aspecteditems_dict, craft_skill_relate_dict)

    # assistance inherits -> asstype via prototypes
    for key,value in assistance_dict.items():
        inherit = value.get('inherits')
        if inherit != None:
            asstype = protoptype_dict[inherit]
            value['assistance_type'] = asstype.get('slots')
            value.pop('inherits')
            assistance_dict[key] = value


    # add zh to items
    br.add_zh(aspecteditems_dict)
    br.add_zh(aspect_dict)
    br.add_zh(tome_dict)
    br.add_zh(abilities_dict)
    br.add_zh(memory_dict)
    br.add_zh(assistance_dict)
    br.add_zh(skill_dict)
    br.add_zh(craft_skill_relate_dict)
    br.add_zh(library_world_dict)
    br.add_zh(gathering_dict)

    # write data to storage
    DATA.write_to_storage(['elements','aspecteditems.json'], aspecteditems_dict)
    DATA.write_to_storage(['elements','tome.json'], tome_dict)
    DATA.write_to_storage(['elements','abilities.json'], abilities_dict)
    DATA.write_to_storage(['elements','assistance.json'], assistance_dict)
    DATA.write_to_storage(['elements','memory.json'], memory_dict)
    DATA.write_to_storage(['elements','aspects.json'], aspect_dict)
    DATA.write_to_storage(['elements','skills.json'], skill_dict)
    DATA.write_to_storage(['recipes', 'skill_relate.json'], craft_skill_relate_dict)
    DATA.write_to_storage(['verbs',   'library_world.json'], library_world_dict)
    DATA.write_to_storage(['verbs',   'gathering.json'], gathering_dict)
    return

def Update():
    storage_zh()
    storage_core()

if __name__ == "__main__":
    Update()