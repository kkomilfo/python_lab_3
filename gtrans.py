# gtrans.py
from my_package.module1 import translate, lang_detect, full_language, language_list

text = "Hello world"
iso_code = "en"
print(lang_detect(text))
print(translate(text, dest='uk'))
print(full_language(iso_code))
print(language_list(text=text))