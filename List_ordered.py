import os
from datetime import datetime
from cleaner_file import list_of_prev_wotd_cleaner

def list_and_sort_files():
    folder_path = r'C:\Users\gabem\OneDrive\Desktop\WOTD images'
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    files_with_dates = [(f, os.path.getctime(os.path.join(folder_path, f))) for f in files]
    sorted_files = sorted(files_with_dates, key=lambda x: x[1])
    return [f[0] for f in sorted_files]

sorted_file_list = list_of_prev_wotd_cleaner(list_and_sort_files())
reverse_sorted_file_list = sorted_file_list[::-1]

