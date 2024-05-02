from . import BaseItem
from Utils import browser as br
import re

from Utils.data_miner import read_from_storage
skill_dict = read_from_storage(['elements','skills.json'])

class Skill(BaseItem):
    def __init__(self, id: str, level=1):
        dict_id = skill_dict.get(id)
        super().__init__(id, dict_id)

        if dict_id is not None:
            self.level = level
            self.aspects = self.get_aspect(dict_id, level)
            self.wisdom  = self.get_wisdom(dict_id)
            self.sources = dict_id.get('source',{})
            self.recipes = dict_id.get('recipes',{})
            self.zh = self.zh + f'(lv:{level})'

    def get_aspect(self, dict_id, level):
        result = br.index_with_re(dict_id['aspects'], re.compile(r'(?!w\.).*'),False)
        for aspect in result:
            if aspect in ['edge', 'forge', 'grail', 'heart', 'knock', 'lantern', 'moon', 'moth', 'nectar', 'rose', 'scale', 'sky', 'winter']:
                result[aspect] += level - 1
        return result

    def get_wisdom(self, dict_id):
        result = br.index_with_re(dict_id['aspects'], re.compile(r'^w\..*'),False)
        return result

    def print(self, print_recipe:bool = False, print_tome:bool = False):
        from Core.aspect import Aspect
        aspect_text = '+'.join([ f'{level}{Aspect(id).zh}' for id,level in self.aspects.items() if Aspect(id).zh != '' ])
        print(self.zh + f'({aspect_text})')
        if print_recipe:
            from Core.recipe import Recipe
            from Core.item   import Item
            from Core.aspect import Aspect
            print('\t合成')
            for recipe_id in self.recipes:
                recipe = Recipe(recipe_id)
                reqs = recipe.reqs
                effect = Item(recipe.effect)
                req_text = ' '.join([f'{level}{Aspect(aspect).zh}' for aspect,level in reqs['aspects'].items()] + [f'{Item(item).zh}' for item in reqs['item']])
                print('\t\t' + f'{req_text:<15} =>' + f'{effect.zh}({effect.id})')
        if print_tome:
            from Core.tome import Tome
            print('\t来源')
            for tome_id in self.sources:
                tome = Tome(tome_id)
                print('\t\t' + tome.zh)

if __name__ == '__main__':
    a = Skill("s.transformations.liberations",5)