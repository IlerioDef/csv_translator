import argparse
import json
import logging
import os
import random
import time
from contextlib import ExitStack
from typing import Iterable, Iterator, List, Any
import pandas as pd
import csv
from googletrans import Translator

PATH_TO_SOURCE_FILE = "./notebooks/data500.csv"  # input("Please enter path to source CSV file")
TARGET_LANGUAGE = "eng"  # input("Please enter target language, i.e. 'eng' ")
PATH_TO_TRANSLATION_FILE = "./.translation.csv"
PATH_TO_FINAL_FILE = "./data3_translated.csv"
CHOICES_MADE = "0,1"
GOOGLE_LENGTH = 4000
LINES_PER_REQUEST = 150  # количество строк, по которым происходит итерация за один запуск цикла.
TARGET_HEADER = 'Объекты административно-территориального деления,^ кроме сельских населенных пунктов'
TARGET_HEADER_ENG = "Объекты деления ENG"
SPLIT_KEY = "\n"

parser = argparse.ArgumentParser()
parser.add_argument("-ps", "--path_source",
                    help="path to source csv file",
                    type=str)
parser.add_argument("-pf", "--path_final",
                    help="path to final csv file, that will be created once translation is finish",
                    type=str)
parser.add_argument("-lpr", "--lines_per_request",
                    help=f"number of column rows that will be packed in one package"
                            f"with the total max length of {GOOGLE_LENGTH} symbols ",
                    type=int)
args = parser.parse_args()
if args.path_source:
    PATH_TO_SOURCE_FILE = args.path_source

if args.path_final:
    PATH_TO_FINAL_FILE = args.path_final

if args.lines_per_request:
    LINES_PER_REQUEST = args.lines_per_request

if args.lines_per_request:
    LINES_PER_REQUEST = args.lines_per_request
logging.basicConfig(level=logging.INFO)


def check_file(path_to_file="") -> str or FileNotFoundError:
    if len(path_to_file) == 0:
        path_to_file = input()

    if not os.path.exists(path_to_file):
        print("wrong path to source file")
        raise FileNotFoundError

    return path_to_file


def get_random_time() -> float:
    timer_seconds = [0.5, 0.75, 1.0, 2.0, 2.5]
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


def create_final_file_name(path_to_sf: str, path_to_tf: str):
    source_file = pd.read_csv(path_to_sf)
    translation_file = pd.read_csv(path_to_tf)
    if verify_lens(source_file, translation_file):
        final_file = source_file.join(translation_file)
        return final_file
    else:
        raise ValueError


def verify_lens(source_file, translation_file):
    if len(source_file) == len(translation_file):
        return True
    else:
        return False


@timer_func
def pack_to_string(pack_components: list) -> str:
    packed_string = ""
    print("type(pack_components)", type(pack_components))
    for v in pack_components:
        if len(packed_string) < GOOGLE_LENGTH:
            packed_string += f"{v}{SPLIT_KEY} "

        else:
            break

    return packed_string


@timer_func
def translate_pack(_packed_string: str or None) -> str or None:
    translator = Translator()
    if _packed_string is None:
        translated_string = None
    else:
        translated_string = translator.translate(_packed_string).text

    return translated_string


@timer_func
def unpack_string(packed_string: str) -> list[str]:
    string_to_list = packed_string.strip().split(SPLIT_KEY)
    string_cleared = [item.strip() for item in string_to_list]

    return string_cleared


@timer_func
def iterate_batches(iterable_data: Iterator, batch_size: int) -> dict:
    """

    @param batch_size: int
    @type iterable_data: object
    """
    flag = True
    while flag:
        _batch: list[Any] = []
        try:
            for _ in range(batch_size):
                row = next(iterable_data)
                _batch.append(row)
        except StopIteration as e:
            print(f"File has ended. {e}")
            flag = False
        yield _batch


@timer_func
def get_column_data(_batch: list, header) -> list:
    """

    @param header:
    @type _batch: list
    """
    column_data = [row[header].strip() for row in _batch]
    return column_data


if __name__ == "__main__":
    path = check_file(PATH_TO_SOURCE_FILE)

    with ExitStack() as stack:
        csvfile = stack.enter_context(open(path, "r+", newline=''))
        csvfile2 = stack.enter_context(open(PATH_TO_TRANSLATION_FILE, "w+", newline=''))
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
                    f' len(US) {len(unpacked_string)}, len(CB) {len(column_batch)} '
                    f'\n unpacked_string {unpacked_string} \n column_batch  {column_batch}')
                raise ValueError

            # print("len(unpacked_string)",len(unpacked_string))

            for x in unpacked_string:
                csv_writer.writerow([x, ])

    final_file = create_final_file_name(PATH_TO_SOURCE_FILE, PATH_TO_TRANSLATION_FILE)
    print(final_file, sep="\n")
    final_file.to_csv(PATH_TO_FINAL_FILE)
