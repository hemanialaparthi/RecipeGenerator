"""Program that generates recipes with ingredients available and calculates calories of the meal."""
import requests

# generate recipe with given ingredients
def generate_recipe(ingredients, diet, strict=2):

    url = "https://recipe-generator-create-custom-recipes-from-your-ingredients.p.rapidapi.com/recipe"
    payload = {
        "ingredients": ingredients,
        "strict": strict,
        "diet": diet
    }
    headers = {
        "x-rapidapi-key": "da4afab614mshd81d42243e1a5adp18e526jsnf77c316bf30e",
        "x-rapidapi-host": "recipe-generator-create-custom-recipes-from-your-ingredients.p.rapidapi.com",
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=payload, headers=headers)
    try:
        return response.json()
    except requests.exceptions.JSONDecodeError:
        print("Error decoding JSON response from recipe generator:")
        print(response.text)
        return None

# extract the ingredients and add them to a list
def extract_ingredients(recipe_text):
    lines = recipe_text.split('\n')
    ingredients = []
    capture = False
    for line in lines:
        if line.strip().lower().startswith("ingredients:"):
            capture = True
            continue
        if capture:
            if line.strip() == "":
                break  # end of ingredients section
            # remove leading dash and any whitespace, then append to the list
            ingredients.append(line.strip().lstrip('- ').strip())
    return ingredients

# generate the calories of the ingredients
def calculate_calories(ingredients):
    formatted_ingredients = ", ".join(ingredients)
    url = "https://nutrition-estimator-what-am-i-eating.p.rapidapi.com/api/nutrition_estimator/estimation"
    payload = {"ingredients": formatted_ingredients}
    headers = {
        "x-rapidapi-key": "da4afab614mshd81d42243e1a5adp18e526jsnf77c316bf30e",
        "x-rapidapi-host": "nutrition-estimator-what-am-i-eating.p.rapidapi.com",
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=payload, headers=headers)
    try:
        return response.json()
    except requests.exceptions.JSONDecodeError:
        print("Error decoding JSON response from calorie estimator:")
        print(response.text)
        return None

# total calories
def get_total_calories(calorie_info):
    if not calorie_info:
        print("No calorie information available")
        return 0

    total_calories = 0
    if 'items' in calorie_info:
        total_calories = sum(item.get('calories', 0) for item in calorie_info['items'])
    elif 'energy' in calorie_info:
        # handle different formats of energy information
        energy_value = calorie_info['energy']
        if isinstance(energy_value, str) and energy_value.endswith('kcal'):
            total_calories = float(energy_value.replace('kcal', '').strip())
        elif isinstance(energy_value, (int, float)):
            total_calories = float(energy_value)
    else:
        print("Unexpected calorie information format")
        print(calorie_info)  # log the unexpected format for debugging

    return total_calories

# main function
def main():
    user_ingredients = input("Enter the ingredients you have: ")
    diet_type = input("Enter your diet type (e.g., 'vegan', 'vegetarian', 'keto', 'gluten_free'):\n ")
    strictness = input("Would you like to change the strictness of you diet?\n 1. yes \n 2. no \n 3. find out more.\n")
    if strictness.lower() == "1":
        print("""
        0 - API will craft a recipe using the provided ingredients but may include additional ingredients if needed.
        1 - API will only use the provided ingredients in the recipe.
        2 - API will strictly use the provided ingredients but may recommend additional ingredients for better results. (This is the default setting)\n
        """)
        try:
            strictness = int(input("Enter the strictness level (0, 1, 2):\n"))
            if strictness < 0 or strictness > 2:
                raise ValueError("Strictness level must be between 0 and 2. Defaulting to 2 (moderate).\n")
        except ValueError as e:
            print(e)
            strictness = 2
    elif strictness.lower() == '2':
        strictness = 2
    elif strictness.lower() == '3':
        print("""""
        This program uses an API which allowes users to select the strictness of the ingredients. 
        0 - API will craft a recipe using the provided ingredients but may include additional ingredients if needed.
        1 - API will only use the provided ingredients in the recipe.
        2 - API will strictly use the provided ingredients but may recommend additional ingredients for better results. (This is the default setting).\n
        """)

    print("Generating the recipe...")
    recipe_response = generate_recipe(user_ingredients, diet_type, strictness)

    if recipe_response and 'recipe' in recipe_response:
        recipe = recipe_response['recipe']
        print("\nRecipe generated:")
        print(recipe)

        # extract ingredients from the generated recipe
        ingredients_list = extract_ingredients(recipe)
    else:
        print("Failed to generate recipe.")
        return

    print("\nCalculating calories...")
    calorie_info = calculate_calories(ingredients_list)

    if calorie_info:
        total_calories = get_total_calories(calorie_info)
        print(f"Total calories: {total_calories:.2f}")

        show_breakdown = input("Do you want to see the breakdown of the calories? (yes/no): ").strip().lower()
        if show_breakdown == 'yes':
            print("Calorie breakdown:")
            if 'items' in calorie_info:
                for item in calorie_info['items']:
                    print(f"{item.get('name', 'Unknown')}: {item.get('calories', 0)} kcal")
            else:
                print(calorie_info)  # print the entire calorie_info for debugging
    else:
        print("Failed to calculate calories.")

if __name__ == "__main__":
    main()
