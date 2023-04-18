
from utils.translators.en_ru.en_ru import translator_en_ru

translators = {"ru": translator_en_ru}


def translate_recepie(recepie, lang="en"):

    translator = translators[lang]

    data = {"title": "", "ingredients": [], "directions": []}

    data["title"] = translator(recepie["title"])

    directions = "|".join(recepie["directions"])
    data["directions"] = [x.strip() for x in translator(directions).split(',')]

    ingredients = "/".join(recepie["ingredients"])
    data["ingredients"] = [x.strip()
                           for x in translator(ingredients).split('/')]

    return data
