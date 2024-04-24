from Utils import browser as br
import re

from Core.aspect import aspect_dict
from Core.item   import item_dict

from Utils.data_miner import read_from_storage
recipe_dict = read_from_storage(['recipes','recipe.json'])

class Recipe(object):
    def __init__(self, id: str):
        dict_id = recipe_dict.get(id)

        if dict_id is not None:
            self.id = id
            self.zh = dict_id['zh']
            self.skill = self.get_skill(dict_id)
            self.reqs  = self.get_reqs(dict_id)
            self.effect = br.get_first_key({k: v for k,v in dict_id['effects'].items() if v > 0})

    def get_skill(self, dict_id:dict):
        reqs = dict_id['reqs']
        skill_re = re.compile(r'^(s|skill)\.(.*)')
        skill_id = br.get_first_key(br.index_with_re(reqs, skill_re, False))
        return skill_id

    def get_reqs(self, dict_id: dict):
        reqs = dict_id['reqs']
        tem_reqs = br.index_with_re(reqs, re.compile(r'^(?!s\.)(?!ability)(?!skill\.).*$'), False)
        result = { 'aspects':{}, 'item':{} }
        for key, level in tem_reqs.items():
            if key in aspect_dict:
                result['aspects'][key] = level
            if key in item_dict:
                result['item'][key] = level
        return result


if __name__ == '__main__':
    a = Recipe("craft.keeper.resurgences.emergences_moth_larva.chimeric_perilousimago")