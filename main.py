import json
import pandas as pd
from googletrans import Translator
translator = Translator()

if __name__ == "__main__":

    # TODO: redo temporary path-to-files and translation options
    path_to_file = "data/TG_MarchenkoUPD"
    csv_to_translate = path_to_file + ".csv"
    temporary_json = path_to_file + ".json"
    # to_translation = ["work", "hopes"]

    # # check if exists
    # if os.path.isfile(temporary_json):
    #     # with open(temporary_json, mode='w') as json_file:
    #     #     translation_dictionary = json.load(json_file)
    #     print("Temporary file detected and will be loaded")
    # else:
    #     translation_dictionary = {}
    #     print("No temporary file detected. It will be created and saved")

    with open(csv_to_translate, mode="r") as csv_file:
        data = pd.read_csv(csv_file, low_memory=False)

    try:
        with open(temporary_json, 'r') as f:
            translation_dictionary = json.load(f)
    except json.decoder.JSONDecodeError as e:
        # if no file exists, just start with an empty dict
        print(e, type(e))
        translation_dictionary = {}

    for row in data['work'].unique():
        print(row)
        if row in translation_dictionary:
            print("yiss")
        else:
            print("nah")
            translation_dictionary[row] = translator.translate(row).text
            time.sleep(1)
            with open(temporary_json, 'w') as t:
                temp = json.dump(translation_dictionary, t)
            print(type(temp))
