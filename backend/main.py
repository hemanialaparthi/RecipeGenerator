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
        "x-rapidapi-key": "8f3eac1b80msh544acfc720c92c9p151248jsnda5d8c853936",
        "x-rapidapi-host": "recipe-generator-create-custom-recipes-from-your-ingredients.p.rapidapi.com",
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()

# generate the calories of the ingredients
def calculate_calories(ingredients):
    url = "https://nutrition-estimator-what-am-i-eating.p.rapidapi.com/api/nutrition_estimator/estimation"
    payload = { "ingredients": ingredients }
    headers = {
        "x-rapidapi-key": "6160410e38msh4f71d07faa45339p134e64jsnec00fbf58dad",
        "x-rapidapi-host": "nutrition-estimator-what-am-i-eating.p.rapidapi.com",
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()

# total calories
def get_total_calories(calorie_info):
    total_calories = sum(item.get('calories', 0) for item in calorie_info.get('items', []))
    return total_calories

# 

# main function
def main():
    user_ingredients = input("Enter the ingredients you have: ")
    diet_type = input("Enter your diet type (e.g., 'vegan', 'vegetarian', 'keto'): ")

    print("Generating recipe...")
    recipe_response = generate_recipe(user_ingredients, diet_type)
    recipe = recipe_response['recipe']  # This assumes 'recipe' is a dictionary containing structured recipe information

    # Print out the formatted recipe
    print("\nRecipe generated:")
    print(recipe)

    print("\nCalculating calories...")
    calorie_info = calculate_calories(user_ingredients)

    # Calculate total calories by extracting and converting relevant values
    total_calories = sum(float(value.replace('kcal', '')) for key, value in calorie_info.items() if key == 'energy')
    print(f"Total calories: {total_calories:.2f}")

    show_breakdown = input("Do you want to see the breakdown of the calories? (yes/no): ").strip().lower()
    if show_breakdown == 'yes':
        print("Calorie breakdown:")
        for key, value in calorie_info.items():
            print(f"{key}: {value}")

if __name__ == "__main__":
    main()

