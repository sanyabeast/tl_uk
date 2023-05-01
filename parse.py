import argparse
import json
import os
from tools import parse_translation_string, load_json_as_dict, save_dict_as_json, load_json_as_string, load_config, migrate_translation

config = load_config()
existing_mod = load_json_as_dict(os.path.join(os.getcwd(), 'output', 'translation.mod.json'), encoding='utf-8')
print(config)
# print(existing_mod)

# args
parser = argparse.ArgumentParser(
    description='Convert translation file to JSON')
parser.add_argument('-d', '--duplicate', action='store_true',
                    help='Duplicate the original file')
args = parser.parse_args()

# main
original_tl_translation_data = load_json_as_string(os.path.join(
    os.getcwd(), 'input', 'translation.dat'), encoding='utf-16-le')

# parsing original translation format
translation_data = parse_translation_string(original_tl_translation_data)

save_dict_as_json(os.path.join(os.getcwd(), 'output', 'translation.json'), translation_data, encoding='utf-8')

if (existing_mod != None):
    translation_data = migrate_translation(existing_mod, translation_data)
    # print(translation_data)
    
save_dict_as_json(os.path.join(os.getcwd(), 'output', 'translation.mod.json'), translation_data, encoding='utf-8')
