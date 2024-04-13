from Utils import data_miner as DATA
from Utils import browser as br
from Utils import zh

# aspect_list = DATA.raw_json_reader(r'elements/_aspects.json')['elements']
# aspected_items_list = DATA.raw_json_reader(r'elements/aspecteditems.json')['elements']

# # beast, beverage, blank, bust, cache, candle... are separated by "inherits"
# memory_list = [ d for d in aspected_items_list if d.get("inherits") == "_memory" ]


# tome_list = DATA.raw_json_reader(r'elements/tomes.json')['elements']
# # add tome to memory as a source
# for tome in tome_list:
#     xtriggers = tome["xtriggers"]
#     mem = next((value for key, value in xtriggers.items() if key.startswith('reading.')),[{'id':None}])[0]['id']
#     for memory in memory_list:
#         if memory['id'] == mem: # assume it always has id
#             if 'source' in memory:
#                 if 'reading' in memory['source']:
#                     memory['source']['reading'].append(tome['id'])
#                 else:
#                     memory['source'] = { "reading": [tome['id']] }
#             else:
#                 memory['source'] = { "reading": [tome['id']] }
# DATA.write_to_storage(['elements','memory.json'],memory_list)

class core:
    def __init__(self, dist={}):
        self.id = br.get_value_of_key(dist,'id')
    