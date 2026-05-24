import os
import re
import json
import subprocess
from wotd import main as run_wotd

FUTURE_WORDS_PATH = os.path.join("other_files", "FUTURE WOTD.txt")
GIT_PATH = os.getenv('GIT_PATH', r"C:\Program Files\Git\bin\git.exe")

def run_git_command(args):
    try:
        # Use 'git' directly if GIT_PATH is not absolute, otherwise use the full path
        cmd = [GIT_PATH] if os.path.isabs(GIT_PATH) else ["git"]
        result = subprocess.run(cmd + args, capture_output=True, text=True, check=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Git error: {e.stderr}")

def git_push_changes(word):
    print(f"Pushing changes for word: {word}")
    run_git_command(["add", "txt_files/*"])
    run_git_command(["add", "Thesaurus/*"])
    run_git_command(["add", "other_files/*"])
    run_git_command(["add", "index.html"])
    run_git_command(["commit", "-m", f"Automated update: {word}", "--trailer", "Co-authored-by: Junie <junie@jetbrains.com>"])
    run_git_command(["push", "origin", "main"]) # Assuming main branch, could detect if needed

def get_next_word():
    if not os.path.exists(FUTURE_WORDS_PATH):
        print(f"File not found: {FUTURE_WORDS_PATH}")
        return None

    with open(FUTURE_WORDS_PATH, "r", encoding="utf-8") as f:
        content = f.read().strip()

    if not content:
        print("FUTURE WOTD.txt is empty.")
        return None

    # Try to parse as the specific format seen in the file
    # It looks like: Future WOTD = [ "word1", "word2" ... ] Affable
    
    # Extract words inside quotes
    words = re.findall(r'"([^"]+)"', content)
    
    # Also find words that are not in quotes but are plain words at the end or on new lines
    # Only if they aren't part of the 'Future WOTD = [' structure
    if "]" in content:
        after_bracket = content.split("]")[-1].strip()
        extra_words = [w.strip() for w in after_bracket.split() if w.strip()]
        words.extend(extra_words)
    
    # If no words in quotes, maybe it's just a list of words?
    if not words:
        words = [line.strip() for line in content.splitlines() if line.strip()]

    if not words:
        print("No words found in FUTURE WOTD.txt")
        return None

    next_word = words[0]
    remaining_words = words[1:]
    
    # Update the file by removing the used word
    # If it was originally a Python-like list, we'll keep that format.
    with open(FUTURE_WORDS_PATH, "w", encoding="utf-8") as f:
        f.write("Future WOTD = [\n")
        for i, w in enumerate(remaining_words):
            comma = "," if i < len(remaining_words) - 1 else ""
            f.write(f'"{w}"{comma}\n')
        f.write("]")

    return next_word

if __name__ == "__main__":
    word = get_next_word()
    if word:
        print(f"Selected next Word of the Day: {word}")
        run_wotd(word)
        git_push_changes(word)
    else:
        print("No word to process.")
