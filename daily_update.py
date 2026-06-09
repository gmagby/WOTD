import os
import re
import json
import subprocess
from wotd import main as run_wotd


FUTURE_WORDS_PATH = os.path.join("other_files", "FUTURE WOTD.txt")
GIT_PATH = os.getenv('GIT_PATH', r"C:\Program Files\Git\bin\git.exe")

def run_git_command(args):
    try:
        cmd = [GIT_PATH] if os.path.isabs(GIT_PATH) else ["git"]
        result = subprocess.run(cmd + args, capture_output=True, text=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Git error: {e.stderr}")
        return False

def git_push_changes(word):
    print(f"Pushing changes for word: {word}")
    run_git_command(["add", "main.py"])
    run_git_command(["add", "wotd.py"])
    run_git_command(["add", "txt_files/*"])
    run_git_command(["add", "Thesaurus/*"])
    run_git_command(["add", "other_files/*"])
    run_git_command(["add", "index.html"])
    run_git_command(["add", "CNAME"])

    
    # Check if there are changes to commit
    try:
        cmd = [GIT_PATH] if os.path.isabs(GIT_PATH) else ["git"]
        status = subprocess.run(cmd + ["status", "--porcelain"], capture_output=True, text=True, check=True)
        if not status.stdout.strip():
            print("No changes to commit.")
            return
    except:
        pass

    run_git_command(["commit", "-m", f"Automated update: {word}"])
    
    if os.getenv('GITHUB_TOKEN'):
        remote_url = f"https://x-access-token:{os.getenv('GITHUB_TOKEN')}@github.com/{os.getenv('GITHUB_REPOSITORY')}.git"
        run_git_command(["push", remote_url, "HEAD:main"])
    else:
        run_git_command(["push", "origin", "main"])

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
    
    # Remove all instances of the chosen word from the list
    # This ensures that if the word was accidentally duplicated, it's fully removed
    remaining_words = [w for w in words[1:] if w.lower() != next_word.lower()]
    
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
        try:
            run_wotd(word)
            git_push_changes(word)
        except Exception as e:
            print(f"Error during word processing: {e}")
            exit(1)
    else:
        print("No word to process. Is FUTURE WOTD.txt empty?")
        exit(1)
