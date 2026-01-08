import streamlit as st
import wotd
from wotd import WordVariant, list_of_word_variants

NUM = len(list_of_word_variants)
st.header("Word of the Day", divider="rainbow")
st.subheader(wotd.WORD)


st.markdown(
    f'{list_of_word_variants[0].definition}')
st.markdown(
    f'Type of speech: {list_of_word_variants[0].type_of_speech}')
st.markdown(
    f'Date first used: {list_of_word_variants[0].date}')
# st.markdown(
#     f'{list_of_word_variants[0].etymology}')

st.image("https://images.unsplash.com/photo-1535930749574-1399327ce78f?q=80&w=1936&auto=format&fit=crop")






