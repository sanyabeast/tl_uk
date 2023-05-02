
import json
import os
from tools import parse_translation_string, generate_tl_translation, convert_dat_to_adm, load_json_as_dict, save_dict_as_json
import requests
import subprocess
import signal
import sys
import time
import asyncio

from pyppeteer import launch
# from googletrans import Translator
# translator = Translator()

# Define a flag to control the while loop
running = True

translation_mod_file = "translation.mod.json"
translation_mod_data = load_json_as_dict(
    os.path.join(os.getcwd(), 'output', translation_mod_file))


async def translate_ru_to_uk(text):
    generic_chrome_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    
    browser = await launch({
        "headless": False,
        "args": ['--no-sandbox']
    })
    page = await browser.newPage()
    await page.setUserAgent(generic_chrome_user_agent)

    await page.evaluateOnNewDocument(pageFunction='''
    () => {
        Object.defineProperty(navigator, 'webdriver', {
            get: () => false,
        });
    }
    ''');
    await page.evaluateOnNewDocument('''
    () => {
        // We can mock this in as much depth as we need for the test.
        window.navigator.chrome = {
            runtime: {},
            // etc.
        };
    }
    ''')
    
    url = "https://translate.google.com/?sl=ru&tl=uk&op=translate"
    await page.goto(url)
    
    # Wait for the input textarea to be available
    input_selector = "#source"
    await page.waitForSelector(input_selector)
    
    # Enter the text to translate
    await page.type(input_selector, text)
    
    # Wait for the translation result
    result_selector = ".result.tlid-copy-target > span"
    await page.waitForSelector(result_selector)
    
    # Get the translated text
    translated_text = await page.evaluate('(selector) => document.querySelector(selector).textContent', result_selector)
    
    await browser.close()
    
    return translated_text



def signal_handler(sig, frame):
    global running
    print('You pressed Ctrl+C!')
    # Here you can add any cleanup code
    running = False


def translate_text(text):
    url = 'http://localhost:1338/translate'
    headers = {'Content-Type': 'application/json; charset=UTF-8'}
    data = {
        'from_language': 'ru',
        'to_language': 'uk',
        'text': text
    }

    response = requests.post(url, headers=headers, data=json.dumps(
        data, ensure_ascii=False).encode('utf8'))
    return response.json()['translation']


time.sleep(3)

# Example usage
async def main():
    text = "Привет, мир!"
    translated_text = await translate_ru_to_uk("Призванный отряд из 3 неподвижных лучников-скелетов атакует противника. Щелкните правой кнопкой мыши, чтобы изучить заклинание.")
    print(translated_text)

    # Main loop
    while running:
        print("Daemon is running...")
        time.sleep(1)  # Sleep for a while to simulate work

    print("Exiting...")
    # Here you can add any cleanup code

    sys.exit(0)

    

# This line should be at the top level of your script, not inside a function
asyncio.run(main())