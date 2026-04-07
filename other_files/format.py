import os
from PIL import Image

# Path to your folder containing images
folder_path = r"C:\Users\gabem\OneDrive\Desktop\WOTD images"

# Loop through all files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith((".png", ".jpeg", ".bmp", ".gif", ".tiff", ".avif", ".gif", ".webp")):
        # Define the full file paths
        img_path = os.path.join(folder_path, filename)

        # Open image
        with Image.open(img_path) as img:
            # Convert image to RGB (required for JPG)
            rgb_im = img.convert('RGB')

            # Create new filename with .jpg extension
            file_name_no_ext = os.path.splitext(filename)[0]
            new_filename = file_name_no_ext + ".jpg"
            new_img_path = os.path.join(folder_path, new_filename)

            # Save as JPEG
            rgb_im.save(new_img_path, "JPEG", quality=95)
            print(f"Converted: {filename} to {new_filename}")

print("All images converted to JPG.")