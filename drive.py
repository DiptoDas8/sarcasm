# from text_sarcasm import text_sarcasm
from image_to_text import extract
import os

"""
text_sarcasm_score = text_sarcasm('thank you!')
print(text_sarcasm_score)
"""

extract(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'test.jpg'), lang="eng")
