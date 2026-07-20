import streamlit as st

from wotd import previous_WOTD
from wotd import WORD
from wotd import NONE_RESULT
from PIL import Image
from wotd import create_variants
import os
# from st_copy_to_clipboard import st_copy_to_clipboard

favored = 0


def create_new_variants(chosen_word):
    list_of_word_variants = create_variants(chosen_word)
    print(list_of_word_variants)
    return list_of_word_variants

def main(chosen_word):
    new_word_variants_list = create_new_variants(chosen_word)
    top_of_page(chosen_word, new_word_variants_list)
    first_definition(chosen_word, new_word_variants_list)
    verify_more_definitions(chosen_word, new_word_variants_list)
    sidebar(chosen_word, new_word_variants_list)
    photo = display_photo(chosen_word)
    if photo:
        st.image(photo)


def verify_more_definitions(chosen_word, variant):
    num = len(variant)
    if num > 1:
        if check_for_data(variant[1].definition):
            if st.button("All Definitions"):
                more_definitions(chosen_word, variant)
        else:
            pass
    else:
        pass

# def share_button():
#     if st.button("Share the Word of the Day"):
#         st_copy_to_clipboard("https://learnnewword.streamlit.app/")

def top_of_page(chosen_word, variant):
    st.header("Word of the Day", divider="rainbow")
    st.title(chosen_word)
    pronunciation = variant[favored].pronunciation
    if pronunciation:
        st.text(fr"{pronunciation}")
    st.markdown(f'**{variant[favored].type_of_speech}**')

# Text to List Converter
def format_text(text):
    text = text.split('^')
    return text

# def check_for_data(text):
#     if text:
#         return True
#     if text == []:
#         return False
#     else:
#         return False

def check_for_data(text):
    return bool(text) and text != []

def pull_specific_photo(folder_path, photo_name):
    # Default case (equivalent to else)
    photo_path = os.path.join(folder_path, photo_name)
    if os.path.exists(photo_path):
        return Image.open(photo_path)
    else:
        raise FileNotFoundError(f"The photo '{photo_name}' does not exist in the specified folder.")

def display_photo(chosen_word):
    try:
        today_photo = pull_specific_photo(r"Photos", f"{chosen_word}.jpg")
        return today_photo
    except FileNotFoundError:
        return None

def first_definition(chosen_word, variant):
    formated_definition = format_text(variant[favored].definition)
    for t in range(len(formated_definition)):
        st.write(
            f'{formated_definition[t]}')

def more_definitions(chosen_word, variant):
    for t in range(1, len(variant)):  # Start from 1 to avoid accessing index 0
        if check_for_data(variant[t].definition):
            st.divider()
            st.markdown(f'**{variant[t].type_of_speech}**')
            
            # definitions are joined with ^ in the data, but here we want to display them nicely
            formated_definition = format_text(variant[t].definition)
            for d in formated_definition:
                st.write(d)
                
            if check_for_data(variant[t].etymology) and variant[t].etymology != 'No info available':
                st.markdown(f'Etymology: {variant[t].etymology}')
            if check_for_data(variant[t].date) and variant[t].date != 'No info available':
                st.markdown(f'Date first used: {variant[t].date}')

def check_for_nyms(nym_list, text):
    if nym_list and nym_list != [NONE_RESULT]:
        st.sidebar.markdown(f"**{text}**")
        for group in nym_list:
             st.sidebar.markdown(", ".join(group))

def print_nyms(variant, iteration):
    check_for_nyms(variant[iteration].synonyms, "Synonyms:")
    check_for_nyms(variant[iteration].antonyms, "Antonyms:")


def display_instructions():
    st.sidebar.markdown('Instructions on how to make WOTD into a widget on your homescreen.')
    st.sidebar.markdown(
        'Safari Instructions: [Here](https://docs.google.com/presentation/d/1ICISEQxe1UuQ7Z3xBA9gU8fPLrTMFCbIZSy9M_au0HY/edit?usp=sharing)')
    st.sidebar.markdown(
        'Chrome instructions: [Here](https://docs.google.com/presentation/d/1B5HWIi_X_8wNhbKWEcTfKhnWs4DfLsemZEEiym612Y8/edit?usp=sharing)')



def sidebar(chosen_word, variant):
    st.sidebar.title(chosen_word)
    st.sidebar.markdown(f'**{variant[favored].type_of_speech}**')
    if check_for_data(variant[favored].etymology) and variant[favored].etymology != NONE_RESULT:
        if st.sidebar.button("Etymology"):
            for t in range(len(variant)):
                    st.sidebar.markdown(variant[t].etymology)

    if st.sidebar.button('Thesaurus'):
       print_nyms(variant, favored)

    def create_merriam_url(word):
        return f'https://www.merriam-webster.com/dictionary/{word}'

    def create_merriam_button(text, word):
        return st.sidebar.link_button(text, create_merriam_url(word))

    create_merriam_button('Merriam-Webster', chosen_word)

    if st.sidebar.button("Instructions to add WOTD to your homescreen"):
        display_instructions()

    if st.sidebar.button("Share the Word of the Day"):
        st.sidebar.code("https://learnnewword.streamlit.app/")

    if st.sidebar.button('Previous words of the day.'):
        # Using a set to keep track of words we've already displayed to avoid duplicates
        seen_words = set()
        for t in reversed(previous_WOTD):
            if t not in seen_words:
                create_merriam_button(t, t)
                seen_words.add(t)


if __name__ == "__main__":
    main(WORD)