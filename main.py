import streamlit as st
# import wotd
# from wotd import list_of_word_variants
from PIL import Image

favored = 0
# num = len(list_of_word_variants)

st.header("Word of the Day", divider="rainbow")
# st.title(wotd.WORD)
st.title('Agentic')
# st.markdown(f'**{list_of_word_variants[favored].type_of_speech}**')
st.markdown("adjective")

# Text to List Converter
def split_text(text):
    return text.split(',')

# formated_definition = split_text(list_of_word_variants[favored].definition)


def first_definition():
    # for t in range (len(formated_definition)):
    #     st.markdown(formated_definition[t])

    st.markdown('Able to accomplish results with autonomy, used especially in reference to artificial intelligence')

    st.markdown('Agentic describes someone or something that is capable of achieving outcomes independently (“functioning like an agent”) or possessing such ability, means, or power (“having agency"). It is especially used with a type of artificial intelligence (AI), often referred to as an AI agent, designed to execute complex tasks autonomously or with little human involvement. In social sciences, agentic is more specifically used to describe people’s self-assertive behaviors or actions directed towards individual accomplishment, status, and independence.')

    # st.markdown(
    #     f'Date first used: {list_of_word_variants[favored].date}')
    st.markdown('Date first used: 2024')
    st.subheader('Prediction')
    st.markdown('Not officially in the dictionary as of 2026. Will become a household word within 2 years.')


# def more_definitions():
#     for t in range (num):
#         if list_of_word_variants[t].definition == 'No info available':
#             pass
#
#         else:
#             st.markdown(
#                 f'{list_of_word_variants[t].definition}')
#             st.markdown(
#                 f'**{list_of_word_variants[t].type_of_speech}**')
#             st.markdown(
#                 f'Date first used: {list_of_word_variants[t].date}')
#             # st.markdown(
#             #     f'{list_of_word_variants[t].etymology}')
#             st.header("", divider="rainbow")



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

# if st.button("Instructions to add WOTD to your homescreen"):
#     instructions_app()
#
# if num > 1:
#     if list_of_word_variants[1].definition == 'No info available':
#         pass
#     else:
#         if st.button("All Definitions"):
#             more_definitions()
# else:
#     pass

# example_img = Image.open(f'{wotd.WORD}.jpg')
example_img = Image.open(f'Agentic.jpg')
st.image(example_img)

# st.subheader("Click below to learn how others have used this word.")

url = "https://www.merriam-webster.com/slang/agentic"
st.link_button("Merriam-Webster", url)




# st.image("https://images.unsplash.com/photo-1535930749574-1399327ce78f?q=80&w=1936&auto=format&fit=crop")
# Open 'data/report.txt' for writing ('w')
