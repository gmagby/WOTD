import json
import re
import requests
import os
from cleaner_file import cleaner
from cleaner_file import list_of_prev_wotd_cleaner


WORD = 'Peregrine'
REF_DICTIONARY = "collegiate"
REF_THESAURUS = "thesaurus"
DICTIONARY_KEY = os.getenv('DICTIONARY_KEY', 'f45f1248-4774-4d20-8d31-ecb2d70452e0')
THESAURUS_KEY = os.getenv('THESAURUS_KEY', '2431331e-690c-4d83-96ac-1f4e9cb350d5')
DEFINITION_KEY = 'shortdef'
TYPE_OF_SPEECH_KEY = 'fl'
DATE_KEY = 'date'
ETYMOLOGY_KEY = 'et'
SYNONYMS = 'syns'
ANTONYMS = 'ants'
STATS = 'hwi'
PRONUNCIATION = 'hw'
NONE_RESULT = 'No info available'
TXT_FOLDER = r'txt_files'
THESAURUS_FOLDER = r'Thesaurus'
WOTD_ARCHIVE = r'Former Words.txt'
FUTURE_LIST = r'other_files/FUTURE WOTD.txt'
PHOTO_FOLDER = r"Photos"
OTHER_FILES = r"other_files"
ARCHIVE_PATH = r'other_files/Former Words.txt'


def read_data(path):
    try:
        if os.path.exists(path):
            with open(path, "r") as f:
                data = json.loads(f.read())
                return data
        return []

    except (ValueError, FileNotFoundError, json.JSONDecodeError):
        print("Error", "Something went wrong.")
        return []

previous_WOTD = read_data(ARCHIVE_PATH)


def get_response(ref, word, key):
    url = f"https://www.dictionaryapi.com/api/v3/references/{ref}/json/{word}?key={key}"
    response = requests.get(url)
    print(f"Fetching: https://www.dictionaryapi.com/api/v3/references/{ref}/json/{word}?key=HIDDEN")
    return response.json()

def get_data(word_selected):
    return get_response(REF_DICTIONARY, word_selected, DICTIONARY_KEY)

def get_thes_data(word_selected):
    return get_response(REF_THESAURUS, word_selected, THESAURUS_KEY)

def check_for_no_data(text):
    if text != 'No info available':
        return True
    else:
        return False

def list_manager(data, syntax, sharp=None):
    return [
        cleaner(item.get(syntax, NONE_RESULT), sharp) if item.get(syntax) else NONE_RESULT
        for item in data
    ]

def extract_synonyms(data, nyms):
    synonyms = []
    if not data or not isinstance(data, list):
        return [NONE_RESULT]
    for entry in data:
        try:
            if isinstance(entry, dict) and 'meta' in entry:
                syn_group = entry['meta'].get(nyms, [])
                if syn_group:
                    synonyms.append(syn_group)
        except (KeyError, TypeError):
            pass
    return synonyms if synonyms else [NONE_RESULT]

def extract_pronunciation(data, syntax, info):
    for entry in data:
        try:
            pronounce = entry[syntax].get(info)
            return pronounce
        except (KeyError, TypeError):
            pass

# def create_file(folder, chosen_word, is_thesaurus=False):
#     file_name = add_dottxt_to_file_name(chosen_word)
#     folder_path = os.path.join(folder, file_name)
#     if not os.path.exists(folder_path):
#         data = get_thes_data(chosen_word) if is_thesaurus else get_data(chosen_word)
#         save_new_data(folder_path, data)

def create_file(folder, chosen_word, is_thesaurus=False):
    folder_path = create_folder_path(folder, chosen_word)
    if not os.path.exists(folder_path):
        data = get_thes_data(chosen_word) if is_thesaurus else get_data(chosen_word)
        save_new_data(folder_path, data)

def save_new_data(file_name, data):
    with open(file_name, "w") as f:
        f.write(json.dumps(data))

def read_data(path):
    try:
        if os.path.exists(path):
            with open(path, "r") as f:
                data = json.loads(f.read())
                return data

    except ValueError:
        print("Error", "Something went wrong.")

def create_folder_path(folder_name, file_name):
    return os.path.join(folder_name, add_dottxt_to_file_name(file_name))

def find_data_with_path(folder_name, file_name):
    return read_data(create_folder_path(folder_name, file_name))

def add_dottxt_to_file_name(text):
    return f'{cleaner(text, 5)}.txt'

def list_photo_names(folder_path):
    return [file for file in os.listdir(folder_path) if
            file.endswith(('.jpg', '.webp', '.avif', '.jpeg', '.png', '.gif'))]
