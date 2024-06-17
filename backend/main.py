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
        "x-rapidapi-key": "aef0bc537amsh78ae44286ba3867p100f0ejsn1cb354c21648",
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
        "x-rapidapi-key": "aef0bc537amsh78ae44286ba3867p100f0ejsn1cb354c21648",
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
        # Assume that the energy is in kcal and is a string ending with 'kcal'
        total_calories = float(calorie_info['energy'].replace('kcal', '').strip())
    else:
        print("Unexpected calorie information format")
        print(calorie_info)  # Log the unexpected format for debugging

    return total_calories

# main function
def main():
    user_ingredients = input("Enter the ingredients you have: ")
    diet_type = input("Enter your diet type (e.g., 'vegan', 'vegetarian', 'keto'): ")

    print("Generating recipe...")
    recipe_response = generate_recipe(user_ingredients, diet_type)
    
    if recipe_response and 'recipe' in recipe_response:
        recipe = recipe_response['recipe']
        print("\nRecipe generated:")
        print(recipe)

        # Extract ingredients from the generated recipe
        ingredients_list = extract_ingredients(recipe)
        print("\nExtracted Ingredients:")
        print(ingredients_list)
    else:
        print("Failed to generate recipe.")
        return

    print("\nCalculating calories...")
    calorie_info = calculate_calories(ingredients_list)

    if calorie_info:
        total_calories = get_total_calories(calorie_info)
        print(f"Total calories: {total_calories:.2f}")

        show_breakdown = input("Do you want to see the breakdown of the calories? (y/n): ").strip().lower()
        if show_breakdown == 'y':
            print("Calorie breakdown:")
            if 'items' in calorie_info:
                for item in calorie_info['items']:
                    print(f"{item['name']}: {item['calories']} kcal")
            else:
                for key, value in calorie_info.items():
                    if isinstance(value, dict) and 'calories' in value:
                        print(f"{key}: {value['calories']} kcal")
    else:
        print("Failed to calculate calories.")

if __name__ == "__main__":
    main()

