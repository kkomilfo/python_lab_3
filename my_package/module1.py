from googletrans import Translator, LANGUAGES
import pandas as pd

translator = Translator()

def translate(text: str, dest='en', src='auto') -> str:
    try:
        translated = translator.translate(text, dest=dest, src=src)
        return translated.text
    except Exception as e:
        return f"Something went wrong: {str(e)}"

def lang_detect(text) -> str:
    try:
        detection = translator.detect(text)
        return f"Detected(lang={detection.lang}, confidence={detection.confidence})"
    except Exception as e:
        return f"Something went wrong: {str(e)}"

def full_language(iso_code) -> str:
    return LANGUAGES[iso_code]

def language_list(out: str = "screen", text: str = None) -> str:
    translations = {}
    if text is not None:
        try:
            for code in list(LANGUAGES.keys())[:10]:
                translation = translator.translate(text, dest=code)
                translations[code] = translation.text
        except Exception as e:
            return f"Translation error: {e}"
    else:
        translations = {}

    data = {
        "N": [],
        "Language": [],
        "ISO-639 code": [],
        "Text": []
    }

    for idx, (code, lang) in enumerate(list(LANGUAGES.items())[:10], start=1):
        data["N"].append(idx)
        data["Language"].append(lang.title())
        data["ISO-639 code"].append(code)
        data["Text"].append(translations.get(code, ""))

    df = pd.DataFrame(data)

    try:
        if out == "screen":
            print(df.to_string(index=False, col_space=15))
        elif out == "file":
            df.to_csv("languages.csv", index=False)
            print("Table saved to 'languages.csv'.")
        else:
            return "Invalid output option."
    except Exception as e:
        return f"An error occurred: {e}"

    return "Ok"