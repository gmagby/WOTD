import streamlit as st
from wotd import previous_WOTD
from wotd import WORD
from PIL import Image
from wotd import create_variants
import os

def create_new_variants(chosen_word):
    list_of_word_variants = create_variants(chosen_word)
    print(list_of_word_variants)
    return list_of_word_variants

favored = 0

def guide_func(chosen_word):
    new_word_variants_list = create_new_variants(chosen_word)
    top_of_page(chosen_word, new_word_variants_list)
    first_definition(chosen_word, new_word_variants_list)
    verify_more_definitions(chosen_word, new_word_variants_list)
    sidebar(chosen_word, new_word_variants_list)
    st.image(display_photo(chosen_word))


def verify_more_definitions(chosen_word, variant):
    num = len(variant)
    if num > 1:
        if check_for_no_data(variant[1].definition):
            if st.button("All Definitions"):
                more_definitions(chosen_word, variant)
        else:
            pass
    else:
        pass

def top_of_page(chosen_word, variant):
    st.header("Word of the Day", divider="rainbow")
    st.title(chosen_word)
    st.markdown(f'**{variant[favored].type_of_speech}**')


# Text to List Converter
def format_text(text):
    text = text.split('^')
    return text

def check_for_no_data(text):
    if text != 'No info available':
        return True

    else:
        return False

def pull_specific_photo(folder_path, photo_name):
    # Default case (equivalent to else)
    photo_path = os.path.join(folder_path, photo_name)
    if os.path.exists(photo_path):
        return Image.open(photo_path)
    else:
        raise FileNotFoundError(f"The photo '{photo_name}' does not exist in the specified folder.")

def display_photo(chosen_word):
    today_photo = pull_specific_photo(r"Photos", f"{chosen_word}.jpg")
    return today_photo

def first_definition(chosen_word, variant):
    formated_definition = format_text(variant[favored].definition)
    for t in range(len(formated_definition)):
        st.write(
            f'{formated_definition[t]}')

def more_definitions(chosen_word, variant):
    for t in range(1, len(variant)):  # Start from 1 to avoid accessing index 0
        if check_for_no_data(variant[t].definition):
            st.header(chosen_word, divider="rainbow")
            st.markdown(f'{format_text(variant[t].definition)}')
            st.markdown(f'**{variant[t].type_of_speech}**')
            st.markdown(f'Etymology: {format_text(variant[t].etymology)}')
            st.markdown(f'Date first used: {variant[t].date}')
            if check_for_no_data(variant[t].synonyms):
                st.markdown("Synonyms:")
                st.markdown(variant[t].synonyms)
                st.markdown("Antonyms:")
                st.markdown(variant[t].antonyms)

def display_instructions():
    st.sidebar.markdown('Instructions on how to make WOTD into a widget on your homescreen.')
    st.sidebar.markdown(
        'Safari Instructions: [Here](https://docs.google.com/presentation/d/1ICISEQxe1UuQ7Z3xBA9gU8fPLrTMFCbIZSy9M_au0HY/edit?usp=sharing)')
    st.sidebar.markdown(
        'Chrome instructions: [Here](https://docs.google.com/presentation/d/1B5HWIi_X_8wNhbKWEcTfKhnWs4DfLsemZEEiym612Y8/edit?usp=sharing)')



def sidebar(chosen_word, variant):
    st.sidebar.title(chosen_word)
    st.sidebar.markdown(f'**{variant[favored].type_of_speech}**')

    if check_for_no_data(variant[favored].etymology):
        if st.sidebar.button("Etymology"):
            for t in range(len(variant)):
                st.sidebar.markdown(variant[favored].etymology)
    else:
        pass

    if check_for_no_data(variant[favored].synonyms):
        if st.sidebar.button('Thesaurus'):
            st.sidebar.markdown("Synonyms:")
            st.sidebar.markdown(variant[favored].synonyms)
            st.sidebar.markdown("Antonyms:")
            st.sidebar.markdown(variant[favored].antonyms)
    else:
        pass

    def create_merriam_url(chosen_word):
        url = f'https://www.merriam-webster.com/dictionary/{chosen_word}'
        return url

    def create_merriam_button(text, chosen_word):
        button = st.sidebar.link_button(f'{text}', create_merriam_url(chosen_word))
        return button

    create_merriam_button('Merriam-Webster', WORD)

    if st.sidebar.button("Instructions to add WOTD to your homescreen"):
        display_instructions()

    if st.sidebar.button('Previous words of the day.'):
        for t in previous_WOTD:
            create_merriam_button(t, t)

