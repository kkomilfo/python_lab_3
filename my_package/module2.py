from deep_translator import GoogleTranslator
from langdetect import detect_langs, DetectorFactory
from langdetect.lang_detect_exception import LangDetectException
import pandas as pd

DetectorFactory.seed = 0  # Для отримання стабільних результатів детекції мови

def translate(text: str, scr: str, dest: str) -> str:
    try:
        translator = GoogleTranslator(source=scr, target=dest)
        translated_text = translator.translate(text)
        return translated_text
    except Exception as e:
        return f"Translation error: {e}"

def lang_detect(text: str, set: str = "all") -> str:
    try:
        langs = list(detect_langs(text))[0]
        if set == "lang":
            return str(langs.most_common()[0][0])
        elif set == "confidence":
            return str(langs.most_common()[0][1])
        else:
            return f"probbilities: {langs}"
    except LangDetectException as e:
        return f"Language detection error: {e}"

def full_language(lang: str) -> str:
    translator = GoogleTranslator()
    languages = translator.get_supported_languages(as_dict=True)
    if lang in languages:
        return languages[lang]

    for code, name in languages.items():
        if name.lower() == lang.lower():
            return code

    return "Language code or name not found."

def language_list(out: str = "screen", text: str = None) -> str:
    translator = GoogleTranslator()
    languages = translator.get_supported_languages()

    translations = {}
    if text is not None:
        try:
            # Переклад тексту на всі доступні мови
            for code in languages[:10]:
                try:
                    translation = translate(text, dest=code, scr="en")
                    translations[code] = translation
                except Exception as e:
                    translations[code] = f"Error: {e}"
        except Exception as e:
            return f"Translation error: {e}"
    else:
        translations = {}

    # Створюємо таблицю
    data = {
        "N": [],
        "Language": [],
        "ISO-639 code": [],
        "Text": []
    }

    for idx, code in enumerate(languages[:10], start=1):
        lang = full_language(code)
        data["N"].append(idx)
        data["Language"].append(code)
        data["ISO-639 code"].append(lang)
        data["Text"].append(translations.get(code, ""))

    df = pd.DataFrame(data)

    # Виведення таблиці
    try:
        if out == "screen":
            # Виведення відформатованої таблиці на екран
            print(df.to_string(index=False, col_space=20))
        elif out == "file":
            # Збереження таблиці у файл CSV
            df.to_csv("languages.csv", index=False)
            print("Table saved to 'languages.csv'.")
        else:
            return "Invalid output option."
    except Exception as e:
        return f"An error occurred: {e}"

    return "Ok"