def list_and_sort_files():
    folder_path = r'Photos'
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    files_with_dates = [(f, os.path.getctime(os.path.join(folder_path, f))) for f in files]
    sorted_files = sorted(files_with_dates, key=lambda x: x[1])
    print(len(sorted_files))
    return [f[0] for f in sorted_files]

class WordVariant:
    def __init__(self, definition=None, type_of_speech=None, date=None, etymology=None, synonyms=None, antonyms=None, pronunciation=None):
        self.definition = definition
        self.type_of_speech = type_of_speech
        self.date = date
        self.etymology = etymology
        self.synonyms = synonyms
        self.antonyms = antonyms
        self.pronunciation = pronunciation

def create_word_variants(definitions, dates, etymologies, types_of_speech, synonyms, antonyms, pronunciation):
    return [
        WordVariant(definition, type_of_speech, date, etymology, synonyms, antonyms, pronunciation)
        for definition, type_of_speech, date, etymology, synonyms, antonyms in
        zip(definitions, types_of_speech, dates, etymologies, synonyms, antonyms)
    ]

def create_variants(word_selected):
    data = read_data(create_folder_path(TXT_FOLDER, word_selected))
    thes_data = read_data(create_folder_path(THESAURUS_FOLDER, word_selected))
    definition_list = list_manager(data, DEFINITION_KEY, sharp=1)
    date_list = list_manager(data, DATE_KEY, sharp=2)
    etymology_list = list_manager(data, ETYMOLOGY_KEY, sharp=3)
    type_of_speech_list = list_manager(data, TYPE_OF_SPEECH_KEY)
    synonyms_list = extract_synonyms(thes_data, SYNONYMS) if thes_data else [
        NONE_RESULT]
    antonyms_list = extract_synonyms(thes_data, ANTONYMS) if thes_data else [
        NONE_RESULT]
    pronunciation_list = extract_pronunciation(data, STATS, PRONUNCIATION)
    variants = create_word_variants(definition_list, date_list, etymology_list, type_of_speech_list, synonyms_list, antonyms_list, pronunciation_list)
    return variants

def add_toFuture_list(chosen_word):
    path = read_data(FUTURE_LIST)
    path.append(chosen_word)
    save_new_data(FUTURE_LIST, path)

def add_new_word(chosen_word):
    previous_WOTD = read_data(ARCHIVE_PATH)
    print(previous_WOTD)
    if chosen_word in previous_WOTD:
        print("Word already added")
    else:
        previous_WOTD.append(chosen_word)  # Append to the end for chronological log
        save_new_data(ARCHIVE_PATH, previous_WOTD)
        add_toFuture_list(WORD)
    return previous_WOTD

def create_archive(chosen_word):
    create_file(TXT_FOLDER, chosen_word)
    create_file(THESAURUS_FOLDER, chosen_word, is_thesaurus=True)

# Text to List Converter
def format_text(text):
    return text.split('^')

def first_definition():
    list_of_word_variants = create_variants(WORD)
    formated_definition = format_text(list_of_word_variants[0].definition)
    print("Formated Text:")
    for t in range(len(formated_definition)):
        print(formated_definition[t])
    print(f'{list_of_word_variants[0].pronunciation}')
    print(f'Date first used: {list_of_word_variants[0].date}')
    print(f'{list_of_word_variants[0].etymology}')
    print(" ")
    print(f'Amount of items in Format: ' + str(len(formated_definition)))
    print(f'Number of variants: ' + str(len(list_of_word_variants)))
    print(" ")
    print(f'Synonyms List: {list_of_word_variants[0].synonyms}')
    print(f'Antonyms List: {list_of_word_variants[0].antonyms}')

    print('')
    for t in range(1, len(list_of_word_variants)):  # Start from 1 to avoid accessing index 0
        print(list_of_word_variants[t].definition)
    print(list_of_word_variants[0].antonyms)

def enter_input():
    return input("Enter '1' to add the word to the archive: ") == '1'


def run_wotd_func(word=None):
    if word is None:
        word = WORD
    first_definition()  # Pass word if you want it to print that specific word's data
    if enter_input():
        add_new_word(word)
        create_archive(word)
    else:
        pass

    from update_html import update_index_html
    update_index_html(word)
    
    # Refresh previous_WOTD after adding a new word
    global previous_WOTD
    previous_WOTD = read_data(ARCHIVE_PATH)




if __name__ == "__main__":
    run_wotd_func()
