from . import data_miner as DATA, browser as br
from . import *
import os,re

# convert raw data to storage

def apply_indexed(tar):
    """
    convert [ {'id': 'idx', ...} ... ]
    into    { 'idx': {...}, ... }
    for every level
    """
    if isinstance(tar, list):
        if len(tar) > 0 and isinstance(tar[0], dict) and 'id' in tar[0]:
            # need modify
            result = {}
            for item in tar:
                id_item = item.pop('id')
                new_item = apply_indexed(item)
                result[id_item] = new_item
        else:
            result = []
            for item in tar:
                result.append(apply_indexed(item))
        return result
    if isinstance(tar, dict):
        result = {}
        for key in tar:
            result[key] = apply_indexed(tar[key])
        return result
    return tar


def add_source_of_xtrigger(opt_dict:dict, source_dict:dict):
    for key, value in source_dict.items():
        trig = value.get('xtriggers')
        if trig is not None:
            for trig_type, trig_result in trig.items():
                    result_ids = [id_res for id_res in trig_result if trig_result[id_res].get('morpheffect') == 'spawn'] if isinstance(trig_result, dict) else [trig_result]
                    trig_type = re.sub('^([^.]*)(?:\..*)?$', r'\1', trig_type)
                    for result_id in result_ids:
                        if result_id in opt_dict:
                            opt_item = opt_dict[result_id]
                            if not 'source' in opt_item:
                                opt_item['source'] = {}
                            if trig_type in opt_item['source']:
                                opt_item['source'][trig_type].append(key)
                            else:
                                opt_item['source'][trig_type] = [key]

def add_source_of_recipe(opt_dict:dict, recipe_dict:dict):
    for key, value in recipe_dict.items():
        effects = value.get('effects')
        if effects is not None:
            for effect in effects.keys():
                if effects[effect] < 0:
                    continue
                if effect in opt_dict:
                    opt_item = opt_dict[effect]
                    if not 'source' in opt_item:
                        opt_item['source'] = {}
                    if 'recipe' in opt_item['source']:
                        opt_item['source']['recipe'].append(key)
                    else:
                        opt_item['source']['recipe'] = [key]

def add_source_of_deck(opt_dict:dict, deck_dict:dict):
    for key, value in deck_dict.items():
        spec_list = value.get('spec')
        if spec_list is not None:
            for spec in spec_list:
                if spec in opt_dict:
                    opt_item = opt_dict[spec]
                    if not 'source' in opt_item:
                        opt_item['source'] = {}
                    if 'deck' in opt_item['source']:
                        if not key in opt_item['source']['deck']:
                            opt_item['source']['deck'].append(key)
                    else:
                        opt_item['source']['deck'] = [key]

def add_source_of_mastering(skill_dict:dict, tome_dict:dict):
    for key, value in tome_dict.items():
        master_re = re.compile(r'^mastering\.(.*)$')
        lesson_re  = re.compile(r'^x\.(.*)$')
        lesson_dict = br.index_with_re(
                    br.get_first_value(br.index_with_re(value['xtriggers'], master_re)),
                    lesson_re, True, r's.\1'
                )
        skill_id = br.get_first_key(lesson_dict)
        if skill_id in skill_dict:
            if not 'source' in skill_dict[skill_id]:
                skill_dict[skill_id]['source'] = []
            skill_dict[skill_id]['source'].append(key)

