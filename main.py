import streamlit as st
import wotd
from wotd import list_of_word_variants
from wotd import split_up_definitions
from wotd import number_of_split_def
from PIL import Image

num = len(list_of_word_variants)
FAVORED = 0

st.header("Word of the Day", divider="rainbow")
st.subheader(wotd.WORD)
st.markdown(f'**{list_of_word_variants[FAVORED].type_of_speech}**')

def more_definitions():
    for t in range (num):
        if list_of_word_variants[t].definition == 'No info available':
            pass

        else:
            st.markdown(
                f'{list_of_word_variants[t].definition}')
            st.markdown(
                f'**{list_of_word_variants[t].type_of_speech}**')
            st.markdown(
                f'Date first used: **{list_of_word_variants[t].date}**')
            # st.markdown(
            #     f'{list_of_word_variants[t].etymology}')
            st.header("", divider="rainbow")


def first_definition():
    for t in range (number_of_split_def):
        st.markdown(split_up_definitions[t])

    # st.markdown(
    #     f'Type of speech: **{list_of_word_variants[FAVORED].type_of_speech}**')
    st.markdown(
        f'Date first used: **{list_of_word_variants[FAVORED].date}**')

    # st.header("",divider="green")


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

if st.button("Instructions to add WOTD to your homescreen"):
    instructions_app()

if num > 1:
    if list_of_word_variants[1].definition == 'No info available':
        pass
    else:
        if st.button("All Definitions"):
            more_definitions()
else:
    pass

example_img = Image.open(f'{wotd.WORD}.jpg')
st.image(example_img)




# st.image("https://images.unsplash.com/photo-1535930749574-1399327ce78f?q=80&w=1936&auto=format&fit=crop")
# Open 'data/report.txt' for writing ('w')
