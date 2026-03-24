import streamlit as st
from wotd import previous_WOTD
from wotd import WORD
from wotd import list_of_word_variants
from PIL import Image
import os
import re

favored = 0
num = len(list_of_word_variants)


def top_of_page():
    st.header("Word of the Day", divider="rainbow")
    st.title(WORD)
    st.markdown(f'**{list_of_word_variants[favored].type_of_speech}**')


# Text to List Converter
def format_text(text):
    text = text.split('^')
    return text

def base_def(word):
    st.markdown()

def check_for_no_data(text):
    if text != 'No info available':
        return True

    else:
        return False

def display_photo():
    today_photo = pull_specific_photo(r"Photos", f"{WORD}.jpg")
    st.image(today_photo)

def first_definition():
    formated_definition = format_text(list_of_word_variants[favored].definition)
    for t in range(len(formated_definition)):
        st.write(
            f'{formated_definition[t]}')
    st.markdown("")

def switch_buttons():
    st.markdown(f' Date first used: {list_of_word_variants[favored].date}.')
    if check_for_no_data(list_of_word_variants[favored].etymology):
        if st.button("Etymology"):
            for t in range(num):
                st.markdown(list_of_word_variants[t].etymology)
    else:
        pass

    if check_for_no_data(list_of_word_variants[favored].synonyms):
        if st.button('Thesaurus'):
            st.markdown("Synonyms:")
            st.markdown(list_of_word_variants[favored].synonyms)
            st.markdown("Antonyms:")
            st.markdown(list_of_word_variants[favored].antonyms)
        else:
            pass

def more_definitions():
    for t in range(num - 1):
        if check_for_no_data(list_of_word_variants[t].definition):
            pass

        st.header(WORD, divider="rainbow")
        st.markdown(
            f'{format_text(list_of_word_variants[t + 1].definition)}')
        st.markdown(
            f'**{list_of_word_variants[t + 1].type_of_speech}**')
        st.markdown(f'Etymology: {format_text(list_of_word_variants[t + 1].etymology)}')
        st.markdown(
            f'Date first used: {list_of_word_variants[t + 1].date}')
        if check_for_no_data(list_of_word_variants[t + 1].synonyms):
            st.markdown("Synonyms:")
            st.markdown(list_of_word_variants[t + 1].synonyms)
            st.markdown("Antonyms:")
            st.markdown(list_of_word_variants[t + 1].antonyms)
        # st.markdown(f'Antonyms: None found')

def display_instructions():
    st.sidebar.markdown('Instructions on how to make WOTD into a widget on your homescreen.')
    st.sidebar.markdown(
        'Safari Instructions: [Here](https://docs.google.com/presentation/d/1ICISEQxe1UuQ7Z3xBA9gU8fPLrTMFCbIZSy9M_au0HY/edit?usp=sharing)')
    st.sidebar.markdown(
        'Chrome instructions: [Here](https://docs.google.com/presentation/d/1B5HWIi_X_8wNhbKWEcTfKhnWs4DfLsemZEEiym612Y8/edit?usp=sharing)')

def pull_specific_photo(folder_path, photo_name):
    # Default case (equivalent to else)
    photo_path = os.path.join(folder_path, photo_name)
    if os.path.exists(photo_path):
        return Image.open(photo_path)
    else:
        raise FileNotFoundError(f"The photo '{photo_name}' does not exist in the specified folder.")


def sidebar():
    st.sidebar.title(WORD)
    st.sidebar.markdown(f'**{list_of_word_variants[favored].type_of_speech}**')

    if check_for_no_data(list_of_word_variants[favored].etymology):
        if st.sidebar.button("Etymology"):
            for t in range(num):
                st.sidebar.markdown(list_of_word_variants[t].etymology)
    else:
        pass


    if check_for_no_data(list_of_word_variants[favored].synonyms):
        if st.sidebar.button('Thesaurus'):
            st.sidebar.markdown("Synonyms:")
            st.sidebar.markdown(list_of_word_variants[favored].synonyms)
            st.sidebar.markdown("Antonyms:")
            st.sidebar.markdown(list_of_word_variants[favored].antonyms)
        else:
            pass
    url = f'https://www.merriam-webster.com/dictionary/{WORD}'
    st.sidebar.link_button("Merriam-Webster", url)

    if st.sidebar.button("Instructions to add WOTD to your homescreen"):
        display_instructions()

    # if st.sidebar.button('Previous words of the day.'):
    #     for t in range(len(previous_WOTD)):
    #         st.sidebar.markdown(previous_WOTD[t])

def guide_func():
    top_of_page()
    first_definition()
    # switch_buttons()
    sidebar()
    display_photo()
    if num > 1:
        if check_for_no_data(list_of_word_variants[1].definition):
            if st.button("All Definitions"):
                more_definitions()
        else:
            pass
guide_func()


if __name__ == "__main__":
    guide_func()