def add_recipe(skill_dict:dict, recipe_dict:dict):
    for key, value in recipe_dict.items():
        skill_re = re.compile(r'^s\.(.*)')
        skill_item = br.index_with_re(value.get('reqs',{}), skill_re, False)
        if skill_item != {}:
            skill_id = br.get_first_key(skill_item)
            effects = br.get_first_key({k: v for k,v in value['effects'].items() if v > 0})
            if skill_id in skill_dict:
                if not 'recipes' in skill_dict[skill_id]:
                    skill_dict[skill_id]['recipes'] = {}
                skill_dict[skill_id]['recipes'][key] = effects
        aspect_re = re.compile(r'^skill\.(.*)')
        aspect_item = br.index_with_re(value.get('reqs',{}), aspect_re, False)
        if aspect_item != {}:
            aspect_id = br.get_first_key(aspect_item)
            effects = br.get_first_key({k: v for k,v in value['effects'].items() if v > 0})
            for skill_id in skill_dict:
                if aspect_id in skill_dict[skill_id]['aspects']:
                    if not 'recipes' in skill_dict[skill_id]:
                        skill_dict[skill_id]['recipes'] = {}
                    skill_dict[skill_id]['recipes'][key] = effects

def apply_prototypes(prototype_dict: dict, tar_dict: dict) -> dict:
    result = tar_dict.copy()
    for key, value in tar_dict.items():
        inherit = value.get('inherits')
        if inherit == None:
            continue
        result[key].pop('inherits')
        inherit_dict = prototype_dict.get(inherit)
        if inherit_dict == None:
            continue
        inherit_dict = br.index_with_re(inherit_dict, re.compile(r'aspects|xtriggers|slots'), False)
        result[key] = br.add_dict(result[key], inherit_dict)
    return result

