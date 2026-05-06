from wotd import save_new_data
FUTURE_WOTD = y

def add_new_word(new_word):
    future_word_list =
    if chosen_word in previous_WOTD:
        print("Word already added")
        pass
    else:
        previous_WOTD.append(chosen_word)  # Use chosen_word instead of WORD
        save_new_data(ARCHIVE_PATH, previous_WOTD)

def add_word_to_future_words_of_the_day():

    new_word = input("what word would you like to add? ")
