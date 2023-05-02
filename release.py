
import json
import os
from tools import parse_translation_string, generate_tl_translation, convert_dat_to_adm, load_json_as_dict, save_dict_as_json

target_dat_file = "TRANSLATION.DAT"
translation_mod_file = "translation.mod.json"

translation_mod_data = load_json_as_dict(os.path.join(os.getcwd(), 'output', translation_mod_file))
translation_mod_data = sorted(translation_mod_data, key=lambda kv: kv['index'])

for item in translation_mod_data:
    if item['new_translation'] != None:
        item['new_translation'] = item['new_translation'].replace(
            '\n', '\\n')
    elif item['translation'] != None:
        item['translation'] = item['translation'].replace('\n', '\\n')

tl_translation = generate_tl_translation(translation_mod_data)

with open(os.path.join(os.getcwd(), 'output', target_dat_file), "w", encoding="utf-16") as f:
    f.write(tl_translation)
    convert_dat_to_adm()
    
