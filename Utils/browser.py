def get_key_value(tar_list, tar_key, tar_value):
    result = next((d for d in tar_list if d.get(tar_key) == tar_value), None)
    if(result == None):
        print("{0}: \"{1}\" not found in list!".format(tar_key,tar_value))
    return result

def is_greater_than(a, b):
    if not all(key in a for key in b):
        return False
    return all(a[key] > b[key] for key in b)

def search_by_aspect(tar_list, tar_aspect_dict):
    # all target that has aspect higher than tar_aspect_dict
    result = [d for d in tar_list if is_greater_than(d.get("aspects"), tar_aspect_dict)]
    return result