guide_func(WORD)


import json
import re
import requests
import os

WORD = 'easter'
chosen_word = 'aver'
REF_DICTIONARY = "collegiate"
REF_THESAURUS = "thesaurus"
DICTIONARY_KEY = 'f45f1248-4774-4d20-8d31-ecb2d70452e0'
Thesaurus_key = '2431331e-690c-4d83-96ac-1f4e9cb350d5'
DEFINITION_KEY = 'shortdef'
TYPE_OF_SPEECH_KEY = 'fl'
DATE_KEY = 'date'
ETYMOLOGY_KEY = 'et'
SYNONYMS = 'syns'
ANTONYMS = 'ants'
NONE_RESULT = 'No info available'
PHOTO_FOLDER = r"Photos"
TXT_FOLDER = r'txt_files'
THESAURUS_FOLDER = r'Thesaurus'

def get_response_dictionary(ref, word, key):
    url = f"https://www.dictionaryapi.com/api/v3/references/{ref}/json/{word}?key={key}"
    response = requests.get(url)
    print(url)
    return response.json()

def get_data(word_selected):
    data = get_response_dictionary(REF_DICTIONARY, word_selected, DICTIONARY_KEY)
    return data

def get_thes_data(word_selected):
    thes_data = get_response_dictionary(REF_THESAURUS, word_selected, Thesaurus_key)
    return thes_data

def cleaner(clean_text, sharp=None):
    print(clean_text)
    clean_text = str(clean_text)
    def etymology_cleaner(clean_text):
        clean_text = re.sub(r"dx_ety}", '', clean_text)
        clean_text = re.sub(r"mat}", '', clean_text)
        clean_text = re.sub(r"bc}", '', clean_text)
        clean_text = re.sub(r"ma}", '', clean_text)
        clean_text = re.sub(r"dx}", '', clean_text)
        clean_text = re.sub(r"dxt", '', clean_text)
        clean_text = re.sub(r'it}', '', clean_text)
        clean_text = re.sub(r"'text', ", '', clean_text)
        clean_text = re.sub(r']]', '', clean_text)
        clean_text = re.sub(r"et_link", '', clean_text)
        clean_text = re.sub(r":2", '', clean_text)
        clean_text = re.sub(r":1", '', clean_text)
        clean_text = re.sub(r"-ia", '', clean_text)
        clean_text = re.sub(r"et_snote',", '', clean_text)
        clean_text = re.sub(r"et_snote", '', clean_text)
        clean_text = re.sub(r"'t',", '', clean_text)
        clean_text = re.sub(r"', '", ', ^', clean_text)
        clean_text = re.sub(r"andor", 'and/or', clean_text)
        clean_text = re.sub(r"[\#[/@<>{}=~|?]", '', clean_text)
        clean_text = re.sub(r"]", '', clean_text)
        return clean_text
    def definition_cleaner(clean_text):
        clean_text = re.sub(r"', '", ', ^', clean_text)
        return clean_text
    def date_cleaner(clean_text):
        # clean_text = re.sub(r"ds1", '', clean_text)
        # clean_text = re.sub(r",", ' or', clean_text)
        clean_text = re.sub(r'dst2', '', clean_text)
        clean_text = re.sub(r"ds1a", '', clean_text)
        clean_text = re.sub(r"dst", '', clean_text)
        clean_text = re.sub(r"ds1b", '', clean_text)
        clean_text = re.sub(r'dst2', '', clean_text)
        clean_text = re.sub(r'ds3', '', clean_text)
        clean_text = re.sub(r'ds5', '', clean_text)
        clean_text = re.sub(r"dx_ety", '', clean_text)
        clean_text = re.sub(r"dxt", '', clean_text)
        clean_text = re.sub(r"dsi1", '', clean_text)
        clean_text = re.sub(r'ds1', '', clean_text)
        clean_text = re.sub(r'ds2', '', clean_text)
        clean_text = re.sub(r'1a', '', clean_text)
        clean_text = re.sub(r'.jpg', '', clean_text)
        clean_text = re.sub(r'.jpeg', '', clean_text)
        clean_text = re.sub(r'.png', '', clean_text)
        clean_text = re.sub(r'.gif', '', clean_text)
        return clean_text
    def base_cleaner(clean_text):
        clean_text = re.sub(r"\s+", " ", clean_text).strip()  # Remove extra spaces
        clean_text = re.sub(r"[\#[/@<>{}=~|?]", '', clean_text)
        clean_text = re.sub(r"]", '', clean_text)
        clean_text = re.sub(r" u ", " 'u' ", clean_text)
        clean_text = re.sub(r"'", '', clean_text)
        return clean_text
    if sharp == 1:  # Definition cleaner
        clean_text = base_cleaner(definition_cleaner(clean_text))
    if sharp == 2:  # Date cleaner
        clean_text = date_cleaner(base_cleaner(clean_text))
    if sharp == 3:  # Etymology cleaner
        clean_text = base_cleaner(etymology_cleaner(clean_text))
    if sharp == 4:
        base_cleaner(clean_text)
    clean_text = re.sub(r"\s+", " ", clean_text).strip()
    clean_text = str(clean_text)
    print(clean_text)
    print(" ")
    return clean_text

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
            synonyms.append([syn for syn in syn_group])
        except (KeyError, TypeError):
            synonyms.append(NONE_RESULT)  # Append an empty list if there's an error
    return synonyms


