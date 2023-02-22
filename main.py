import json
import pandas as pd
from googletrans import Translator
import time
from tqdm import tqdm
translator = Translator()

def CSV_translator(csv_to_translate, columns, number_of_tries=3, sleep_timer=1):

    """
    CSV translator for files that contains data in languages other that English.
    Saves the result in a json dictionary. 
    TODO: handles for translation on the different languages.
    csv_to_translate: path to a CSV_file that has columns you want to translate
    columns: should be a list or a tuple to iterate on
    number_of_tries: since translator is unstable most probably 
    it will take several times to translate all the data need thus
    you can change the number of tries before failure. Default number is 3.
    sleep_timer: number of seconds between requests. Default is 1 second.
    RETURN: dictionary with unique pairs, where keys are original data and values are translated data
        
    """
    with open(csv_to_translate, mode="r") as csv_file:
        data = pd.read_csv(csv_file, low_memory=False)

    try:
        with open("temp.json", 'r') as f:
            translation_dictionary = json.load(f)
        print("temporary json file found and loaded")
    except (json.decoder.JSONDecodeError, FileNotFoundError) as e:
        # if no file exists, just start with an empty dict
        print(e, type(e))
        print("no temporary json file found. It will be created")
        translation_dictionary = {}
    
    with open(csv_to_translate, mode="r") as csv_file:
        data = pd.read_csv(csv_file, low_memory=False)
    
    for column in columns:
        for row in tqdm(data[column].unique()):
            if row in translation_dictionary:
                continue
            else:
                translation_dictionary[row] = translator.translate(row).text
                time.sleep(sleep_timer)
                with open("temp.json", 'w') as t:
                    temp = json.dump(translation_dictionary, t)

    return translation_dictionary
                