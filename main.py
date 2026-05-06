import streamlit as st
from wotd import previous_WOTD
from wotd import WORD
from PIL import Image
from wotd import create_variants
import os
# from st_copy_to_clipboard import st_copy_to_clipboard

def create_new_variants(chosen_word):
    list_of_word_variants = create_variants(chosen_word)
    print(list_of_word_variants)
    return list_of_word_variants

favored = 0

def main(chosen_word):
    new_word_variants_list = create_new_variants(chosen_word)
    top_of_page(chosen_word, new_word_variants_list)
    first_definition(chosen_word, new_word_variants_list)
    verify_more_definitions(chosen_word, new_word_variants_list)
    sidebar(chosen_word, new_word_variants_list)
    st.image(display_photo(chosen_word))


def verify_more_definitions(chosen_word, variant):
    num = len(variant)
    if num > 1:
        if check_for_no_data(variant[1].definition):
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
    st.text(fr"{variant[favored].pronunciation}")
    st.markdown(f'**{variant[favored].type_of_speech}**')

# Text to List Converter
def format_text(text):
    text = text.split('^')
    return text

def check_for_no_data(text):
    if text != 'No info available':
        return True

    else:
        return False

def pull_specific_photo(folder_path, photo_name):
    # Default case (equivalent to else)
    photo_path = os.path.join(folder_path, photo_name)
    if os.path.exists(photo_path):
        return Image.open(photo_path)
    else:
        raise FileNotFoundError(f"The photo '{photo_name}' does not exist in the specified folder.")

def display_photo(chosen_word):
    today_photo = pull_specific_photo(r"Photos", f"{chosen_word}.jpg")
    return today_photo

def first_definition(chosen_word, variant):
    formated_definition = format_text(variant[favored].definition)
    for t in range(len(formated_definition)):
        st.write(
            f'{formated_definition[t]}')

def more_definitions(chosen_word, variant):
    for t in range(1, len(variant)):  # Start from 1 to avoid accessing index 0
        if check_for_no_data(variant[t].definition):
            st.header(chosen_word, divider="rainbow")
            st.markdown(f'{format_text(variant[t].definition)}')
            st.markdown(f'**{variant[t].type_of_speech}**')
            st.markdown(f'Etymology: {format_text(variant[t].etymology)}')
            st.markdown(f'Date first used: {variant[t].date}')
            if check_for_no_data(variant[t].synonyms):
                st.markdown("Synonyms:")
                st.markdown(variant[t].synonyms)
                st.markdown("Antonyms:")
                st.markdown(variant[t].antonyms)

def display_instructions():
    st.sidebar.markdown('Instructions on how to make WOTD into a widget on your homescreen.')
    st.sidebar.markdown(
        'Safari Instructions: [Here](https://docs.google.com/presentation/d/1ICISEQxe1UuQ7Z3xBA9gU8fPLrTMFCbIZSy9M_au0HY/edit?usp=sharing)')
    st.sidebar.markdown(
        'Chrome instructions: [Here](https://docs.google.com/presentation/d/1B5HWIi_X_8wNhbKWEcTfKhnWs4DfLsemZEEiym612Y8/edit?usp=sharing)')

def sidebar(chosen_word, variant):
    st.sidebar.title(chosen_word)
    st.sidebar.markdown(f'**{variant[favored].type_of_speech}**')

    if check_for_no_data(variant[favored].etymology):
        if st.sidebar.button("Etymology"):
            for t in range(len(variant)):
                st.sidebar.markdown(variant[favored].etymology)
    else:
        pass

    if check_for_no_data(variant[favored].synonyms[0]):
        if st.sidebar.button('Thesaurus'):
            st.sidebar.markdown("Synonyms:")
            st.sidebar.markdown(f", ".join(variant[favored].synonyms))
            st.sidebar.markdown("Antonyms:")
            st.sidebar.markdown(variant[favored].antonyms[1:-1])
    else:
        pass

    def create_merriam_url(chosen_word):
        url = f'https://www.merriam-webster.com/dictionary/{chosen_word}'
        return url

    def create_merriam_button(text, chosen_word):
        button = st.sidebar.link_button(f'{text}', create_merriam_url(chosen_word))
        return button

    create_merriam_button('Merriam-Webster', WORD)

    if st.sidebar.button("Instructions to add WOTD to your homescreen"):
        display_instructions()

    if st.sidebar.button("Share the Word of the Day"):
        st.sidebar.markdown(
            '[Hold to copy WOTD link](https://learnnewword.streamlit.app/)')

    if st.sidebar.button('Previous words of the day.'):
        previous_WOTD.sort()
        for t in previous_WOTD:
            create_merriam_button(t, t)



if __name__ == "__main__":
    main(WORD)