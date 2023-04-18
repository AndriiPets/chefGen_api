
from utils.translators.en_ru.ru_en import translate_ru_en

translators = {"ru": translate_ru_en}


def translate_input(inputs, lang="ru"):
    translator = translators[lang]

    text = translator(inputs)
    return text
