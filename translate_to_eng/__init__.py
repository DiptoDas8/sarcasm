from googletrans import Translator
from goslate import Goslate

def translate_to_eng(src_text):
    translator = Translator()
    ret = translator.translate(src_text)
    print('text: ', ret.text)
    # translator = Goslate()
    # ret = translator.translate(src_text, 'en')
    # print('text: ', ret.decode("utf-8"))
