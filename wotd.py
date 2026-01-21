import re
import requests

WORD = 'Monochromatic'
REF_DICTIONARY = "collegiate"
REF_THESAURUS = "thesaurus"
DICTIONARY_KEY = 'f45f1248-4774-4d20-8d31-ecb2d70452e0'
Thesaurus_key = '2431331e-690c-4d83-96ac-1f4e9cb350d5'
DEFINITION_KEY = 'shortdef'
TYPE_OF_SPEECH_KEY = 'fl'
DATE_KEY = 'date'
ETYMOLOGY_KEY = 'et'
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

def cleaner(clean_text):
    clean_text = str(clean_text)
    clean_text = re.sub(r"[()\#[/@<>{}=~|?]", '', clean_text)
    # clean_text = re.sub(r"[^a-zA-Z0-9:]", " ", clean_text)
    # clean_text = re.sub(r"\s+", " ", clean_text).strip()  # Remove extra spaces
    clean_text = re.sub(r"dst1", '', clean_text)
    clean_text = re.sub(r",", ', \n', clean_text)
    clean_text = re.sub(r"]", '\n', clean_text)
    clean_text = re.sub(r"ds1a", '\n', clean_text)
    return clean_text


def list_manager(data, syntax):
    return [
        cleaner(item.get(syntax, NONE_RESULT)) if item.get(syntax) else NONE_RESULT
        for item in data
    ]


data = get_response_dictionary(REF_DICTIONARY, WORD, DICTIONARY_KEY)


definition_list = list_manager(data, DEFINITION_KEY)
type_of_speech_list = list_manager(data, TYPE_OF_SPEECH_KEY)
etymology_list = list_manager(data, ETYMOLOGY_KEY)
date_list = list_manager(data, DATE_KEY)


class WordVariant:
    def __init__(self, definition, type_of_speech, date, etymology):
        self.definition = definition
        self.type_of_speech = type_of_speech
        self.date = date
        self.etymology = etymology


def create_word_variants(definitions, types_of_speech, dates, etymologies):
    return [
        WordVariant(definition, type_of_speech, date, etymology)
        for definition, type_of_speech, date, etymology in zip(definitions, types_of_speech, dates, etymologies)
    ]



list_of_word_variants = create_word_variants(definition_list, type_of_speech_list, date_list, etymology_list)

def split_up(number,key):
    deep_list = []
    for t in data[number][key]:
        deep_list.append(t)
    return deep_list

split_up_definitions = split_up(0,DEFINITION_KEY)
number_of_split_def = len(split_up_definitions)
print(split_up_definitions)
