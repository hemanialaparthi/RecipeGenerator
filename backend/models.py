from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class UserPreference(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    food_type = db.Column(db.String(50), nullable=False)
    flavor_profile = db.Column(db.String(50), nullable=False)
    meat_option = db.Column(db.String(50), nullable=False)
    veggies_option = db.Column(db.String(50), nullable=False)
