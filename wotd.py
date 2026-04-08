import json
import requests
import os
from cleaner_file import cleaner
from cleaner_file import list_of_prev_wotd_cleaner

WORD = 'skulduggery'
REF_DICTIONARY = "collegiate"
REF_THESAURUS = "thesaurus"
DICTIONARY_KEY = 'f45f1248-4774-4d20-8d31-ecb2d70452e0'
THESAURUS_KEY = '2431331e-690c-4d83-96ac-1f4e9cb350d5'
DEFINITION_KEY = 'shortdef'
TYPE_OF_SPEECH_KEY = 'fl'
DATE_KEY = 'date'
ETYMOLOGY_KEY = 'et'
SYNONYMS = 'syns'
ANTONYMS = 'ants'
NONE_RESULT = 'No info available'
TXT_FOLDER = r'txt_files'
THESAURUS_FOLDER = r'Thesaurus'
WOTD_ARCHIVE = r'Former Words.txt'
PHOTO_FOLDER = r"Photos"
OTHER_FILES = r"other_files"
ARCHIVE_PATH = r'other_files/Former Words.txt'

def get_response(ref, word, key):
    url = f"https://www.dictionaryapi.com/api/v3/references/{ref}/json/{word}?key={key}"
    response = requests.get(url)
    print(url)
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
    for entry in data:
        try:
            syn_group = entry['meta'].get(nyms, [])
            synonyms.append(syn_group)
        except (KeyError, TypeError):
            synonyms.append(NONE_RESULT)
    return synonyms

def create_file(folder, chosen_word, is_thesaurus=False):
    file_name = add_txt_to_file_name(chosen_word)
    folder_path = os.path.join(folder, file_name)
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
    return os.path.join(folder_name, add_txt_to_file_name(file_name))

def find_data_with_path(folder_name, file_name):
    return read_data(create_folder_path(folder_name, file_name))

def add_txt_to_file_name(text):
    return f'{cleaner(text, 5)}.txt'

def list_photo_names(folder_path):
    return [file for file in os.listdir(folder_path) if
            file.endswith(('.jpg', '.webp', '.avif', '.jpeg', '.png', '.gif'))]

class WordVariant:
    def __init__(self, definition=None, type_of_speech=None, date=None, etymology=None, synonyms=None, antonyms=None):
        self.definition = definition
        self.type_of_speech = type_of_speech
        self.date = date
        self.etymology = etymology
        self.synonyms = synonyms
        self.antonyms = antonyms

def create_word_variants(definitions, dates, etymologies, types_of_speech, synonyms, antonyms):
    return [
        WordVariant(definition, type_of_speech, date, etymology, synonyms, antonyms)
        for definition, type_of_speech, date, etymology, synonyms, antonyms in
        zip(definitions, types_of_speech, dates, etymologies, synonyms, antonyms)
    ]

def create_variants(word_selected):
    data = find_data_with_path(TXT_FOLDER, word_selected)
    thes_data = find_data_with_path(THESAURUS_FOLDER, word_selected)
    definition_list = list_manager(data, DEFINITION_KEY, sharp=1)
    date_list = list_manager(data, DATE_KEY, sharp=2)
    etymology_list = list_manager(data, ETYMOLOGY_KEY, sharp=3)
    type_of_speech_list = list_manager(data, TYPE_OF_SPEECH_KEY)
    synonyms_list = extract_synonyms(thes_data, SYNONYMS) if thes_data else [
        NONE_RESULT]
    antonyms_list = extract_synonyms(thes_data, ANTONYMS) if thes_data else [
        NONE_RESULT]
    variants = create_word_variants(definition_list, date_list, etymology_list, type_of_speech_list, synonyms_list, antonyms_list)
    return variants


def add_new_word(chosen_word):
    previous_WOTD = list_of_prev_wotd_cleaner(list_photo_names(PHOTO_FOLDER))
    if chosen_word in previous_WOTD:
        print("Word already added")
        pass
    else:
        previous_WOTD.append(chosen_word)  # Use chosen_word instead of WORD
        save_new_data(ARCHIVE_PATH, previous_WOTD)

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
    print(f'Date first used: {list_of_word_variants[0].date}')
    print(" ")
    print(f'Amount of items in Format: ' + str(len(formated_definition)))
    print(f'Number of variants: ' + str(len(list_of_word_variants)))
    print(" ")
    print(f'Synonyms List: {list_of_word_variants[0].synonyms}')
    print(f'Antonyms List: {list_of_word_variants[0].antonyms}')
    print('')

def main():
    add_new_word(WORD)
    create_archive(WORD)
    first_definition()

main()
previous_WOTD = read_data(ARCHIVE_PATH)
print(previous_WOTD)