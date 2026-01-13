import streamlit as st
import wotd
from wotd import list_of_word_variants
from PIL import Image

NUM = len(list_of_word_variants)
st.header("Word of the Day", divider="rainbow")
st.subheader(wotd.WORD)

def more_definitions():
    for t in range (NUM):
        st.markdown(
            f'{list_of_word_variants[t].definition}')
        st.markdown(
            f'Type of Speech: **{list_of_word_variants[t].type_of_speech}**')
        st.markdown(
            f'Date first used: **{list_of_word_variants[t].date}**')
        # st.markdown(
        #     f'{list_of_word_variants[t].etymology}')
        st.header("",divider="rainbow")

def first_definition():
    st.markdown(
        f'{list_of_word_variants[0].definition}')
    st.markdown(
        f'Type of speech: **{list_of_word_variants[0].type_of_speech}**')
    st.markdown(
        f'Date first used: **{list_of_word_variants[0].date}**')
    # st.markdown(
    #     f'{list_of_word_variants[0].etymology}')
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

if st.button("More Definitions"):
    more_definitions()


# st.image("https://images.unsplash.com/photo-1535930749574-1399327ce78f?q=80&w=1936&auto=format&fit=crop")
# Open 'data/report.txt' for writing ('w')


#example_img = Image.open(f'{wotd.WORD}.jpg')
# st.image(example_img)
