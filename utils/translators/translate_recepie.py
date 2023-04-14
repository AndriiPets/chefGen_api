
from utils.translators.en_ru.en_ru import translator_en_ru

ru = translator_en_ru


def translate_recepie(recepie, translator=ru):
    data = {"title": "", "ingredients": [], "directions": []}

    data["title"] = translator(recepie["title"])

    directions = "|".join(recepie["directions"])
    data["directions"] = translator(directions).split('|')

    ingredients = "|".join(recepie["ingredients"])
    data["ingredients"] = translator(ingredients).split('|')

    return data
