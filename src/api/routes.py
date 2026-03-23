"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, Character, Planet
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from sqlalchemy import select

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200

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

@api.route('/users/<int:user_id>/favorites', methods=['GET'])
def get_all_favorites(user_id):
    found_user = db.session.get(User, user_id)
    if found_user is None:
        return jsonify({"msg": "User does not exist"}), 404
    serialized_user = found_user.serialize()
    return jsonify(
        {
            "favorite_characters": serialized_user["favorite_characters"],
            "favorite_planets": serialized_user["favorite_planets"] 
        }), 200  

@api.route('/favorite/people/<int:person_id>', methods=['POST'])
def add_favorite_person(person_id):
    body = request.json
    found_person = db.session.get(Character, person_id)
    found_user = db.session.get(User, body["user_id"])
    if found_user is None:
        return jsonify({"msg": "User does not exist"}), 404
    if found_person is None:
        return jsonify({"msg": "Character does not exist"}), 404
    found_user.favorite_characters.append(found_person)
    db.session.commit()
    serialized_user = found_user.serialize()
    return jsonify({"favorite_characters": serialized_user["favorite_characters"]}), 201

@api.route('/favorite/planets/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    body = request.json
    found_planet = db.session.get(Planet, planet_id)
    found_user = db.session.get(User, body["user_id"])
    if found_user is None:
        return jsonify({"msg": "User does not exist"}), 404
    if found_planet is None:
        return jsonify({"msg": "Planet does not exist"}), 404
    found_user.favorite_planets.append(found_planet)
    db.session.commit()
    serialized_user = found_user.serialize()
    return jsonify({"favorite_planets": serialized_user["favorite_planets"]}), 201

@api.route('/favorite/people/<int:person_id>', methods=['DELETE'])
def delete_favorite_person(person_id):
    pass

@api.route('/favorite/planets/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    pass