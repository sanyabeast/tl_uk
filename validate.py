
import json
import os
from tools import parse_translation_string, generate_tl_translation, convert_dat_to_adm, load_json_as_dict, save_dict_as_json, filter_unique, validate_item

translation_mod_file = "translation.mod.json"

translation_mod_data = load_json_as_dict(
    os.path.join(os.getcwd(), 'output', translation_mod_file))


unique_items = filter_unique(lambda kv: kv['original'], translation_mod_data)

all_good = True

for item in unique_items:
    all_good = all_good and validate_item(item)

if all_good:
    print("Success! All good!")
