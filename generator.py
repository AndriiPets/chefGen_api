from transformers import pipeline, set_seed
from transformers import AutoTokenizer
import re
from utils import ext
from utils.ext import pure_comma_separation

from decouple import config
import os

from utils.api import generate_cook_image
from utils.translators.translate_recepie import translate_recepie
from utils.translators.translate_input import translate_input


model_name_or_path = "flax-community/t5-recipe-generation"
task = "text2text-generation"

tokenizer = AutoTokenizer.from_pretrained(model_name_or_path)
generator = pipeline(task, model=model_name_or_path,
                     tokenizer=model_name_or_path)

prefix = "items: "

chef_top = {
    "max_length": 512,
    "min_length": 64,
    "no_repeat_ngram_size": 3,
    "do_sample": True,
    "top_k": 60,
    "top_p": 0.95,
    "num_return_sequences": 1,
    "return_tensors": True,
    "return_text": False
}
chef_beam = {
    "max_length": 512,
    "min_length": 64,
    "no_repeat_ngram_size": 3,
    "early_stopping": True,
    "num_beams": 5,
    "length_penalty": 1.5,
    "num_return_sequences": 1
}

generation_kwargs = {
    "max_length": 512,
    "min_length": 64,
    "no_repeat_ngram_size": 3,
    "do_sample": True,
    "top_k": 60,
    "top_p": 0.95
}


def load_api():
    api_key = config("API_KEY")
    api_id = config("API_ID")
    return {"KEY": api_key, "ID": api_id}


def skip_special_tokens_and_prettify(text):

    data = {"title": "", "ingredients": [], "directions": []}

    text = text + '$'

    pattern = r"(\w+:)(.+?(?=\w+:|\$))"

    for match in re.findall(pattern, text):
        if match[0] == 'title:':
            data["title"] = match[1]
        elif match[0] == 'ingredients:':
            data["ingredients"] = [ing.strip() for ing in match[1].split(',')]
        elif match[0] == 'directions:':
            data["directions"] = [d.strip() for d in match[1].split('.')]
        else:
            pass

    data["ingredients"] = ext.ingredients(
        data["ingredients"])

    data["directions"] = ext.directions(data["directions"])

    data["title"] = ext.title(data["title"])

    return data


def generation_function(texts, lang="en"):

    langs = ['ru', 'en']

    if lang != "en" and lang in langs:
        texts = translate_input(texts, lang)

    output_ids = generator(
        texts,
        ** chef_top
    )[0]["generated_token_ids"]

    recipe = tokenizer.decode(output_ids, skip_special_tokens=False)

    generated_recipe = skip_special_tokens_and_prettify(recipe)

    if lang != "en" and lang in langs:
        generated_recipe = translate_recepie(generated_recipe, lang)

    api_credentials = load_api()
    cook_image = generate_cook_image(
        generated_recipe['title'], app_id=api_credentials['ID'], app_key=api_credentials['KEY'])

    generated_recipe["image"] = cook_image

    return generated_recipe


items = [
    "macaroni, butter, salt, bacon, milk, flour, pepper, cream corn",
    "provolone cheese, bacon, bread, ginger"
]
