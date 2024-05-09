from Utils import browser as br
import re

from Core.aspect import aspect_dict
from Core.item   import item_dict
from Core.skill  import skill_dict, Skill
from Core.item   import Item
from Core.tome   import Tome
from Core        import BaseItem

from Utils.data_miner import read_from_storage
recipe_dict = read_from_storage(['recipes','recipe.json'])

class Recipe(object):
    def __init__(self, id: str):
        dict_id = recipe_dict.get(id)

        if dict_id is not None:
            self.id = id
            self.zh = dict_id.get('zh','')
            self.skills = self.get_skills(dict_id)
            self.reqs  = self.get_reqs(dict_id)
            self.effect = br.get_first_key({k: v for k,v in dict_id.get('effects',{}).items() if v > 0})
            self.extra_slot = {}

    def get_skills(self, dict_id:dict):
        reqs = dict_id.get('reqs',{})
        skill_re = re.compile(r'^s\.(.*)')
        skill_id = br.get_first_key(br.index_with_re(reqs, skill_re, False))
        if skill_id is not None:
            return {skill_id: 1}
        aspect_re = re.compile(r'^skill\.(.*)')
        aspect_id = br.get_first_key(br.index_with_re(reqs, aspect_re, False))
        if aspect_id is not None:
            return {skill_id: 1 for skill_id in skill_dict if aspect_id in Skill(skill_id).aspects}

    def get_reqs(self, dict_id: dict):
        reqs = dict_id.get('reqs',{})
        tem_reqs = br.index_with_re(reqs, re.compile(r'^(?!s\.)(?!skill\.).*$'), False)
        result = { 'aspects':{}, 'item':{} }
        for key, level in tem_reqs.items():
            if key in aspect_dict:
                result['aspects'][key] = level
            if key in item_dict:
                result['item'][key] = level
        return result

    def isgood(self, item:BaseItem):
        return item.id in self.reqs['item'] or any([ aspect in self.reqs['aspects'] for aspect in item.aspects ])

    def unfilled(self, reqs:dict[str,dict[str,int]]) -> dict:
        aspect_dict = self.reqs.get('aspects',{}).copy()
        item_dict = self.reqs.get('item',{}).copy()
        result = { 'aspects':aspect_dict, 'item': item_dict }
        for type_id in result:
            for aspect in reqs.get(type_id,{}):
                if aspect in result[type_id]:
                    result[type_id][aspect] -= reqs[type_id][aspect]
                    if result[type_id][aspect] <= 0:
                        result[type_id].pop(aspect)
        return result

    def isfull(self, reqs:dict[str,dict[str,int]]) -> bool:
        result = self.unfilled(reqs)
        return not result['aspects'] and not result['item']

def Tome_recipe(tome:Tome)->Recipe:
    recipe = Recipe(tome.id)
    recipe.id = tome.id
    recipe.zh = f'阅读书目：{tome.zh}'
    recipe.skills = {tome.language: 1} if tome.language else {}
    recipe.reqs = { 'aspects':tome.challenge, 'item':{tome.id: 1} }
    recipe.effect = tome.lesson
    recipe.extra_slot = {'language':{'required':{tome.language:1}}} if recipe.skills else None
    return recipe

if __name__ == '__main__':
    a = Recipe("craft.keeper.resurgences.emergences_moth_larva.chimeric_perilousimago")
    # for recipe_id in recipe_dict:
    #     recipe = Recipe(recipe_id)
    #     if recipe.skills == None:
    #         print(recipe.zh,recipe.effect)