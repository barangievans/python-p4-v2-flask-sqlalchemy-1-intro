# server/app.py

from flask import Flask, jsonify, request
from flask_migrate import Migrate
from models import db, Pet

# Create a Flask application instance
app = Flask(__name__)

# Configure the database connection to the local file app.db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

# Configure flag to disable modification tracking and use less memory
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create a Migrate object to manage schema modifications
migrate = Migrate(app, db)

# Initialize the Flask application to use the database
db.init_app(app)

# Create a sample route to get all pets
@app.route('/pets', methods=['GET'])
def get_pets():
    pets = Pet.query.all()
    return jsonify([{'id': pet.id, 'name': pet.name, 'species': pet.species} for pet in pets])

# Create a route to add a new pet
@app.route('/pets', methods=['POST'])
def add_pet():
    data = request.get_json()
    new_pet = Pet(name=data['name'], species=data['species'])
    db.session.add(new_pet)
    db.session.commit()
    return jsonify({'id': new_pet.id, 'name': new_pet.name, 'species': new_pet.species}), 201

# Main entry point to run the application
if __name__ == '__main__':
    app.run(port=5555, debug=True)
