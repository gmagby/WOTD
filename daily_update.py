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
    
    # Check for file existence before adding to avoid git errors
    files_to_add = [
        "main.py",
        "wotd.py",
        f"txt_files/{word}.txt",
        f"Thesaurus/{word}.txt",
        f"Photos/{word}.jpg",
        f"Photos/{word}.png",
        "other_files/*",
        "index.html"
    ]
    
    for file_pattern in files_to_add:
        run_git_command(["add", file_pattern])

    # Check if there are changes to commit
    try:
        cmd = [GIT_PATH] if os.path.isabs(GIT_PATH) else ["git"]
        status = subprocess.run(cmd + ["status", "--porcelain"], capture_output=True, text=True, check=True)
        if not status.stdout.strip():
            print("No changes to commit.")
    except:
        pass

    run_git_command(["commit", "-m", f"Automated update: {word}"])
    
    print("Attempting to push to GitHub...")
    success = False
    if os.getenv('GITHUB_TOKEN'):
        remote_url = f"https://x-access-token:{os.getenv('GITHUB_TOKEN')}@github.com/{os.getenv('GITHUB_REPOSITORY')}.git"
        success = run_git_command(["push", remote_url, "HEAD:main"])
    else:
        success = run_git_command(["push", "origin", "main"])
    
    if success:
        print("Successfully pushed to GitHub.")
    else:
        print("Failed to push to GitHub.")

def get_next_word():
    if not os.path.exists(FUTURE_WORDS_PATH):
        print(f"File not found: {FUTURE_WORDS_PATH}")
        return None

    with open(FUTURE_WORDS_PATH, "r", encoding="utf-8") as f:
        content = f.read().strip()

    if not content:
        print("FUTURE WOTD.txt is empty.")
        return None

    # Try to parse words from the file
    # Handles: Future WOTD = [ "'word1'", "word2" ] or just a list of words
    
    # First, find anything that looks like a word in quotes (single or double)
    words = re.findall(r'["\']([^"\']+)["\']', content)
    
    # If no quotes found, try to split by whitespace/newlines, excluding the structural parts
    if not words:
        # Remove structural parts if they exist
        clean_content = content.replace("Future WOTD = [", "").replace("]", "").replace(",", "")
        words = [w.strip() for w in clean_content.split() if w.strip()]

    if not words:
        print("No words found in FUTURE WOTD.txt")
        return None

    # Clean the word (strip any lingering quotes or whitespace)
    next_word = words[0].strip("'\" ")
    
    if not next_word or next_word == '[': # Extra safety
         if len(words) > 1:
             next_word = words[1].strip("'\" ")
         else:
             print("Could not extract a valid word.")
             return None

    # Remove all instances of the chosen word from the list for the update
    remaining_words = [w.strip("'\" ") for w in words if w.strip("'\" ").lower() != next_word.lower()]
    
    # Update the file by removing the used word
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
