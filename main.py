import argparse
import json
import logging
import os
import random
import time
from typing import Iterable, Iterator
import pandas as pd
import csv
from googletrans import Translator


def get_random_time() -> float:
    timer_seconds = [1.0, 0.5, 3.0, 2.0, 0.75]
    shuffle = random.choice(timer_seconds)
    return shuffle


def timer_func(func):
    # This function shows the execution time of
    # the function object passed
    def wrap_func(*args, **kwargs):
        t1 = time.time()
        result = func(*args, **kwargs)
        t2 = time.time()
        print(f'Function {func.__name__!r} executed in {(t2 - t1):.4f}s')
        return result

    return wrap_func


PATH_TO_SOURCE_FILE = "./notebooks/data500.csv"  # input("Please enter path to source CSV file")
TARGET_LANGUAGE = "eng"  # input("Please enter target language, i.e. 'eng' ")
PATH_TO_TRANSLATION_FILE = "./eng.csv"
PATH_TO_FINAL_FILE = "./data3_translated.csv"
CHOICES_MADE = "0,1"
GOOGLE_LENGTH = 4000
LINES_PER_REQUEST = 150  # количество строк, по которым происходит итерация за один запуск цикла.
TARGET_HEADER = 'Объекты административно-территориального деления,^ кроме сельских населенных пунктов'
TARGET_HEADER_ENG = "Объекты деления ENG"


@timer_func
def pack_to_string(pack_components: list) -> str:
    packed_string = ""
    print("type(pack_components)", type(pack_components))
    for v in pack_components:
        if len(packed_string) < GOOGLE_LENGTH:
            packed_string += f"{v}\n "

        else:
            break

    return packed_string


@timer_func
def translate_pack(_packed_string: str or None) -> str or None:
    translator = Translator()
    if _packed_string == None:
        return None
    else:
        translated_string = translator.translate(_packed_string).text
    return translated_string


@timer_func
def unpack_string(_packed_string: str) -> pd.Series:
    _string_to_list = _packed_string.strip().split("\n")
    string_cleared = [x.strip() for x in _string_to_list]

    return string_cleared


@timer_func
def iterate_batches(iterable_data: Iterator, batch_size: int) -> dict:
    flag = True
    while flag:
        batch = []
        try:
            for _ in range(batch_size):
                row = next(iterable_data)
                batch.append(row)
        except StopIteration as e:
            print(f"File has ended. {e}")
            flag = False
        yield batch


@timer_func
def get_column_data(batch, header) -> list:
    column_data = [row[header].strip() for row in batch]
    return column_data


if __name__ == "__main__":
    with open(PATH_TO_SOURCE_FILE, "r+", newline='') as csvfile:
        with open(PATH_TO_TRANSLATION_FILE, "w+", newline='') as csvfile2:

            dict_reader = csv.DictReader(csvfile)
            csv_writer = csv.writer(csvfile2)
            csv_writer.writerow([f'{TARGET_HEADER_ENG}'])

            batches = iterate_batches(dict_reader, LINES_PER_REQUEST)
            for batch in batches:
                column_batch = get_column_data(batch, TARGET_HEADER)
                print("len(column_batch)", len(column_batch))
                pack = pack_to_string(column_batch)
                # print("len(pack)",len(pack))
                translated_pack = translate_pack(pack)
                # print("len(translated_pack)",len(translated_pack))
                sleeping_timer = get_random_time()
                print(f"timer set to: {sleeping_timer}")
                time.sleep(sleeping_timer)
                unpacked_string = unpack_string(translated_pack)
                print("len(unpacked_string", len(unpacked_string))
                if len(unpacked_string) == len(column_batch):
                    print("len(unpacked_string) == len(column_batch)", "YES")
                else:
                    print("len(unpacked_string) == len(column_batch)", "NO")
                    print(
                        f" len(US) {len(unpacked_string)}, len(CB) {len(column_batch)} \n unpacked_string {unpacked_string} \n column_batch  {column_batch}")
                    raise ValueError

                # print("len(unpacked_string)",len(unpacked_string))

                for x in unpacked_string:
                    csv_writer.writerow([x, ])
