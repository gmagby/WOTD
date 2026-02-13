import streamlit as st
from wotd import WORD
from wotd import list_of_word_variants
from PIL import Image

favored = 0
num = len(list_of_word_variants)

st.header("Word of the Day", divider="rainbow")
st.title(WORD)
st.markdown(f'**{list_of_word_variants[favored].type_of_speech}**')

# Text to List Converter
def split_text(text):
    return text.split("',    '")


formated_definition = split_text(list_of_word_variants[favored].definition)
formated_etymology = split_text(list_of_word_variants[favored].etymology)


def first_definition():
    for t in range (len(formated_definition)):
        st.write(
            f'{formated_definition[t]}')

    st.markdown(
        f'**Date first used: {list_of_word_variants[favored].date}**')


def more_definitions():
    for t in range (num):
        if list_of_word_variants[t].definition == 'No info available':
            pass

        else:

            st.markdown(f'Synonyms: {list_of_word_variants[t].synonyms}')
            st.markdown(f'Antonyms: {list_of_word_variants[t].antonyms}')

            st.header(WORD, divider="rainbow")
            st.markdown(
                f'{list_of_word_variants[t+1].definition}')
            st.markdown(
                f'**{list_of_word_variants[t+1].type_of_speech}**')
            st.markdown(f'Etymology: {list_of_word_variants[t + 1].etymology}')
            st.markdown(
                f'Date first used: {list_of_word_variants[t+1].date}')
            st.markdown(f'Synonyms: {list_of_word_variants[t+1].synonyms}')
            st.markdown(f'Antonyms: {list_of_word_variants[t + 1].antonyms}')

            if list_of_word_variants[favored].etymology != 'No info available':
                for t in range(len(formated_etymology)):
                    st.markdown(formated_etymology[t+1])
    # st.header(WORD, divider="rainbow")
    # st.markdown(
    #     f'{list_of_word_variants[t].definition}')
    # st.markdown(
    #     f'**{list_of_word_variants[t].type_of_speech}**')
    # st.markdown(f'Etymology: {list_of_word_variants[t].etymology}')
    # st.markdown(
    #     f'Date first used: {list_of_word_variants[t].date}')



def instructions_app():
    st.sidebar.markdown(
        '''Instructions on how to make WOTD into a widget on your homescreen.''')
    st.sidebar.markdown('''
        Safari Instructions:
        (https://docs.google.com/presentation/d/1ICISEQxe1UuQ7Z3xBA9gU8fPLrTMFCbIZSy9M_au0HY/edit?usp=sharing)''')
    st.sidebar.markdown('''
        Chrome instructions:
        (https://docs.google.com/presentation/d/1B5HWIi_X_8wNhbKWEcTfKhnWs4DfLsemZEEiym612Y8/edit?usp=sharing)
        '''
    )

first_definition()

st.sidebar.title(WORD)
st.sidebar.markdown(f'**{list_of_word_variants[favored].type_of_speech}**')

if list_of_word_variants[favored].etymology != 'No info available':
    if st.sidebar.button("Etymology"):
        for t in range(len(formated_etymology)):
            st.sidebar.markdown(formated_etymology[t])

if st.sidebar.button('Thesaurus'):
    st.sidebar.markdown("Synonyms:")
    st.sidebar.markdown(list_of_word_variants[favored].synonyms)
    st.sidebar.markdown("Antonyms:")
    st.sidebar.markdown(list_of_word_variants[favored].antonyms)

if num > 1:
    if list_of_word_variants[1].definition == 'No info available':
        pass
    else:
        if st.button("All Definitions"):
            more_definitions()

st.button("Additional information has been added to a new menu in the top left corner.")

url = f'https://www.merriam-webster.com/dictionary/{WORD}'
st.sidebar.link_button("Merriam-Webster", url)

if st.sidebar.button("Instructions to add WOTD to your homescreen"):
    instructions_app()

# example_img = Image.open(f'{WORD}.gif')
# st.image(example_img)

example_img = Image.open(f'{WORD}.jpg')
st.image(example_img)