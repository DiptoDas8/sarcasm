import os
from PIL import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract'

def extract(image_file, lang):
    print(image_file)
    im = Image.open(image_file)
    text = pytesseract.image_to_string(im, lang=lang)
    print(text)


# extract('test.png')
