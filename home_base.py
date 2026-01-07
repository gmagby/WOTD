import tkinter as tk
import wotd
from wotd import WordVariant, list_of_word_variants



class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Word of the Day")
        self.root.geometry("800x500")
        self.setup_ui()

    def setup_ui(self):
        label_word = tk.Label(self.root, text=wotd.WORD, pady=10, padx=10, bg="purple", fg="white")
        label_word.pack()
        self.front_page()
        self.root.mainloop()

    def elements(self,num):
        label_definition = tk.Label(self.root, text=list_of_word_variants[num].definition)
        label_definition.bind('<Configure>', lambda e: label_definition.config(wraplength=label_definition.winfo_width()))
        label_definition.pack()

        label_type_of_speach = tk.Label(self.root, text=list_of_word_variants[num].type_of_speech)
        label_type_of_speach.bind('<Configure>',lambda e: label_type_of_speach.config(wraplength=label_type_of_speach.winfo_width()))
        label_type_of_speach.pack()

        label_first_date = tk.Label(self.root, text=list_of_word_variants[num].date)
        label_first_date.bind('<Configure>',lambda e: label_first_date.config(wraplength=label_first_date.winfo_width()))
        label_first_date.pack()

        label_etymology = tk.Label(self.root, text=list_of_word_variants[num].etymology)
        label_etymology.bind('<Configure>', lambda e: label_etymology.config(wraplength=label_etymology.winfo_width()))
        label_etymology.pack()


    def front_page(self):
        for t in range (4):
            self.elements(t)
        pass


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
