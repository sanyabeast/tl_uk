import re
import json
import subprocess
import os

tokens_stats = []
unique_texts = 0
long_texts = 0

long_text_length = 64


def load_config():
    return load_json_as_dict(os.path.join(os.getcwd(), 'config.json'))


def convert_dat_to_adm():
    subprocess.run(["./lib/tldat.exe", "./output/TRANSLATION.DAT"])


def find(test, my_list):
    return next(filter(test, my_list), None)


def save_dict_as_json(path, dictionary, encoding='utf-8'):
    with open(path, 'w', encoding=encoding) as f:
        json.dump(dictionary, f, indent=4, ensure_ascii=False)


def load_json_as_dict(path, encoding='utf-8'):
    if not os.path.exists(path):
        return None
    try:
        with open(path, 'r', encoding=encoding) as f:
            return json.load(f)
    except json.JSONDecodeError:
        return None


def load_json_as_string(path, encoding='utf-8'):
    if not os.path.exists(path):
        return None
    try:
        with open(path, 'r', encoding=encoding) as f:
            return f.read()
    except Exception as e:
        # print(e)
        return None


def parse_translation_string(s):
    global tokens_stats
    global unique_texts
    global long_texts

    translations = []
    pattern = r'<STRING>FILE:(.*?)\n<STRING>PROPERTY:(.*?)\n<STRING>ORIGINAL:(.*?)\n<STRING>TRANSLATION:(.*?)\n'
    matches = re.findall(pattern, s, re.DOTALL)
    match_index = 0

    for match in matches:
        file, property, original, translation = match
        tokens = parse_tokens(original)

        translations.append({'index': match_index, 'file': file, 'property': property.strip(
        ), 'original': original.strip(), 'translation': translation.strip(), 'new_translation': None, 'tokens': tokens if tokens['total'] > 0 else None})

        if (len(original)) > long_text_length:
            long_texts += 1

        match_index += 1

    for item in translations:
        duplicates_count = len(
            list(filter(lambda kv: kv['index'] != item['index'] and kv['original'] == item['original'], translations)))
        item['duplicates'] = duplicates_count
        if (duplicates_count == 0):
            unique_texts += 1

    print(f'Torchlight translation parsed\n')
    print(f'total texts: {len(translations)}')
    print(f'long texts (>{long_text_length}): {long_texts}')
    print(f'unique texts: {unique_texts}')
    print('\n')
    print(f'tokens stats: ')

    tokens_stats = sorted(
        tokens_stats, key=lambda kv: kv['count'], reverse=True)
    for item in tokens_stats:
        print(f'{item["id"]}: {item["count"]}')

    translations = sorted(translations, key=lambda kv: len(
        kv['original']), reverse=True)
    return translations


# def parse_tokens(s):
#     global tokens_stats
#     tokens = []
#     pattern = r'\[([^\]]+)\]|\|c([0-9A-F]{8})([^\|]+)\|u'
#     matches = re.findall(pattern, s)
#     variables = 0
#     colored_prints = 0
#     for match in matches:
#         token_id = None
#         if match[0]:
#             tokens.append({'type': 'variable', 'value': match[0]})
#             variables += 1
#             token_id = f'VAR:{match[0]}'
#         elif match[1] and match[2]:
#             tokens.append({'type': 'colored_print',
#                           'value': match[2], 'color': match[1]})
#             colored_prints += 1
#             token_id = f'COLOR:{match[1]}'

#         if (token_id != None):
#             token_data = find(lambda kv: kv['id'] == token_id, tokens_stats)
#             if (token_data == None):
#                 tokens_stats.append({
#                     "id": token_id,
#                     "count": 1
#                 })
#             else:
#                 token_data['count'] += 1

#     return {
#         "tokens": tokens,
#         "variables": variables,
#         "colored_prints": colored_prints,
#         "total": variables + colored_prints
#     }

