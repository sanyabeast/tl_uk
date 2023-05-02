
import json
import os
from tools import parse_translation_string, generate_tl_translation, convert_dat_to_adm, load_json_as_dict, save_dict_as_json, filter_unique

translation_mod_file = "translation.mod.json"

translation_mod_data = load_json_as_dict(
    os.path.join(os.getcwd(), 'output', translation_mod_file))


# filling dups
dups_filled = 0
for item in translation_mod_data:
    if (len(item['original']) > 0 and item['duplicates'] > 0 and item['new_translation'] != None):
        for test_item in translation_mod_data:
            if (test_item['original'] == item['original']):
                if test_item['new_translation'] == None:
                    test_item['new_translation'] = item['new_translation']
                    dups_filled += 1
                else:
                    if test_item["new_translation"] != item["new_translation"]:
                        print(
                            f'skipping non-empty duplicated, index {item["index"]}, test index {test_item["index"]}, text: {test_item["new_translation"]}')


unique_items = filter_unique(lambda kv: kv['original'], translation_mod_data)

translated_items = list(
    filter(lambda kv: kv['new_translation'] != None, unique_items))
not_translated_items = list(
    filter(lambda kv: kv['new_translation'] == None, unique_items))
items_with_tokens = list(
    filter(lambda kv:  kv['tokens'] != None, unique_items))

items_longer16 = list(filter(lambda kv:  len(
    kv['original']) > 16, not_translated_items))

items_longer32 = list(filter(lambda kv:  len(
    kv['original']) > 32, not_translated_items))

items_longer64 = list(filter(lambda kv:  len(
    kv['original']) > 32, not_translated_items))

items_longer128 = list(filter(lambda kv:  len(
    kv['original']) > 128, not_translated_items))

most_duplicated_items = list(map(lambda kv: f'[{kv["duplicates"]}]: {kv["original"][0:72]}...', sorted(
    not_translated_items, key=lambda kv: kv['duplicates'], reverse=True)))[0:10]

longest_items = list(map(lambda kv: f'[{len(kv["original"])}]: {kv["original"][0:72]}...', sorted(
    not_translated_items, key=lambda kv: len(kv['original']), reverse=True)))[0:10]

translated_percentage = "{:.2f}".format(
    (len(translated_items) / len(unique_items)) * 100)

print(
    f'items translated: {len(translated_items)} / {len(unique_items)} unque ({len(translation_mod_data)} total)')
print(f'{translated_percentage}%')
print('\n')
print(f'dups filled: {dups_filled}')
print('\n')
print('[stats about NON-translated items]')
print(f'items longer than 16 characters: {len(items_longer16)}')
print(f'items longer than 32 characters: {len(items_longer32)}')
print(f'items longer than 64 characters: {len(items_longer64)}')
print(f'items longer than 128 characters: {len(items_longer128)}')
print('\n')
print(f'items with tokens: {len(items_with_tokens)}')
print('\n')
print('most duplicated items:')
print(json.dumps(most_duplicated_items, indent=4))
print('longest items:')
print(json.dumps(longest_items, indent=4))

print('\n')
print(f'saving modified {translation_mod_file} with filled dups')
save_dict_as_json(os.path.join(os.getcwd(), 'output',
                  'translation.mod.json'), translation_mod_data, encoding='utf-8')
