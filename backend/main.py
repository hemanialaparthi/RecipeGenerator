from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import requests
from models import UserPreference, db

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///friends.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

@app.route('/set_preferences', methods=['POST'])
def set_preferences():
    data = request.get_json()
    food_type = data.get('food_type')
    flavor_profile = data.get('flavor_profile')
    meat_option = data.get('meat_option')
    veggies_option = data.get('veggies_option')

    user_preference = UserPreference(
        food_type=food_type,
        flavor_profile=flavor_profile,
        meat_option=meat_option,
        veggies_option=veggies_option
    )
    db.session.add(user_preference)
    db.session.commit()

    return jsonify({"message": "Preferences saved successfully!"}), 201

@app.route('/get_recipe', methods=['GET'])
def get_recipe():
    preference = UserPreference.query.order_by(UserPreference.id.desc()).first()

    if not preference:
        return jsonify({"message": "No preferences found"}), 404

    api_url = "https://www.themealdb.com/api/json/v1/1/filter.php"
    params = {
        "c": preference.food_type,
    }

    response = requests.get(api_url, params=params)
    if response.status_code != 200:
        return jsonify({"message": "Failed to fetch recipe"}), 500

    recipe_data = response.json()
    return jsonify(recipe_data), 200

if __name__ == "__main__":
    app.run(debug=True)
