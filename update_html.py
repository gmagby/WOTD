import os
import wotd

def update_index_html(word):
    path = 'index.html'
    if not os.path.exists(path):
        print(f"Error: {path} not found.")
        return

    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the word title line and replace the word
    # <h2 id="word" class="word-title">Aureole</h2>
    import re
    new_content = re.sub(r'(<h2 id="word" class="word-title">)(.*?)(</h2>)', fr'\1{word}\3', content)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"Successfully updated index.html for word: {word}")

if __name__ == "__main__":
    update_index_html(wotd.WORD)
