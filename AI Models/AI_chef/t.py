import json, pandas as pd

def save_ingredients(ingredients: list[str], key: str = "initail_ingredients"):
    """Saves the ingredients list to a JSON file."""
    j = {key: ingredients}
    lj = load_ingredients()
    if lj:
        lj.update(j)
        j = lj
    with open("ingredients.json", "w") as json_file:
        json.dump(j, json_file, indent=4)
        
def load_ingredients(key: str = None):
    """Loads the ingredients list from a JSON file."""
    try:
        with open("ingredients.json", "r") as json_file:
            if key:
                return json.load(json_file).get(key, [])
            return json.load(json_file)
    except Exception:
        return {}
    
    
def take_input():
    s = "Broccoli, Carrot, Onions, Garlic, Ginger"
    l = sorted([item.strip().capitalize() for item in s.split(',')])
    save_ingredients(l, "initail_ingredients")
    
def manupulate_input():
    ingredients = load_ingredients()
    ingredients = ingredients[ "all_ingredients" if "all_ingredients" in ingredients else "initail_ingredients"]

    print(ingredients)

    new_item = "cheese"
    
    if new_item.strip():
        ingredients = sorted(list(set(ingredients + [new_item.strip().capitalize()])))
        save_ingredients(ingredients, "all_ingredients")
        
    print(ingredients)
    
    
def process_ingredients():
    dishes = {'dishes': [{'dish_name': 'Garlic Ginger Broccoli and Carrot Stir-fry', 'required_ingredients': ['Broccoli', 'Carrot', 'Onions', 'Garlic', 'Ginger'], 'recipe': ['Finely chop onions, garlic, and ginger.', 'Cut broccoli and carrots into bite-sized pieces.', 'Stir-fry onions, garlic, and ginger in a wok or large pan with a little oil until fragrant.', 'Add broccoli and carrots, stir-fry until tender-crisp.', 'Season with salt and pepper to taste.']}, {'dish_name': 'Ginger Carrot and Broccoli Soup', 'required_ingredients': ['Broccoli', 'Carrot', 'Onions', 'Garlic', 'Ginger', 'Vegetable Broth'], 'recipe': ['Sauté onions, garlic, and ginger in a pot.', 'Add chopped broccoli and carrots, cook for a few minutes.', 'Pour in vegetable broth, bring to a boil, then simmer until vegetables are tender.', 'Blend until smooth (optional).']}, {'dish_name': 'Broccoli and Carrot Fritters', 'required_ingredients': ['Broccoli', 'Carrot', 'Onions', 'Garlic', 'Ginger', 'Egg', 'Flour'], 'recipe': ['Grate carrots and finely chop broccoli, onions, garlic, and ginger.', 'Mix with egg and flour to form a batter.', 'Fry spoonfuls of batter in oil until golden brown.']}, {'dish_name': 'Spicy Carrot and Onion Relish', 'required_ingredients': ['Carrot', 'Onions', 'Ginger', 'Chili'], 'recipe': ['Grate carrots and finely chop onions and ginger.', 'Mix with finely chopped chili (adjust amount to taste).', 'Season with salt and lime juice.']}, {'dish_name': 'Garlic Ginger Broccoli with Soy Sauce', 'required_ingredients': ['Broccoli', 'Garlic', 'Ginger', 'Soy Sauce'], 'recipe': ['Steam or blanch broccoli until tender-crisp.', 'Sauté minced garlic and ginger in oil until fragrant.', 'Toss broccoli with garlic-ginger mixture and soy sauce.']}, {'dish_name': 'Sautéed Onions and Carrots with Ginger', 'required_ingredients': ['Onions', 'Carrot', 'Ginger'], 'recipe': ['Slice onions and carrots thinly.', 'Sauté onions and carrots with minced ginger until softened.']}, {'dish_name': 'Creamy Carrot and Broccoli Soup', 'required_ingredients': ['Broccoli', 'Carrot', 'Onions', 'Garlic', 'Ginger', 'Heavy Cream'], 'recipe': ['Sauté onions, garlic, and ginger.', 'Add chopped broccoli and carrots, cook for a few minutes.', 'Add vegetable broth, simmer until tender.', 'Blend until smooth, stir in heavy cream.']}, {'dish_name': 'Garlic and Ginger Noodles with Broccoli', 'required_ingredients': ['Broccoli', 'Garlic', 'Ginger', 'Noodles', 'Soy Sauce'], 'recipe': ['Cook noodles according to package directions.', 'Sauté minced garlic and ginger.', 'Add cooked broccoli and noodles, toss with soy sauce.']}, {'dish_name': 'Potato and Carrot Stir-fry (Replacing Broccoli)', 'required_ingredients': ['Potato', 'Carrot', 'Onions', 'Garlic', 'Ginger'], 'recipe': ['Dice potatoes and carrots.', 'Stir-fry onions, garlic, and ginger.', 'Add potatoes and carrots, stir-fry until tender.']}, {'dish_name': 'Simple Garlic Ginger Carrot', 'required_ingredients': ['Carrot', 'Garlic', 'Ginger'], 'recipe': ['Slice carrots thinly.', 'Sauté minced garlic and ginger.', 'Add carrots, stir-fry until tender-crisp.']}]}
    
    dishes = dishes.get("dishes")
    
    if dishes:
        dish_name = []
        required_ingredients = []
        recipe = []
        
        for dish in dishes:
            dish_name.append(dish["dish_name"])
            required_ingredients.append(dish["required_ingredients"])
            recipe.append(dish["recipe"])
        
        df = pd.DataFrame(
            {
                "dish_name": dish_name,
                "required_ingredients": required_ingredients,
                "recipe": recipe,
            }
        )
        
        print(df)
        save_ingredients(df.to_dict(), "dishes")

def main():
    take_input()
    manupulate_input()
    process_ingredients()
    
    
main()