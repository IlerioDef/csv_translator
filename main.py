import json
import os
import pandas as pd
from googletrans import Translator
translator = Translator()

if __name__ == "__main__":
    #TODO: redo temporary path-to-files and translation options
    path_to_file = "data/TG_MarchenkoUPD"
    csv_to_translate = path_to_file + ".csv"
    temporary_json = path_to_file+".json"
    to_translation = ["work", "hopes"]


# check if exists
    if os.path.isfile(temporary_json) == True:
        with open(temporary_json, mode='r') as json_file:
            translation_dictionary = json.load(json_file)
    else:
        translation_dictionary = {}

    with open(csv_to_translate, mode="r") as csv_file:
            data = pd.read_csv(csv_file, low_memory=False)





    for row in to_translation:
        for k, v  in data[row].items():
            if v not in translation_dictionary[row]:
                translation_dictionary[v] = translator.translate(v).text

        for k, v in data[row].items():
            print(v)





