import re
def cleaner(clean_text, sharp=None):
    from wotd import WORD
    print(f'Old:          {clean_text}')
    clean_text = str(clean_text)
    def etymology_cleaner(clean_text):
        # Remove Merriam-Webster API tokens/tags
        # Pattern matches {tag|data} or {tag} or {/tag}
        clean_text = re.sub(r'\{[a-z_]+(\|[^}]*)?\}', '', clean_text)
        clean_text = re.sub(r'\{/[a-z_]+\}', '', clean_text)
        # Specific patterns and cleanup
        clean_text = re.sub(r"'text', ", '', clean_text)
        clean_text = re.sub(r']]', '', clean_text)
        clean_text = re.sub(r":2", '', clean_text)
        clean_text = re.sub(r":1", '', clean_text)
        clean_text = re.sub(r"-ia", '', clean_text)
        clean_text = re.sub(r"et_snote',", '', clean_text)
        clean_text = re.sub(r"et_snote", '', clean_text)
        clean_text = re.sub(r"'t',", '', clean_text)
        clean_text = re.sub(r"', '", ', ^', clean_text)
        clean_text = re.sub(r"andor", 'and/or', clean_text)
        # Remove specific artifacts
        clean_text = re.sub(r"ǵehinf2infr-", r'', clean_text)
        # Double WORD occurrences
        clean_text = re.sub(r"-ed-ed", f'-ed', clean_text)
        clean_text = re.sub(r"addleaddle", r'addle', clean_text)
        
        return clean_text
    def definition_cleaner(clean_text):
        clean_text = re.sub(r"', '", ', ^', clean_text)
        return clean_text
    def date_cleaner(clean_text):
        # Remove Merriam-Webster API tokens/tags like {ds||1|a|}
        clean_text = re.sub(r'\{[a-z_]*(\|[^}]*)?\}', '', clean_text)
        clean_text = re.sub(r'\{/[a-z_]+\}', '', clean_text)
        
        # Cleanup file extensions if they leaked in
        clean_text = re.sub(r'\.(jpg|jpeg|png|gif|webp|avif|mp4)', '', clean_text)
        
        return clean_text
    def file_cleaner(clean_text):
        clean_text = re.sub(r".txt.txt", ".txt", clean_text)
        return clean_text
    def base_cleaner(clean_text):
        # Remove Merriam-Webster API tokens/tags
        clean_text = re.sub(r'\{[a-z_]*(\|[^}]*)?\}', '', clean_text)
        clean_text = re.sub(r'\{/[a-z_]+\}', '', clean_text)
        
        clean_text = re.sub(r"\s+", " ", clean_text).strip()  # Remove extra spaces
        clean_text = re.sub(r"[\#[/@<>{}=~|?*\]]", '', clean_text) # Removed '*' via [] and added ']'
        clean_text = re.sub(r" u ", " 'u' ", clean_text)
        clean_text = re.sub(r"'", '', clean_text)
        clean_text = re.sub(r"\s+", " ", clean_text).strip()
        return clean_text
    if sharp == 1:  # Definition cleaner
        clean_text = base_cleaner(definition_cleaner(clean_text))
    elif sharp == 2:  # Date cleaner
        clean_text = date_cleaner(base_cleaner(clean_text))
    elif sharp == 3:  # Etymology cleaner
        clean_text = base_cleaner(etymology_cleaner(clean_text))
    elif sharp == 4:
        clean_text = base_cleaner(clean_text)
    elif sharp == 5:
        clean_text = file_cleaner(clean_text)
    clean_text = re.sub(r"\s+", " ", clean_text).strip()
    clean_text = str(clean_text)
    print(f'Clean:        {clean_text}')
    print(" ")
    return clean_text

def list_of_prev_wotd_cleaner(clean_text):
    # print(clean_text)
    clean_text = str(clean_text)
    clean_text = re.sub(r'.jpg', '', clean_text)
    clean_text = re.sub(r'.jpeg', '', clean_text)
    clean_text = re.sub(r'.png', '', clean_text)
    clean_text = re.sub(r'.gif', '', clean_text)
    clean_text = re.sub(r'.webp', '', clean_text)
    clean_text = re.sub(r'.avif', '', clean_text)
    clean_text = re.sub(r'.mp4', '', clean_text)
    clean_text = re.sub(r"[\#[/@<>{}=~|?]", '', clean_text)
    clean_text = re.sub(r"]", '', clean_text)
    clean_text = re.sub(r"'", '', clean_text)
    clean_text = re.sub(r"2", '', clean_text)
    clean_text = clean_text.lower()
    clean_list = clean_text.split(", ")
    # print(clean_list)
    print(len(clean_list))
    # print('')
    return clean_list