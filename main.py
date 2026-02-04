import streamlit as st
import wotd
from wotd import list_of_word_variants
from PIL import Image

favored = 0
num = len(list_of_word_variants)

st.header("Word of the Day", divider="rainbow")
st.title(wotd.WORD)

st.markdown(f'**{list_of_word_variants[favored].type_of_speech}**')


# Text to List Converter
def split_text(text):
    return text.split(',')

formated_definition = split_text(list_of_word_variants[favored].definition)


def first_definition():
    for t in range (len(formated_definition)):
        st.markdown(formated_definition[t])
    st.markdown(
        f'Date first used: {list_of_word_variants[favored].date}')



def more_definitions():
    for t in range (num-1):
        if list_of_word_variants[t].definition == 'No info available':
            pass

        else:
            st.markdown(
                f'{list_of_word_variants[t+1].definition}')
            st.markdown(
                f'**{list_of_word_variants[t+1].type_of_speech}**')
            st.markdown(
                f'Date first used: {list_of_word_variants[t+1].date}')
            st.markdown(f'Synonyms: {list_of_word_variants[t+1].synonyms}')
            st.markdown(f'Antonyms: {list_of_word_variants[t+1].antonyms}')
            # st.markdown(
            #     f'{list_of_word_variants[t].etymology}')
            st.header("", divider="rainbow")



def instructions_app():
    st.markdown(
        '''Instructions on how to make WOTD into a widget on your homescreen.''')
    st.markdown('''
        Safari Instructions:
        (https://docs.google.com/presentation/d/1ICISEQxe1UuQ7Z3xBA9gU8fPLrTMFCbIZSy9M_au0HY/edit?usp=sharing)''')
    st.markdown('''
        Chrome instructions:
        (https://docs.google.com/presentation/d/1B5HWIi_X_8wNhbKWEcTfKhnWs4DfLsemZEEiym612Y8/edit?usp=sharing)
        '''
    )

first_definition()

if st.button('Thesaurus'):
    st.markdown(list_of_word_variants[favored].synonyms)
    st.markdown(list_of_word_variants[favored].antonyms)


url = f'https://www.merriam-webster.com/dictionary/{wotd.WORD}'
st.link_button("Merriam-Webster", url)

if st.button("Instructions to add WOTD to your homescreen"):
    instructions_app()

if num > 1:
    if list_of_word_variants[1].definition == 'No info available':
        pass
    else:
        if st.button("All Definitions"):
            more_definitions()


example_img = Image.open(f'{wotd.WORD}.jpg')
st.image(example_img)
