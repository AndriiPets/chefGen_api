import re
import os

text = 'title:macaroni and corn ingredients: 1 lb. macarooni 2 tbsp. butter 1 tsp salt 4 slices bacon 2 1/2 c. milk 2/3 c flour pepper to taste 1 can cream corn directions: cook macaronis in salted water until tender. fry bacon until crisp. drain on paper towel. melt butter in saucepan. add flour, salt and pepper. cook over low heat, stirring constantly, until mixture is smooth and bubbly. remove from heat. stir in milk. return to heat and bring to a boil. reduce heat and simmer until thickened. fold in corn and bacon. pour into greased baking dish. bake at 350 for 30 minutes.'

text = text + '$'

pattern = r"(\w+:)(.+?(?=\w+:|\$))"

data = {"title": "", "ingredients": [], "directions": []}

for match in re.findall(pattern, text):
    if match[0] == 'title:':
        data["title"] = match[1]
    elif match[0] == 'ingredients:':
        data["ingredients"] = [ing.strip() for ing in match[1].split(',')]
    elif match[0] == 'directions:':
        data["directions"] = [dir.strip() for dir in match[1].split('.')]
print(os.getenv("API_KEY"))
