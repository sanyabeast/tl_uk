
import json
import os
from tools import parse_translation_string, generate_tl_translation, convert_dat_to_adm, load_json_as_dict, save_dict_as_json
import requests

translation_mod_file = "translation.mod.json"
translation_mod_data = load_json_as_dict(os.path.join(os.getcwd(), 'output', translation_mod_file))


def translate_text(text):
    url = 'http://localhost:1338/translate'
    headers = {'Content-Type': 'application/json; charset=UTF-8'}
    data = {
    'from_language': 'ru',
    'to_language': 'uk',
    'text': text
    }

    response = requests.post(url, headers=headers, data=json.dumps(data, ensure_ascii=False).encode('utf8'))
    return response.json()['translation']


print(translate_text("Заставляет противников в радиусе 6 метров замолчать, не давая им использовать большую часть навыков.\\n\\nЩелкните правой кнопкой мыши, чтобы изучить заклинание."))