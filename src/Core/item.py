from . import BaseItem, get_zh_with_class
from Utils import browser as br
import re

from Utils.data_miner import read_from_storage
item_dict = read_from_storage(['elements','aspecteditems.json'])

class Item(BaseItem):
    def __init__(self, id: str):
        dict_id = item_dict.get(id)
        super().__init__(id, dict_id)

        if dict_id is not None:
            self.source = dict_id.get('source')
            self.aspects = br.index_with_re(dict_id['aspects'], re.compile(r'(?!boost).*$'), False)

    def print(self, print_source:bool = True):

        from Core.aspect import Aspect
        from Core.tome import Tome
        from Core.skill import Skill
        from Core.recipe import Recipe

        aspect_text = '+'.join([ f'{value}'+Aspect(aspect_id).zh for aspect_id, value in self.aspects.items() if Aspect(aspect_id).zh != '' ])
        print(self.zh + f'({aspect_text}): ' + self.id)

        # print source
        if print_source:
            for type, source_list in self.source.items():
                match type:
                    case 'reading':
                        print('\t读书')
                        for source in source_list:
                            print('\t\t' + Tome(source).zh + f' ({Tome(source).id})')
                    case 'recipe':
                        print('\t合成')
                        for source in source_list:
                            recipe_id = Recipe(source)
                            skill_id = recipe_id.skill
                            req_text = ' + '.join([ f'{level}{Aspect(key).zh}' for key,level in recipe_id.reqs['aspects'].items() ] + [ f'{level}{Item(key).zh}' for key,level in recipe_id.reqs['item'].items() ])
                            print('\t\t' + get_zh_with_class(skill_id, [Skill, Aspect]) + ' + ' + req_text)
                    case 'scrutiny':
                        print('\t检查')
                        count = 0
                        for source in source_list:
                            if Item(source).zh == '' or count > 5:
                                continue
                            count += 1
                            if count > 5:
                                print('\t\t...')
                            else:
                                print('\t\t' + Item(source).zh)
                    case 'deck':
                        print('\t卡池')
                        for source in source_list:
                            print('\t\t' + source)

if __name__ == '__main__':
    a = Item("numen.thre")