from flask import Blueprint, jsonify,request
from models import User, Character, Location
from app import db

api = Blueprint("api", __name__)

#Obtener todos los usuarios
@api.route("/users", methods=["GET"])
def get_users():
    user = User.query.all()
    response= [user.serialize()for user in user] #list comprehension
    return jsonify(response), 200

# obtener un solo usuario 
@api.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = User.query.get(user_id)
    if not user: #si no existe el user:
        return jsonify({"message": "User not found"}), 404
    return jsonify(user.serialize()), 200

@api.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    if not data.get("name") or not data.get("email") or not data.get("password"):
        return jsonify({"message": "Missing required fields"}), 400
    
    new_user = User(
        name=data["name"],
        email=data["email"],
        password=data["password"]
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.serialize()), 201


@api.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"}), 200


@api.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    user= User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    
    data = request.get_json()
    user.name =data.get("name", user.name)
    user.email = data.get("email", user.email)
    user.password = data.get("password", user.password)

    db.session.commit()
    return jsonify(user.serialize()), 200


@api.route("/users/<int:user_id>/favorites", methods=["POST"])
def add_favorite(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    
    data = request.get_json()
    character_id = data.get("character_id")
    character = Character.query.get(character_id)
    if not character:
        return jsonify({"message": "Character not found"}), 404
    
    user.favorites.append(character)
    db.session.commit()
    return jsonify({"message": "Character added to favorites"}), 200


#characters zone
@api.route("/characters", methods=["GET"])
def get_characters():
    characters = Character.query.all()
    response = [character.serialize() for character in characters]
    return jsonify(response), 200



@api.route("/characters/<int:character_id>", methods=["GET"])
def get_character(character_id):
    character = Character.query.get(character_id)
    if not character:
        return jsonify({"message": "Character not found"}), 404
    return jsonify(character.serialize()), 200



@api.route("/characters", methods=["POST"])
def create_character():
    data = request.get_json()
    if not data.get("name") or not data.get("image") or not data.get("quote") or not data.get("location_id"):
        return jsonify({"message": "Missing required fields"}), 400
    
    new_character = Character(
        name=data["name"],
        image=data["image"],
        quote=data["quote"],
        location_id=data["location_id"]
    )
    db.session.add(new_character)
    db.session.commit()
    return jsonify(new_character.serialize()), 201


@api.route("/characters/<int:character_id>", methods=["DELETE"])
def delete_character(character_id):
    character = Character.query.get(character_id)
    if not character:
        return jsonify({"message": "Character not found"}), 404
    db.session.delete(character)
    db.session.commit()
    return jsonify({"message": "Character deleted successfully"}), 200



@api.route("/characters/<int:character_id>", methods=["PUT"])
def update_character(character_id):
    character = Character.query.get(character_id)
    if not character:
        return jsonify({"message": "Character not found"}), 404
    
    data = request.get_json()
    character.name = data.get("name", character.name)
    character.image = data.get("image", character.image)
    character.quote = data.get("quote", character.quote)
    character.location_id = data.get("location_id", character.location_id)

    db.session.commit()
    return jsonify(character.serialize()), 200



#location zone
@api.route("/location", methods=["POST"])
def create_location():
    data = request.get_json()
    if not data.get("name"):
        return jsonify({"message": "Missing required fields"}), 400
    
    new_location = Location(
        name=data["name"]
    )
    db.session.add(new_location)
    db.session.commit()
    return jsonify(new_location.serialize()), 201


@api.route("/location", methods=["GET"])
def get_locations():
    locations = Location.query.all()
    response = [location.serialize() for location in locations]
    return jsonify(response), 200

@api.route("/location/<int:location_id>", methods=["GET"])
def get_location(location_id):
    location = Location.query.get(location_id)
    if not location:
        return jsonify({"message": "Location not found"}), 404
    return jsonify(location.serialize()), 200

@api.route("/location/<int:location_id>", methods=["DELETE"])
def delete_location(location_id):
    location = Location.query.get(location_id)
    if not location:
        return jsonify({"message": "Location not found"}), 404
    db.session.delete(location)
    db.session.commit()
    return jsonify({"message": "Location deleted successfully"}), 200

@api.route("/location/<int:location_id>", methods=["PUT"])
def update_location(location_id):
    location = Location.query.get(location_id)
    if not location:
        return jsonify({"message": "Location not found"}), 404
    
    data = request.get_json()
    location.name = data.get("name", location.name)

    db.session.commit()
    return jsonify(location.serialize()), 200





@api.route("/users/<int:user_id>/favorites", methods=["GET"])
def get_favorites(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    
    favorites = [character.serialize() for character in user.favorites]
    return jsonify(favorites), 200


@api.route("/users/<int:user_id>/favorites/<int:character_id>", methods=["DELETE"])
def remove_favorite(user_id, character_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    
    character = Character.query.get(character_id)
    if not character:
        return jsonify({"message": "Character not found"}), 404
    
    if character in user.favorites:
        user.favorites.remove(character)
        db.session.commit()
        return jsonify({"message": "Character removed from favorites"}), 200
    else:
        return jsonify({"message": "Character not in favorites"}), 404
    
