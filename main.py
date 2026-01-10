import streamlit as st
import wotd
from wotd import WordVariant, list_of_word_variants
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

first_definition()

# if st.button("More Definitions"):
#     more_definitions()


# st.image("https://images.unsplash.com/photo-1535930749574-1399327ce78f?q=80&w=1936&auto=format&fit=crop")
# Open 'data/report.txt' for writing ('w')


example_img = Image.open(f'{wotd.WORD}.jpg')
st.image(example_img)











