import re
import requests

WORD = 'Steerage'
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
file_name = "Former Words of the day"

def get_response_dictionary(ref, word, key):
    url = f"https://www.dictionaryapi.com/api/v3/references/{ref}/json/{word}?key={key}"
    response = requests.get(url)
    print(url)
    return response.json()

# def offline_data():
#     try:
#         if os.path.exists(file_name):
#             with open(file_name, "r") as f:
#                 new_data = json.loads(f.read())
#                 return new_data
#
#             # with open(file_name, "w") as f:
#             #     f.write(json.dumps(new_data))
#
#     except ValueError:
#         messagebox.showerror("Error", "Something went wrong.")


def cleaner(clean_text, sharp=None):
    clean_text = str(clean_text)
    if sharp:
        clean_text = re.sub(r"bc}", '', clean_text)
        clean_text = re.sub(r"dx}", '', clean_text)
        clean_text = re.sub(r'it}', '', clean_text)
        clean_text = re.sub(r'text', '', clean_text)
        clean_text = re.sub(r"'", '', clean_text)
        clean_text = re.sub(r", P", 'P', clean_text)
        # clean_text = re.sub(r"[^a-zA-Z0-9:]", " ", clean_text)
        clean_text = re.sub(r"\s+", " ", clean_text).strip()  # Remove extra spaces
    clean_text = re.sub(r"[\#[/@<>{}=~|?]", '', clean_text)
    # clean_text = re.sub(r"'", '', clean_text)
    clean_text = re.sub(r"ds1", '', clean_text)
    clean_text = re.sub(r",", ' or', clean_text)
    clean_text = re.sub(r"]", '', clean_text)
    clean_text = re.sub(r"ds1a", '', clean_text)
    clean_text = re.sub(r"dst", '', clean_text)
    print(clean_text)
    return clean_text


def list_manager(data, syntax):
    return [
        cleaner(item.get(syntax, NONE_RESULT)) if item.get(syntax) else NONE_RESULT
        for item in data
    ]

def et_list_manager(data, syntax):
    return [
        cleaner(item.get(syntax, NONE_RESULT),1) if item.get(syntax) else NONE_RESULT
        for item in data
    ]

def extract_synonyms(data, nyms):
    nyms_lists = []  # List to hold lists of synonyms/antonyms for each entry

    for entry in data:
        entry_nyms_list = [syn for syn_group in entry['meta'].get(nyms, []) for syn in syn_group] or [NONE_RESULT]
        nyms_lists.append(entry_nyms_list)  # Append the entry's list to the main list
    return nyms_lists

data = get_response_dictionary(REF_DICTIONARY, WORD, DICTIONARY_KEY)

try:
    thes_data = get_response_dictionary(REF_THESAURUS, WORD, Thesaurus_key)
    if thes_data:
        synonyms_list = extract_synonyms(thes_data, SYNONYMS)
        antonyms_list = extract_synonyms(thes_data, ANTONYMS)
    else:
        synonyms_list = NONE_RESULT
        antonyms_list = NONE_RESULT

except Exception as e:
    synonyms_list = NONE_RESULT
    antonyms_list = NONE_RESULT
    print(f"An error occurred: {e}")

print(synonyms_list)
print(antonyms_list)

definition_list = list_manager(data, DEFINITION_KEY)
type_of_speech_list = list_manager(data, TYPE_OF_SPEECH_KEY)
etymology_list = et_list_manager(data, ETYMOLOGY_KEY)
date_list = list_manager(data, DATE_KEY)



class WordVariant:
    def __init__(self, definition, type_of_speech, date, etymology, synonyms=None, antonyms=None):
        self.definition = definition
        self.type_of_speech = type_of_speech
        self.date = date
        self.etymology = etymology
        self.synonyms = synonyms
        self.antonyms = antonyms


def create_word_variants(definitions, types_of_speech, dates, etymologies, synonyms, antonyms):
    return [
        WordVariant(definition, type_of_speech, date, etymology, synonyms, antonyms)
        for definition, type_of_speech, date, etymology, synonyms, antonyms in zip(definitions, types_of_speech, dates, etymologies, synonyms, antonyms)
    ]
list_of_word_variants = create_word_variants(definition_list, type_of_speech_list, date_list, etymology_list, synonyms_list, antonyms_list)

# Text to List Converter
def split_text(text):
    return text.split(',')

formated_definition = split_text(list_of_word_variants[0].definition)

def first_definition():
    for t in range (len(formated_definition)):
        print(formated_definition[t])

    print(
        f'Date first used: {list_of_word_variants[0].date}')

first_definition()
