
import json
from tools import parse_translation_string, generate_tl_translation

target_dat_file = "TRANSLATION.DAT"
translation_mod_file = "TRANSLATION.DAT.mod.json"

with open(translation_mod_file, 'r', encoding='utf-8') as f:
    content = json.loads(f.read())
    content = sorted(content, key=lambda kv: kv['index'])

    for item in content:
        if item['new_translation'] != None:
            item['new_translation'] = item['new_translation'].replace(
                '\n', '\\n')
        elif item['translation'] != None:
            item['translation'] = item['translation'].replace('\n', '\\n')

    tl_translation = generate_tl_translation(content)

    with open(target_dat_file, "w", encoding="utf-16") as f:
        f.write(tl_translation)
