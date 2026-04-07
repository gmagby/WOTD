import re

def cleaner(clean_text, sharp=None):
    print(f'Old:          {clean_text}')
    clean_text = str(clean_text)
    def etymology_cleaner(clean_text):
        clean_text = re.sub(r"dx_ety}", '', clean_text)
        clean_text = re.sub(r"mat}", '', clean_text)
        clean_text = re.sub(r"bc}", '', clean_text)
        clean_text = re.sub(r"ma}", '', clean_text)
        clean_text = re.sub(r"dx}", '', clean_text)
        clean_text = re.sub(r"dxt", '', clean_text)
        clean_text = re.sub(r'it}', '', clean_text)
        clean_text = re.sub(r"'text', ", '', clean_text)
        clean_text = re.sub(r']]', '', clean_text)
        clean_text = re.sub(r"et_link", '', clean_text)
        clean_text = re.sub(r":2", '', clean_text)
        clean_text = re.sub(r":1", '', clean_text)
        clean_text = re.sub(r"-ia", '', clean_text)
        clean_text = re.sub(r"et_snote',", '', clean_text)
        clean_text = re.sub(r"et_snote", '', clean_text)
        clean_text = re.sub(r"'t',", '', clean_text)
        clean_text = re.sub(r"', '", ', ^', clean_text)
        clean_text = re.sub(r"andor", 'and/or', clean_text)
        clean_text = re.sub(r"[\#[/@<>{}=~|?]", '', clean_text)
        clean_text = re.sub(r"]", '', clean_text)
        return clean_text
    def definition_cleaner(clean_text):
        clean_text = re.sub(r"', '", ', ^', clean_text)
        return clean_text
    def date_cleaner(clean_text):
        clean_text = re.sub(r'dst1a1', '', clean_text)
        clean_text = re.sub(r'dst2', '', clean_text)
        clean_text = re.sub(r"ds1a", '', clean_text)
        clean_text = re.sub(r"dst", '', clean_text)
        clean_text = re.sub(r"ds1b", '', clean_text)
        clean_text = re.sub(r'dst2', '', clean_text)
        clean_text = re.sub(r'ds3', '', clean_text)
        clean_text = re.sub(r'ds5', '', clean_text)
        clean_text = re.sub(r"dx_ety", '', clean_text)
        clean_text = re.sub(r"dxt", '', clean_text)
        clean_text = re.sub(r"dsi1", '', clean_text)
        clean_text = re.sub(r'ds1', '', clean_text)
        clean_text = re.sub(r'ds2', '', clean_text)
        clean_text = re.sub(r'1a', '', clean_text)
        clean_text = re.sub(r'.jpg', '', clean_text)
        clean_text = re.sub(r'.jpeg', '', clean_text)
        clean_text = re.sub(r'.png', '', clean_text)
        clean_text = re.sub(r'.gif', '', clean_text)
        return clean_text
    def file_cleaner(clean_text):
        clean_text = re.sub(r".txt.txt", ".txt", clean_text)
        return clean_text
    def base_cleaner(clean_text):
        clean_text = re.sub(r"\s+", " ", clean_text).strip()  # Remove extra spaces
        clean_text = re.sub(r"[\#[/@<>{}=~|?]", '', clean_text)
        clean_text = re.sub(r"]", '', clean_text)
        clean_text = re.sub(r" u ", " 'u' ", clean_text)
        clean_text = re.sub(r"'", '', clean_text)
        return clean_text
    if sharp == 1:  # Definition cleaner
        clean_text = base_cleaner(definition_cleaner(clean_text))
    if sharp == 2:  # Date cleaner
        clean_text = date_cleaner(base_cleaner(clean_text))
    if sharp == 3:  # Etymology cleaner
        clean_text = base_cleaner(etymology_cleaner(clean_text))
    if sharp == 4:
        base_cleaner(clean_text)
    if sharp == 5:
        file_cleaner(clean_text)
    clean_text = re.sub(r"\s+", " ", clean_text).strip()
    clean_text = str(clean_text)
    print(f'Clean:        {clean_text}')
    print(" ")
    return clean_text

def list_of_prev_wotd_cleaner(clean_text):
    print(clean_text)
    clean_text = str(clean_text)
    clean_text = re.sub(r'.jpg', '', clean_text)
    clean_text = re.sub(r'.jpeg', '', clean_text)
    clean_text = re.sub(r'.png', '', clean_text)
    clean_text = re.sub(r'.gif', '', clean_text)
    clean_text = re.sub(r'.webp', '', clean_text)
    clean_text = re.sub(r'.avif', '', clean_text)
    clean_text = re.sub(r"[\#[/@<>{}=~|?]", '', clean_text)
    clean_text = re.sub(r"]", '', clean_text)
    clean_text = re.sub(r"'", '', clean_text)
    clean_text = re.sub(r"2", '', clean_text)
    clean_text = clean_text.lower()
    clean_list = clean_text.split(", ")
    clean_list.sort(key=str.lower)
    print(clean_list)
    print('')
    print(len(clean_list))
    return clean_list