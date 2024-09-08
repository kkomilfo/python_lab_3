# filetr.py

import os
from deep_translator import GoogleTranslator
from langdetect import detect
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
nltk.download('punkt_tab')
def read_config(filename):
    if not os.path.isfile(filename):
        raise FileNotFoundError(f"Configuration file '{filename}' not found.")

    with open(filename, 'r') as file:
        lines = file.read().splitlines()
        if len(lines) != 6:
            raise ValueError("Configuration file should contain exactly 6 lines.")

        text_file = lines[0]
        target_lang = lines[1]
        output_mode = lines[2]
        max_chars = int(lines[3])
        max_words = int(lines[4])
        max_sentences = int(lines[5])

    return text_file, target_lang, output_mode, max_chars, max_words, max_sentences

def analyze_text(text):
    num_chars = len(text)
    num_words = len(word_tokenize(text))
    num_sentences = len(sent_tokenize(text))
    return num_chars, num_words, num_sentences

def read_text_file(filename, max_chars, max_words, max_sentences):
    if not os.path.isfile(filename):
        raise FileNotFoundError(f"Text file '{filename}' not found.")

    with open(filename, 'r') as file:
        content = ""
        for line in file:
            content += line
            num_chars, num_words, num_sentences = analyze_text(content)
            if num_chars > max_chars or num_words > max_words or num_sentences > max_sentences:
                break

    return content.strip()

def translate_text(text, target_lang):
    translator = GoogleTranslator(target=target_lang)
    return translator.translate(text)

def write_output(filename, translated_text, output_mode, target_lang):
    if output_mode == "file":
        output_file = f"{os.path.splitext(filename)[0]}_{target_lang}.txt"
        with open(output_file, 'w') as file:
            file.write(translated_text)
        print(f"File saved as '{output_file}'.")
    elif output_mode == "screen":
        print(f"Translated text ({target_lang}):")
        print(translated_text)
    else:
        raise ValueError("Invalid output mode specified.")

def main():
    try:
        config_file = 'config.txt'
        text_file, target_lang, output_mode, max_chars, max_words, max_sentences = read_config(config_file)

        text = read_text_file(text_file, max_chars, max_words, max_sentences)

        num_chars, num_words, num_sentences = analyze_text(text)
        print(f"File: {text_file}")
        print(f"Size: {os.path.getsize(text_file)} bytes")
        print(f"Characters: {num_chars}")
        print(f"Words: {num_words}")
        print(f"Sentences: {num_sentences}")
        print(f"Detected language: {detect(text)}")

        translated_text = translate_text(text, target_lang)
        print(f"Translated text: {translated_text}")

        write_output(text_file, translated_text, output_mode, target_lang)

        print("Ok")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
