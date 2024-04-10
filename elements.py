import Utils

aspect_list = Utils.json_reader(r'core/elements/_aspects.json')['elements']
aspected_items_list = Utils.json_reader(r'core/elements/aspecteditems.json')['eements']

# beast, beverage, blank, bust, cache, candle... are separated by "inherits"
memory_list = [ d for d in aspected_items_list if d.get("inherits") == "_memory" ]


tome_list = Utils.json_reader(r'core/elements/tomes.json')['elements']
# add tome to memory as a source
for tome in tome_list:
    xtriggers = tome["xtriggers"]
    mem = next((value for key, value in xtriggers.items() if key.startswith('reading.')),[{'id':None}])[0]['id']
    for memory in memory_list:
        if memory['id'] == mem: # assume it always has id
            if 'source' in memory:
                if 'reading' in memory['source']:
                    memory['source']['reading'].append(tome['id'])
                else:
                    memory['source'] = { "reading": [tome['id']] }
            else:
                memory['source'] = { "reading": [tome['id']] }