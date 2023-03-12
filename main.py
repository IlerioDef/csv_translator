# План рефакторинга
# + 1. Приведем в порядок requirements.txt
# + 2. Выделить из csv_translator функции по их ответственности.
# + 3. Реализуем CLI-интерфейс.
# 4. Сделаем из этого хороший добротный скрипт!

import argparse
import json
import logging
import time

import pandas as pd
from googletrans import Translator

translator = Translator()
logging.basicConfig(filename='errors.log', encoding='utf-8', level=logging.DEBUG)

parser = argparse.ArgumentParser()
parser.add_argument("source")
parser.add_argument("--columns", "-c", nargs="+", required=True)
parser.add_argument("--lang", "-l", default="en")
parser.add_argument("--fast", "-f", action="store_true")
parser.add_argument("--debug", "-d", action="store_true")


def retry(max_retries=10):
    """
    simple decorator-iterator. When number max_retries depletes it returns a warning.
    """

    def retry_decorator(func):
        def _wrapper(*args, **kwargs):
            for _ in range(max_retries):
                try:
                    func(*args, **kwargs)
                except:
                    time.sleep(10)
                    print(f"{_ + 1} of {max_retries} tries used")

        return _wrapper

    return retry_decorator


def save_translated_file(path: str, data: pd.DataFrame, columns: list, dictionary: dict):
    pass


def translate(value: str, lang: str, delay: int) -> str:
    pass


def populate_dictionary(dictionary: dict, lang: str) -> None:
    # TODO: Сохранение словаря в файл после обновления.
    # TODO: Можно сделать в одну строчку с помощью метода словаря. Какого?
    pass


def get_dictionary(lang: str) -> dict:
    dictionary = {}

    try:
        with open(f"{lang}.json") as fh:
            return json.load(fh)
    except FileNotFoundError:
        return dictionary


def read_source_file(path: str) -> pd.DataFrame:
    # TODO: Проверка существования файла.
    with open(path) as fh:
        return pd.read_csv(fh)


def main(source: str, lang: str, columns: list, delay: int):
    # + 1. Читаешь исходный csv-файл.
    # + 2. Получаешь словарь.
    # 3. Переводишь csv-файл с помощью словаря, подтягивая недостающие переводы.
    # 4. Записываешь переведенную колонку в csv-файл.
    # 5. Сохраняешь новый csv-файл.
    pass


if __name__ == '__main__':
    # TODO: Настройка логирования и настройка скорости перевода.
    args = parser.parse_args()
    # main(args.source, args.lang)


# def csv_translator(csv_to_translate, columns, sleep_timer=1, dest='en'):
#     """
#     CSV translator for files that contains data in languages other that English.
#     Saves the result in a json dictionary.
#     TODO: handles for translation on the different languages.
#     csv_to_translate: path to a CSV_file that has columns you want to translate
#     columns: should be a list or a tuple to iterate on
#     number_of_tries: since translator is unstable most probably
#     it will take several times to translate all the data need thus
#     you can change the number of tries before failure. Default number is 3.
#     sleep_timer: number of seconds between requests. Default is 1 second.
#     dest: destination language, "en" (English) as a default value.
#     RETURN:
#
#     """
#     # + 1. Читаешь исходный csv-файл.
#     # + 2. Получаешь словарь.
#     # 3. Переводишь csv-файл с помощью словаря, подтягивая недостающие переводы.
#     # 4. Записываешь переведенную колонку в csv-файл.
#     # 5. Сохраняешь новый csv-файл.
#
#     def translator_iterator(columns, dest_translation_dictionary, number_of_tries, sleep_timer):
#         for column in columns:
#             try:
#                 for row in tqdm(data[column].unique()):
#                     # Заменить на populate_dictionary.
#                     if row in translation_dictionary:
#                         continue
#                     else:
#
#                         dest_translation_dictionary[row] = translator.translate(row, dest=dest).text
#                         print(dest_translation_dictionary[row])
#                         # dump translated into json file
#                         time.sleep(sleep_timer)
#                         with open("temp.json", 'w') as t:
#                             temp = json.dump(translation_dictionary, t, indent=4)
#
#             except (ValueError, AttributeError, NameError) as e:
#                 now = dt.datetime.now()
#                 current_time = now.strftime("%H:%M:%S")
#                 logging.error(e, type(e))
#                 with open("error.log", 'w') as fh:
#                     fh.write(f"{e}, {type(e)}, {current_time}")
#
#                 time.sleep(1)
#                 while number_of_tries != 0:
#                     translator_iterator(columns, translation_dictionary, number_of_tries, sleep_timer)
#                     number_of_tries -= 1
#     # open a csv to translate
#     with open(csv_to_translate, mode="r") as csv_file:
#         data = pd.read_csv(csv_file, low_memory=False)
#
#     translation_dictionary = existence_check("temp.json")  # TODO: redo the file name
#     name_ending = LANGUAGES[dest]
#     translation_dictionary[dest] = translation_dictionary[dest]
#
#
#
#         return translation_dictionary
#     temp = translator_iterator(columns, translation_dictionary, number_of_tries, sleep_timer)
#
#     for column in columns:
#         translated_header = column + LANGUAGES[dest]
#         data[translated_header] = data[column].map(translation_dictionary)
#         print(data.info())
#
#     data.to_csv("New_file.csv")
