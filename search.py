import sys
import json
import os
from tools import parse_translation_string, generate_tl_translation, convert_dat_to_adm, load_json_as_dict, save_dict_as_json, filter_unique


translation_mod_file = "translation.mod.json"

translation_mod_data = load_json_as_dict(
    os.path.join(os.getcwd(), 'output', translation_mod_file))

unique_items = filter_unique(lambda kv: kv['original'], translation_mod_data)

# Check if both arguments are provided
if len(sys.argv) != 3:
    print("Please provide two string arguments.")
else:
    # Retrieve the two string arguments
    type = sys.argv[1]
    query = sys.argv[2]

    found_items = []
    found_texts = []

    # Print the arguments
    print("Search type:", type)
    print("Search query:", query)

    print(f"Unique items to search in: {len(unique_items)}")
    
    query = query.lower()

    if type == 'o':
        print("Searchin in original texts...")
        found_items = list(
            filter(lambda kv: query in kv["original"].lower(), unique_items))
        found_texts = list(map(lambda kv: kv["original"], found_items))
    if type == 't':
        print("Searchin in old translations...")
        found_items = list(
            filter(lambda kv: query in kv["translation"].lower(), unique_items))
        found_texts = list(map(lambda kv: kv["translation"], found_items))
    if type == 'nt':
        print("Searchin in new translations...")
        found_items = list(filter(
            lambda kv: kv["new_translation"] != None and (query in kv["new_translation"].lower()), unique_items))
        found_texts = list(map(lambda kv: kv["new_translation"], found_items))

    print(f"total items found: {len(found_texts)}")
    index = 0
    for item in found_texts:
        print(f"[{index}] {item}\n")
        index += 1
