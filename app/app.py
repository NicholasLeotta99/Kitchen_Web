'''
This is the main file for the Flask application. It contains the routes and the logic for each route.

Written by: Nicholas Leotta
Date: 2024-05-25
'''


from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

##############################################################
# Initialize the app and the database
##############################################################

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join('/app', 'data', 'pantry.db')
app.config['SQLALCHEMY_BINDS'] = {
    'second_db': 'sqlite:///' + os.path.join('/app', 'data', 'recipe.db')
}
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.debug = True

db = SQLAlchemy(app)

##############################################################
# Define the routes and the logic for each route
##############################################################

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/lets_cook')
def lets_cook():
    return render_template('lets_cook.html')

@app.route('/open_pantry')
def open_pantry():
    # Assuming you have a function get_all_items() that returns all items from the database
    items = get_all_items()
    return render_template('open_pantry.html', items=items)

@app.route('/enter_groceries', methods=['POST'])
def enter_groceries():
    name = request.form['name']
    quantity = request.form['quantity']
    unit = request.form['unit']
    expiration_date = request.form['expiration_date'] if request.form['expiration_date'] else None
    new_item = PantryItem(name=name, quantity=quantity, unit=unit, expiration_date=expiration_date)
    db.session.add(new_item)
    db.session.commit()
    return 'Item added to pantry'


@app.route('/delete_items', methods=['POST'])
def delete_items():
    ids = request.json['ids']
    PantryItem.query.filter(PantryItem.id.in_(ids)).delete(synchronize_session=False)
    db.session.commit()
    return 'Items deleted'

@app.route('/recipe_book')
def recipe_book():
    recipes = Recipe.query.all()  # Get all recipes from the database
    return render_template('recipe_book.html', recipes=recipes)

##############################################################
# Define the models
##############################################################

class PantryItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit = db.Column(db.String(80), nullable=False)
    expiration_date = db.Column(db.DateTime, nullable=True)

class Recipe(db.Model):
    __bind_key__ = 'second_db'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    ingredients = db.relationship('Ingredient', backref='recipe', lazy=True)
    instructions = db.relationship('Instruction', backref='recipe', lazy=True)

class Instruction(db.Model):
    __bind_key__ = 'second_db'
    id = db.Column(db.Integer, primary_key=True)
    step_number = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)
    time = db.Column(db.Integer, nullable=True)  # Time in minutes
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)

class Ingredient(db.Model):
    __bind_key__ = 'second_db'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    quantity = db.Column(db.String(80), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)

##############################################################
# Define the functions to interact with the database
##############################################################

def get_all_items():
    return PantryItem.query.all()

def get_all_recipes():
    return Recipe.query.all()

##############################################################
# Run the app
##############################################################
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000)