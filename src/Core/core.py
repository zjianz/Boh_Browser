from Utils.data_miner import read_from_storage
from Utils import browser as br
import re, itertools

from Core.item    import Item,                item_dict
from Core.aspect  import Aspect,              aspect_dict
from Core.skill   import Skill,               skill_dict
from Core.tome    import Tome,                tome_dict
from Core.station import Station, Slot,       station_dict
from Core.recipe  import Recipe, Tome_recipe, recipe_dict
from Core.ability import Ability,             ability_dict
from Core.condition import Condition as Cd, CompositeCondition

def get_item_list_by_aspect(cond: CompositeCondition, is_print:bool=False, print_source:bool=False, pic_dir:bool=False):
    result = []
    for item_id in item_dict:
        item = Item(item_id)
        aspect_item = item.aspects
        if item.zh == '':
            continue
        if cond.evaluate(aspect_item):
            result.append(item)
            if is_print:
                item.print(print_source, pic_dir)
    return result

def low_q_station_finder(recipe:Recipe, preset_items:dict={}) -> list[Station]:
    """
    preset_items: a dict which contains these keys:
        'skill': a dict of skill_id: skill_level, convering the skill you willing to use
        'item' : a list of item instances, include all items you already decided
    """
    result = []
    skill_preset = preset_items.get('skill',{})
    if recipe.skills and skill_preset:
        skill_preset = br.add_dict(skill_preset,{skill_id: level for skill_id, level in recipe.skills.items() if not skill_id in skill_preset})
    if not skill_preset:
        skill_preset = recipe.skills

    item_preset = preset_items.get('item', [])
    if recipe.reqs['item'] is not None:
        for item_id in recipe.reqs['item']:
            for item in item_preset:
                if item.id == item_id:
                    break
            else:
                if re.match(r'^t\.', item_id):
                    item_preset.append(Tome(item_id))
                else:
                    item_preset.append(Item(item_id))

    # speed up
    special_aspects = ['sound','instrument','tool','liquid','metal','flower','egg','wood']
    candidate_aspect = [aspect for aspect in special_aspects if aspect in recipe.reqs['aspects']]
    candidate_lists = [[Item(item_id) for item_id in item_dict if aspect in Item(item_id).aspects] for aspect in candidate_aspect]
    prev_list = []
    for station_id in station_dict:
        station = Station(station_id)
        for candidate_list in candidate_lists:
            if any([station.fill(candidate) for candidate in candidate_list]):
                station.reset()
            else:
                station.reset()
                break
        else:
            prev_list.append(station_id)

    #loop
    for station_id in prev_list:
        station = Station(station_id)
        if recipe.extra_slot:
            for id, slot_dict in recipe.extra_slot.items():
                station.slots[id] = Slot(slot_dict)
        if skill_preset:
            # need to loop skills
            for skill_id, level in skill_preset.items():
                skill = Skill(skill_id, level)
                if station.fill(skill):
                    # fill in all items
                    if all([ station.fill(item) for item in item_preset ]):
                        result.append(station)
        else:
            if all([ station.fill(item) for item in item_preset ]):
                result.append(station)
    return result

def high_q_station_finder(recipe:Recipe, preset_items:dict={}, is_print:bool=False, print_id:bool=False) -> list[Station]:
    """
    preset_items: a dict which contains these keys:
        'skill': a dict of skill_id: skill_level, convering the skill you willing to use
        'item' : a list of item instances, include all items you already decided
    """
    skill_preset = preset_items.get('skill',{})
    if recipe.skills and skill_preset :
        skill_preset = br.add_dict(skill_preset,{skill_id: level for skill_id, level in recipe.skills.items() if not skill_id in skill_preset})
    if skill_preset == None:
        skill_preset = recipe.skills

    item_preset = preset_items.get('item', [])
    if recipe.reqs['item'] is not None:
        for item_id in recipe.reqs['item']:
            for item in item_preset:
                if item.id == item_id:
                    break
            else:
                if re.match(r'^t\.', item_id):
                    item_preset.append(Tome(item_id))
                else:
                    item_preset.append(Item(item_id))
    preset_items = {'skill':skill_preset, 'item':item_preset}

    station_list = low_q_station_finder(recipe, preset_items)
    result:list[Station]
    result = []
    canditates = [Item(item_id) for item_id in item_dict if recipe.isgood(Item(item_id))] + [Ability(ability_id) for ability_id in ability_dict if recipe.isgood(Ability(ability_id))] + [Skill(skill_id,5) for skill_id in skill_dict if recipe.isgood(Skill(skill_id,5))]
    for station in station_list:
        to_be_filled = [ key for key in station.slots if not station.slots[key].is_filled() ]
        locked = [ key for key in station.slots if station.slots[key].is_filled() ]
        valid_items = [[item for item in canditates if station.slots[key].judge(item) and not item.id in recipe.effect and not Cd('numen').evaluate(item.aspects) ] for key in to_be_filled]
        for combo in itertools.product(*valid_items):
            if all([station.fill(item,locked) for item in combo]) and recipe.isfull(station.total):
                result.append(station)
                break
            else:
                station.reset(to_be_filled)
    if is_print:
        recipe_text = recipe.zh
        if skill_preset:
            recipe_text += f'({"+".join(Skill(skill_id,level).zh for skill_id,level in skill_preset.items())})'
        if item_preset:
            recipe_text += f'({"+".join([f"{item.zh}" for item in item_preset])})'
        print(recipe_text)
        print('可用工作站及示例配方：')
        for station in result:
            station.print(print_id)
    return result




if __name__ == '__main__':
    print("ite = get_item_list_by_aspect(Cd('memory')&~Cd('numen'),1,1)")
    recipe = Recipe('craft.keeper.inks.containment_winter_liquid.solomon_nillycant')
    print("result = high_q_station_finder(recipe,{},1,1)")