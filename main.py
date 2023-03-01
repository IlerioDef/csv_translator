import json
import pandas as pd
from googletrans import Translator
import time
from tqdm import tqdm
import datetime as dt
translator = Translator()
LANGUAGES = {
    "af":"_AFR",
    "ga":"_GAE",
    "sq":"_ALB",
    "it":"_ITA",
    "ar":"_ARB",
    "ja":"_JAP",
    "az":"_AZR",
    "kn":"_KAN",
    "eu":"_BSQ",
    "ko":"_KOR",
    "bn":"_BEN",
    "la":"_LAT",
    "be":"_BEL",
    "lv":"_LAV",
    "bg":"_BUL",
    "lt":"_LIT",
    "ca":"_CAT",
    "mk":"_MAC",
    "zh-CN":"_CHN",
    "ms":"_MAL",
    "zh-TW":"_CHN",
    "mt":"_MAL",
    "hr":"_CRO",
    "no":"_NOR",
    "cs":"_CSZ",
    "fa":"_PER",
    "da":"_DNS",
    "pl":"_POL",
    "nl":"_DUT",
    "pt":"_POR",
    "en":"_ENG",
    "ro":"_ROM",
    "eo":"_ESR",
    "ru":"_RUS",
    "et":"_EST",
    "sr":"_SRB",
    "tl":"_TAG",
    "sk":"_SLK",
    "fi":"_FIN",
    "sl":"_SLO",
    "fr":"_FRA",
    "es":"_ESP",
    "gl":"_GAL",
    "sw":"_SWA",
    "ka":"_GEO",
    "sv":"_SWE",
    "de":"_DEU",
    "ta":"_TAM",
    "el":"_GRE",
    "te":"_TEL",
    "gu":"_GUJ",
    "th":"_THA",
    "ht":"_HAI",
    "tr":"_TUR",
    "iw":"_HEB",
    "uk":"_UKR",
    "hi":"_HIN",
    "ur":"_URD",
    "hu":"_HUN",
    "vi":"_VIE",
    "is":"_ISL",
    "cy":'_WEL',
    "id":"_IND",
    "yi":"_YID",
    }

def CSV_translator(csv_to_translate, columns, number_of_tries=3, sleep_timer=1, dest='en'):
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
    dest: destination language, "en" (English) as a default value.
    RETURN:

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

    def translator_iterator(columns, translation_dictionary, number_of_tries, sleep_timer):
        for column in columns:
            try:
                for row in tqdm(data[column].unique()):
                    if row in translation_dictionary:
                        continue
                    else:

                        translation_dictionary[row] = translator.translate(row).text
                        time.sleep(sleep_timer)
                        with open("temp.json", 'w') as t:
                            temp = json.dump(translation_dictionary, t)
    #
            except (ValueError, AttributeError, NameError) as e:
                now = dt.datetime.now()
                current_time = now.strftime("%H:%M:%S")
                print(e, type(e))
                with open("error.log", 'w') as fh:
                    fh.write(f"{e}, {type(e)}, {current_time}")

                time.sleep(1)
                while number_of_tries !=0:
                    translator_iterator(columns, translation_dictionary, number_of_tries, sleep_timer)
                    number_of_tries -= 1

        return translation_dictionary

    temp = translator_iterator(columns, translation_dictionary, number_of_tries, sleep_timer)

    for column in columns:
        translated_header = column + LANGUAGES[dest]
        data[translated_header] = data[column].map(translation_dictionary)
        print(data.info())

    data.to_csv("New_file.csv")