def parse_tokens(s):
    global tokens_stats
    tokens = []
    pattern = r'\[([^\]]+)\]|\<(LOOKAT=[^\>]+)\>|\|c([0-9A-F]{8})([^\|]+)\|u'
    matches = re.findall(pattern, s)
    variables = 0
    colored_prints = 0
    directives = 0
    for match in matches:
        token_id = None
        if match[0]:
            tokens.append({'type': 'variable', 'value': match[0]})
            variables += 1
            token_id = f'VAR:{match[0]}'
        elif match[1]:
            tokens.append({'type': 'directive', 'value': match[1]})
            directives += 1
            token_id = f'DIR:{match[1]}'
        elif match[2] and match[3]:
            inner_matches = re.findall(pattern, match[3])
            if inner_matches:
                for inner_match in inner_matches:
                    if inner_match[0]:
                        tokens.append(
                            {'type': 'colored_variable', 'value': inner_match[0], 'color': match[2]})
                        variables += 1
                        token_id = f'CVAR:{inner_match[0]}'
            else:
                tokens.append({'type': 'colored_print',
                              'value': match[3], 'color': match[2]})
                colored_prints += 1
                token_id = f'COLOR:{match[2]}'

        if (token_id != None):
            token_data = find(lambda kv: kv['id'] == token_id, tokens_stats)
            if (token_data == None):
                tokens_stats.append({
                    "id": token_id,
                    "count": 1
                })
            else:
                token_data['count'] += 1

    return {
        "tokens": tokens,
        "variables": variables,
        "colored_prints": colored_prints,
        "directives": directives,
        "total": variables + colored_prints + directives
    }


def generate_tl_translation(d):
    result = "[TRANSLATIONS]\n"
    for item in d:
        result += "[TRANSLATION]\n"
        result += "<STRING>FILE:" + item["file"] + "\n"
        result += "<STRING>PROPERTY:" + item["property"] + "\n"
        result += "<STRING>ORIGINAL:" + item["original"] + "\n"
        translation = item["new_translation"] if item["new_translation"] != None else item["original"]
        result += "<STRING>TRANSLATION:" + translation + "\n"
        result += "[/TRANSLATION]\n"
    result += "[/TRANSLATIONS]\n"
    return result


def migrate_translation(source, target):
    migrated_items = 0
    for item in target:
        existing_item = find(lambda kv: (
            kv['index'] == item['index'] and kv['new_translation'] != item['new_translation']), source)
        if (existing_item != None):
            item['new_translation'] = existing_item['new_translation']
            migrated_items += 1

    print(f'\nitems migrated - {migrated_items}')
    return target


def filter_unique(predicate, iterable):
    seen = set()
    result = []
    for item in iterable:
        key = predicate(item)
        if key not in seen:
            seen.add(key)
            result.append(item)
    return result


def count_occurrences(string, substring):
    count = 0
    start = 0
    while True:
        index = string.find(substring, start)
        if index == -1:
            break
        count += 1
        start = index + 1
    return count


def check_same_occurrences(a, b, c):
    count_a = count_occurrences(a, c)
    count_b = count_occurrences(b, c)
    return count_a == count_b


def validate_item(item):
    translated = item['new_translation']
    new_lines_check = True
    colored_print_check = True
    variables_count_check = True
    directives_check = True
    colored_variables_check = True

    if translated != None:
        index = item['index']
        english = item['original']
        token_data = item['tokens']
        alias = f"[ {index}: {english[0:32]} ]"

        new_lines_check = check_same_occurrences(
            english, translated, '\\n')

        if isinstance(token_data, dict):
            tokens = token_data['tokens']

            if (tokens != None):
                for token in tokens:
                    if token['type'] == 'colored_print':
                        colored_print_check = check_same_occurrences(
                            english, translated, f"|c{token['color']}") and check_same_occurrences(
                            english, translated, f"|u")
                    if token['type'] == 'directive':
                        directives_check = check_same_occurrences(
                            english, translated, f"<{token['value']}>")
                    if (token['type'] == 'variable'):
                        variables_count_check = check_same_occurrences(
                            english, translated, f"[{token['value']}]")
                    if (token['type'] == 'colored_variable'):
                        variables_count_check = check_same_occurrences(
                            english, translated, f"|c{token['color']}[{token['value']}]|u")

        if not new_lines_check:
            print(f'Error! Incorrect state of line breaks at "{alias}"')
        if not colored_print_check:
            print(f'Error! Incorrect state of colored prints at "{alias}"')
        if not variables_count_check:
            print(f'Error! Incorrect state of variables at "{alias}"')
        if not colored_variables_check:
            print(f'Error! Incorrect state of colored variables at "{alias}"')
        if not directives_check:
            print(f'Error! Incorrect state of directives at "{alias}"')

    return new_lines_check and colored_variables_check and colored_print_check and variables_count_check and directives_check