def storage_zh():
    zh_files = []
    for root, dirs, files in os.walk(DATA.zh_dir):
            for file in files:
                if file.endswith('.json'):
                    file_path = os.path.join(root, file)
                    zh_files.append(file_path)
    zh_data = apply_indexed(DATA.raw_json_reader(zh_files))

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

    aspect_dir = [ r'elements/_aspects.json', r'elements/_evolutionaspects.json' ]
    aspect_dict = apply_indexed(DATA.raw_json_reader(aspect_dir, 'elements'))
    tome_dict = apply_indexed(DATA.raw_json_reader(r'elements/tomes.json', 'elements'))
    aspecteditems_dir = [ r'elements/aspecteditems.json', r'elements/incidents_weather.json' ]
    aspecteditems_dict = apply_indexed(DATA.raw_json_reader(aspecteditems_dir, 'elements'))
    ability_dirs = [r'elements/abilities.json',r'elements/abilities2.json',r'elements/abilities3.json',r'elements/abilities4.json']
    abilities_dict = apply_indexed(DATA.raw_json_reader(ability_dirs, 'elements'))
    assistance_dict = apply_indexed(DATA.raw_json_reader(r'elements/assistance.json', 'elements'))
    skill_dict = apply_indexed(DATA.raw_json_reader(r'elements/skills.json', 'elements'))

    # recipes
    recipe_dirs = [r'recipes/crafting_2_keeper.json',
                   r'recipes/crafting_3_scholar.json',
                   r'recipes/crafting_4b_prentice.json',
                   r'recipes/crafting_1_chandlery.json',
                   r'recipes/crafting_1_simplemanipulations.json',
                   r'recipes/gathering_2_seasonal.json'
                   ]
    recipe_dict = apply_indexed(DATA.raw_json_reader(recipe_dirs, 'recipes'))

    talk_beast_dict = apply_indexed(DATA.raw_json_reader(r'recipes/beasts.json', 'recipes'))

    # work station
    bed_dict = apply_indexed(DATA.raw_json_reader(r'verbs/workstations_beds.json', 'verbs'))
    gathering_dict = apply_indexed(DATA.raw_json_reader(r'verbs/workstations_gathering.json', 'verbs'))
    library_world_dict = apply_indexed(DATA.raw_json_reader(r'verbs/workstations_library_world.json', 'verbs'))

    # unstoraged
    prototype_dict = apply_indexed(DATA.raw_json_reader(r'elements/_prototypes.json', 'elements'))
    deck_dir = [ r'decks/catalogue_decks.json', r'decks/challenges.json', r'decks/chats.json', r'decks/gathering_decks.json', r'decks/incidents_decks.json' ]
    deck_dict = apply_indexed(DATA.raw_json_reader(deck_dir, 'decks'))


    # keep id, unique, aspects
    br.keep_key(aspect_dict,             [ 'inherits', 'ishidden' ])
    br.keep_key(tome_dict,               [ 'inherits', 'aspects', 'slots', 'xtriggers' ])
    br.keep_key(abilities_dict,          [ 'inherits', 'aspects', 'xtriggers' ])
    br.keep_key(assistance_dict,         [ 'inherits', 'aspects', 'slots', 'xtriggers' ])
    br.keep_key(aspecteditems_dict,      [ 'inherits', 'aspects', 'xtriggers' ])
    br.keep_key(skill_dict,              [ 'inherits', 'aspects', 'ambits' ])
    br.keep_key(recipe_dict,             [ 'inherits', 'reqs', 'effects', 'craftable', 'actionid', 'deckeffects' ])
    br.keep_key(library_world_dict,      [ 'inherits', 'hints', 'slots', 'aspects' ])
    br.keep_key(gathering_dict,          [ 'inherits', 'hints', 'slots' ])
    br.keep_key(prototype_dict,          [ 'inherits', 'aspects', 'slots', 'xtriggers' ])

    prototype_dict     = apply_prototypes(prototype_dict, prototype_dict)
    aspecteditems_dict = apply_prototypes(prototype_dict, aspecteditems_dict)
    tome_dict          = apply_prototypes(prototype_dict, tome_dict)
    abilities_dict     = apply_prototypes(prototype_dict, abilities_dict)
    recipe_dict        = apply_prototypes(prototype_dict, recipe_dict)

    # add source
    for keys in aspecteditems_dict:
        aspecteditems_dict[keys]['source'] = {}
    add_source_of_xtrigger(aspecteditems_dict, tome_dict)
    add_source_of_xtrigger(aspecteditems_dict, aspecteditems_dict)
    add_source_of_xtrigger(aspecteditems_dict, abilities_dict)
    add_source_of_xtrigger(aspecteditems_dict, assistance_dict)

    add_source_of_recipe(aspecteditems_dict, recipe_dict)

    add_source_of_deck(aspecteditems_dict,deck_dict)

    add_source_of_mastering(skill_dict, tome_dict)
    add_recipe(skill_dict, recipe_dict)

    # assistance inherits -> asstype via prototypes
    for key,value in assistance_dict.items():
        inherit = value.get('inherits')
        if inherit is not None:
            asstype = prototype_dict[inherit]
            value['assistance_type'] = asstype.get('slots')
            value.pop('inherits')
            assistance_dict[key] = value


    # add zh to items
    br.add_zh(aspecteditems_dict)
    br.add_zh(aspect_dict)
    br.add_zh(tome_dict)
    br.add_zh(abilities_dict)
    br.add_zh(assistance_dict)
    br.add_zh(skill_dict)
    br.add_zh(recipe_dict)
    br.add_zh(library_world_dict)
    br.add_zh(gathering_dict)

    # write data to storage
    DATA.write_to_storage(['elements','aspecteditems.json'], aspecteditems_dict)
    DATA.write_to_storage(['elements','tome.json'], tome_dict)
    DATA.write_to_storage(['elements','abilities.json'], abilities_dict)
    DATA.write_to_storage(['elements','assistance.json'], assistance_dict)
    DATA.write_to_storage(['elements','aspects.json'], aspect_dict)
    DATA.write_to_storage(['elements','skills.json'], skill_dict)
    DATA.write_to_storage(['recipes', 'recipe.json'], recipe_dict)
    DATA.write_to_storage(['verbs',   'library_world.json'], library_world_dict)
    DATA.write_to_storage(['verbs',   'gathering.json'], gathering_dict)
    DATA.write_to_storage(['unused',  'decks.json'], deck_dict)
    DATA.write_to_storage(['unused',  'prototype.json'], prototype_dict)
    return

def Update():
    storage_zh()
    storage_core()

if __name__ == "__main__":
    Update()