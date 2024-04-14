from flask import current_app
import os
from PIL import Image
import unicodedata
import string

def _convert_to_alphanumeric_lowercase(input_string):
    # Remove punctuation and convert to lowercase
    table = str.maketrans('', '', string.punctuation)
    alphanumeric_lowercase = input_string.translate(table).lower()

    # Normalize Unicode characters and replace spaces with underscores
    alphanumeric_lowercase = '_'.join(unicodedata.normalize('NFD', char).encode('ascii', 'ignore').decode('utf-8')
                                      for char in alphanumeric_lowercase.split())

    return alphanumeric_lowercase


# Function to convert image to PNG format
def _convert_to_png_and_save(filename, image_file):
    # Converting all recipe into png and saving them in the static folder
    with Image.open(image_file) as img:
        png_image = filename.split('.')[0] + '.png'
        png_image_path = os.path.join(current_app.root_path, 'static', 'img', 'img_recipe', png_image)
        img.save(png_image_path, 'PNG')
        return f'/static/img/img_recipe/{png_image}'

def _normalize_name_string(input_string):
    if not input_string:
        return input_string
    else:
        # Remove leading and trailing spaces, capitalize first letter
        return input_string.strip().capitalize()