import argparse
import json
from tools import parse_translation_string

original_data_file = "TRANSLATION.DAT.bak"

parser = argparse.ArgumentParser(description='Convert translation file to JSON')
parser.add_argument('-d', '--duplicate', action='store_true', help='Duplicate the original file')
args = parser.parse_args()

with open(original_data_file, 'r', encoding='utf-16-le') as f:
    content = f.read()
    translation_data = parse_translation_string(content)

    # Write a JSON file
    with open(f'{original_data_file.replace(".bak", "")}.json', 'w', encoding='utf-8') as outfile:
        json.dump(translation_data, outfile, indent=4, ensure_ascii=False)

    # Duplicate the file if -d option is specified
    if args.duplicate:
        with open(f'{original_data_file.replace(".bak", "")}.json', 'r', encoding='utf-8') as infile:
            with open(f'{original_data_file.replace(".bak", "")}.mod.json', 'w', encoding='utf-8') as outfile:
                outfile.write(infile.read())