def create_file(chosen_word, folder):
    file_name = f'{chosen_word}.txt'
    try:
        folder_path = os.path.join(folder, file_name)
        if os.path.exists(folder_path):
            pass
        else:
            save_to_file(folder_path, get_data(chosen_word))
    except ValueError:
        print("Error", "Something went wrong.")

def create_thes_file(chosen_word, folder):
    file_name = f'{chosen_word}.txt'
    try:
        folder_path = os.path.join(folder, file_name)
        if os.path.exists(folder_path):
            pass
        else:
            save_to_file(folder_path, get_thes_data(chosen_word))
    except ValueError:
        print("Error", "Something went wrong.")

def save_to_file(file_name, data):
    with open(file_name, "w") as f:
        f.write(json.dumps(data))

def read_data(chosen_word, folder):
    file_name = f'{chosen_word}.txt'
    try:
        folder_path = os.path.join(folder, file_name)
        if os.path.exists(folder_path):
            with open(folder_path, "r") as f:
                data = json.loads(f.read())
                return data

    except ValueError:
       print("Error", "Something went wrong.")

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
    try:
        thes_data = read_data(word_selected, THESAURUS_FOLDER)
        data = read_data(word_selected, TXT_FOLDER)

    except TypeError:
        data = get_data(word_selected)
        thes_data = get_thes_data(word_selected)
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

def list_photo_names(folder_path):
    return [file for file in os.listdir(folder_path) if
            file.endswith(('.jpg', '.webp', '.avif', '.jpeg', '.png', '.gif'))]

def list_of_prev_wotd_cleaner(clean_text):
    print(clean_text)
    clean_text = str(clean_text)
    clean_text = re.sub(r'.jpg', '', clean_text)
    clean_text = re.sub(r'.jpeg', '', clean_text)
    clean_text = re.sub(r'.png', '', clean_text)
    clean_text = re.sub(r'.gif', '', clean_text)
    clean_text = re.sub(r'.webp', '', clean_text)
    clean_text = re.sub(r'.avif', '', clean_text)
    clean_text = re.sub(r"[\#[/@<>{}=~|?]", '', clean_text)
    clean_text = re.sub(r"]", '', clean_text)
    clean_text = re.sub(r"'", '', clean_text)
    clean_text = re.sub(r"2", '', clean_text)
    clean_text = clean_text.lower()
    clean_list = clean_text.split(", ")
    clean_list.sort(key=str.lower)
    print(clean_list)
    print('')
    print(len(clean_list))
    return clean_list

photo_folder = r"Photos"
previous_WOTD = list_of_prev_wotd_cleaner(list_photo_names(photo_folder))
for t in previous_WOTD:
    create_file(t, TXT_FOLDER)
    create_thes_file(t, THESAURUS_FOLDER)

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
