import re


DEFAULT_MAP_DICT = {
    " c ": " c. ",
    ", chopped": " (chopped)",
    ", crumbled": " (crumbled)",
    ", thawed": " (thawed)",
    ", melted": " (melted)",
}


def replace_regex(text, map_dict):
    pattern = "|".join(map(re.escape, map_dict.keys()))
    return re.sub(pattern, lambda m: map_dict[m.group()], str(text))


def unique_list(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]


def pure_comma_separation(list_str, return_list=True):
    r = unique_list([item.strip()
                    for item in list_str.lower().split(",") if item.strip()])
    if return_list:
        return r
    return ", ".join(r)


def ingredient(text, map_dict):
    if len(map_dict) > 0:
        map_dict.update(**DEFAULT_MAP_DICT)
    else:
        map_dict = DEFAULT_MAP_DICT

    text = replace_regex(text, map_dict)
    text = re.sub(r"(\d)\s(\d\/\d)", r" \1+\2 ", text)
    text = " ".join([word.strip() for word in text.split() if word.strip()])
    return text


def ingredients(text: list[str]):

    tokens = ['<sep>', '<section>']

    texts = text[0].split(tokens[0])

    text_list = [text.replace(tokens[1], '').strip() for text in texts]

    return text_list


def directions(text_list: list[str]):
    token = '<sep>'
    text_list.pop()

    clean_txt = []

    for line in text_list:
        new = line.replace(token, '').strip()
        clean_txt.append(new)

    return clean_txt


def title(text: str):
    token = '<section>'

    return text.replace(token, '').strip()
