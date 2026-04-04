"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, Character, Planet
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from sqlalchemy import select
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)

@api.route('/signup', methods=["POST"])
def handle_sign_up():
    body = request.json
    potential_user = db.session.execute(
        select(User).where(User.email == body["email"])
    ).scalar_one_or_none()
    if potential_user is not None:
        return jsonify({"msg": "User with that email already exists"})
    
    # Creating the user object
    new_user = User()
    new_user.email = body["email"]
    new_user.password = body["password"]
    new_user.is_active = True

    # Adding the user to the database and saving the database
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"msg": "User was created"}), 201

@api.route('/login', methods=['POST'])
def create_token():
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    user = User.query.filter_by(email=email, password=password).first()

    # We check to make sure that we found a user with a matching email and password
    if user is None:
        return jsonify({"msg": "Bad username or password"}), 401
    
    access_token = create_access_token(identity=str(user.id))
    return jsonify({ "token": access_token, "user_id": user.id, "email": user.email })

@api.route('/people', methods=['GET'])
def get_all_people():
    all_people = db.session.execute(select(Character)).scalars().all()
    list_of_dictionaries = []
    for person in all_people:
        list_of_dictionaries.append(person.serialize())
    return jsonify(list_of_dictionaries), 200

@api.route('/people/<int:person_id>', methods=['GET'])
def get_single_person(person_id):
    found_person = db.session.get(Character, person_id)
    if found_person is None:
        return jsonify({"msg": "Character does not exist"}), 404
    return jsonify(found_person.serialize()), 200

@api.route('/planets', methods=['GET'])
def get_all_planets():
    all_planets = db.session.execute(select(Planet)).scalars().all()
    list_of_dictionaries = []
    for planet in all_planets:
        list_of_dictionaries.append(planet.serialize())
    return jsonify(list_of_dictionaries), 200

@api.route('/planets/<int:planet_id>', methods=['GET'])
def get_single_planet(planet_id):
    found_planet = db.session.get(Planet, planet_id)
    if found_planet is None:
        return jsonify({"msg": "Planet does not exist"}), 404
    return jsonify(found_planet.serialize()), 200

@api.route('/users', methods=['GET'])

def get_all_users():
    all_users = db.session.execute(select(User)).scalars().all()
    list_of_dictionaries = []
    for user in all_users:
        list_of_dictionaries.append(user.serialize())
    return jsonify(list_of_dictionaries), 200

@api.route('/users/favorites', methods=['GET'])
@jwt_required()
def get_all_favorites(): 
    user_id = get_jwt_identity()
    found_user = db.session.get(User, user_id)
    if found_user is None:
        return jsonify({"msg": "User does not exist"}), 404
    serialized_user = found_user.serialize()
    return jsonify(
        {
            "email": serialized_user["email"],
            "favorite_characters": serialized_user["favorite_characters"],
            "favorite_planets": serialized_user["favorite_planets"] 
        }), 200  

@api.route('/favorite/people/<int:person_id>', methods=['POST'])
@jwt_required()
def add_favorite_person(person_id):
    user_id = get_jwt_identity()
    found_person = db.session.get(Character, person_id)
    found_user = db.session.get(User, user_id)
    if found_user is None:
        return jsonify({"msg": "User does not exist"}), 404
    if found_person is None:
        return jsonify({"msg": "Character does not exist"}), 404
    found_user.favorite_characters.append(found_person)
    db.session.commit()
    serialized_user = found_user.serialize()
    return jsonify({"favorite_characters": serialized_user["favorite_characters"]}), 201

@api.route('/favorite/planets/<int:planet_id>', methods=['POST'])
@jwt_required()
def add_favorite_planet(planet_id):
    user_id = get_jwt_identity()
    found_planet = db.session.get(Planet, planet_id)
    found_user = db.session.get(User, user_id)
    if found_user is None:
        return jsonify({"msg": "User does not exist"}), 404
    if found_planet is None:
        return jsonify({"msg": "Planet does not exist"}), 404
    found_user.favorite_planets.append(found_planet)
    db.session.commit()
    serialized_user = found_user.serialize()
    return jsonify({"favorite_planets": serialized_user["favorite_planets"]}), 201

@api.route('/favorite/people/<int:person_id>', methods=['DELETE'])
@jwt_required()
def delete_favorite_person(person_id):
    user_id = get_jwt_identity()
    found_person = db.session.get(Character, person_id)
    found_user = db.session.get(User, user_id)
    if found_user is None:
        return jsonify({"msg": "User does not exist"}), 404
    if found_person is None:
        return jsonify({"msg": "Character does not exist"}), 404
    found_user.favorite_characters.remove(found_person)
    db.session.commit()
    serialized_user = found_user.serialize()
    return jsonify({"favorite_characters": serialized_user["favorite_characters"]}), 201
    

@api.route('/favorite/planets/<int:planet_id>', methods=['DELETE'])
@jwt_required()
def delete_favorite_planet(planet_id):
    user_id = get_jwt_identity()
    found_planet = db.session.get(Planet, planet_id)
    found_user = db.session.get(User, user_id)
    if found_user is None:
        return jsonify({"msg": "User does not exist"}), 404
    if found_planet is None:
        return jsonify({"msg": "Planet does not exist"}), 404
    found_user.favorite_planets.remove(found_planet)
    db.session.commit()
    serialized_user = found_user.serialize()
    return jsonify({"favorite_planets": serialized_user["favorite_planets"]}), 201