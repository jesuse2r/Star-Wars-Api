"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet, Favorite
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def get_all_user():
    user_list = User.query.all()
    serialized_user = [user.serialize() for user in user_list]
    return jsonify({"data": serialized_user})






@app.route("/user/favorite/<int:id>", methods=['GET'])
def get_all_favorite(id):
    favorite_list = Favorite.query.filter_by(user_id=id).all()


  
    if not favorite_list:
        return {"mensaje" : "este usuario no tiene favorito"} 
    serialized_favorite = [favorite.serialize() for favorite in favorite_list]
    return jsonify({"data": serialized_favorite})



@app.route("/favorite/character/<int:id>", methods=['POST'])
def add_all_character_favorite(id):
  
    
    body = request.json
   
    character_id = body.get("character_id", None)
   
    if  character_id is None:
        return {"error": "el character es invalido"},400
    favorite_exists = Favorite.query.filter_by(user_id=id,character_id=character_id).first()
   
    if favorite_exists:
        return {"error": "Ya existe un planeta con el nombre:"}, 400
   
    new_favorites = Favorite(user_id=id,character_id=character_id)
    db.session.add(new_favorites)
    
 
    try:
        db.session.commit()
        return jsonify({"msg": "Favorito creado con exito"}), 201
    except Exception as error:
        db.session.rollback()
        return jsonify ({"error": error})

@app.route("/favorite/planet/<int:id>", methods=['POST'])
def add_all_favorite(id):
  
    
    body = request.json
   
    planet_id = body.get("planet_id", None)
   
    if not planet_id:
        return {"error": "el planeta es invalido"}
    favorite_exist = Favorite.query.filter_by(user_id=id,planet_id=planet_id).first()
   
    if favorite_exist:
        return {"Error": "Ya existe un planeta con el nombre: "}, 400
   
    new_favorite = Favorite(planet_id=planet_id, user_id=id)
    db.session.add(new_favorite)
 
    try:
        db.session.commit()
        return jsonify({"msg": "Favorito creado con exito"}), 201
    except Exception as error:
        db.session.rollback()
        return jsonify ({"error": error})





@app.route('/characters', methods=['GET'])
def get_all_characters():
    character_list = Character.query.all()
    serialized_characters = [character.serialize() for character in character_list]
    return jsonify({"data": serialized_characters})

@app.route('/character/<int:id>', methods=['GET'])
def get_character(id):
   
    character = Character.query.filter_by(id=id).one_or_none()
  
    if not character:
        return {"mensaje" : "no existe un personaje con este id"}    
    return jsonify({"data": character.serialize()})



@app.route('/character', methods=['POST'])
def create_character():
    body = request.json
    body_name = body.get('name', None)
    body_eye_color = body.get('eye_color', None)
    body_homeworld = body.get('homeworld', None)
    body_gender = body.get('gender', None)

    if body_name is None or body_eye_color is None or body_homeworld is None or body_gender is None:
        return {"error: Todos los campos requeridos"}, 400

    character_exists = Character.query.filter_by(name=body_name).first()
    if character_exists:
        return {"error": f"ya existe un personaje con el nombre: {body_name}"}, 400
    new_character = Character(name=body_name,  eye_color=body_eye_color, homeworld=body_homeworld, gender=body_gender)
    db.session.add(new_character)
    try:
        db.session.commit()
        return jsonify({"msg": "personaje creado con exito!"}), 201
    except Exception as error:
        db.session.rollback()
        return {"error": error}, 500


@app.route('/character/<int:id>', methods=['DELETE'])
def delete_character(id):
    
    character = Character.query.get(id)
    if not character:
        return {"mensaje" : "no existe un personaje con este id"}    
    db.session.delete(character)
    try:
         db.session.commit()
         return "personaje elminado con exito"
    except Exception as error:
        db.session.rollback()
        return {"error": error}, 500

@app.route('/character/<int:id>', methods=['PUT'])
def actualice_character(id):
    character = Character.query.get(id)
    body = request.json
    body_name = body.get('name', None)
    body_eye_color = body.get('eye_color', None)
    body_homeworld = body.get('homeworld', None)
    body_gender = body.get('gender', None)
    if not character:
        return {"mensaje" : "no existe un personaje con este id"} 
    if body_name is not None: 
        character.name = body_name
 
    if body_eye_color is not None:
        character.eye_color = body_eye_color
  
    if body_homeworld is not None:
        character.homeworld = body_homeworld

    if body_gender is not None:
        character.gender = body_gender

    try:
     db.session.commit()
     return "personaje actualizado"
    except Exception as error:
        db.session.rollback()
        return {"error": error}, 500
    

    

@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    serialized_planets = [planet.serialize() for planet in planets]
    return jsonify({"data": serialized_planets})

@app.route('/planet/<int:id>', methods=['GET'])
def get_planet(id):
   
    planet = Planet.query.filter_by(id=id).one_or_none()
  
    if not planet:
        return {"mensaje" : "no existe un planeta con este id"}    
    return jsonify({"data": planet.serialize()})

@app.route('/planet', methods=['POST'])
def add_planet():
    body = request.json
    body_name = body.get('name', None)
    body_population = body.get('population', None)
    body_terrain = body.get('terrain', None)
    body_climate = body.get('climate', None)
    body_faction = body.get('faction', None)
    if body_name is None or body_population is None:
        return {"error": "dos campos requeridos is name, is population"}, 400

    planet_exists = Planet.query.filter_by(name=body_name).first()
    if planet_exists:
        return{"error": f"ya existe un planeta con el nombre: {body_name}"}
    
    new_planet = Planet(name=body_name, population=body_population, terrain=body_terrain, climate=body_climate, faction=body_faction)
    db.session.add(new_planet)
    try:
        db.session.commit()
        return jsonify({"msg": "planeta creado con exito!"}), 201
    except Exception as error:
        db.session.rollback()
        return {"error": error}, 500
    
    
    db.session.add(new_planet)
    db.session.commit()
   
    return jsonify({"data": f"Planeta {body_name} creado con exito"}), 201

@app.route('/planet/<int:id>', methods=['PUT'])
def actualice_planet(id):
    planet = Planet.query.get(id)
    body = request.json
    body_name = body.get('name', None)
    body_terrain = body.get('terrain', None)
    body_population = body.get('population', None)
    body_climate = body.get('climate', None)
    body_faction = body.get('faction', None)
    if not planet:
        return {"mensaje" : "no existe un planeta con este id"} 
    if body_name is not None: 
        planet.name = body_name
 
    if body_terrain is not None:
        planet.terrain = body_terrain
  
    if body_population is not None:
        planet.population = body_population

    if body_climate is not None:
        planet.climate = body_climate
    
    if body_faction is not None:
        planet.faction = body_faction

    try:
     db.session.commit()
     return "planeta actualizado"
    except Exception as error:
        db.session.rollback()
        return {"error": error}, 500

@app.route('/favorite/planet/<int:planet_id>/<int:user_id>', methods=['DELETE'])
def delete_favorite_planet(user_id, planet_id):
    favorite_delete = Favorite.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if not favorite_delete:
        return {"msg": "no existe un favorite con este id"}
    db.session.delete(favorite_delete)
    try:
         db.session.commit()
         return "planeta elminado con exito"
    except Exception as error:
        db.session.rollback()
        return {"error": error}, 500


@app.route('/favorite/character/<int:character_id>/<int:user_id>', methods=['DELETE'])
def delete_favorite_character(user_id, character_id):
    favorite_deletes = Favorite.query.filter_by(user_id=user_id, character_id=character_id).first()
    if not favorite_deletes:
        return {"msg": "no existe un favorite con este id"}
    db.session.delete(favorite_deletes)
    try:
        db.session.commit()
        return "character elminado con exito"
    except Exception as error:
        db.session.rollback()
        return {"error": error}, 500
            

    

@app.route('/planet/<int:id>', methods=['DELETE'])
def delete_planet(id):
    
    planet = Planet.query.get(id)
    if not planet:
        return {"mensaje" : "no existe un planet con este id"}    
    db.session.delete(planet)
    try:
         db.session.commit()
         return "planeta elminado con exito"
    except Exception as error:
        db.session.rollback()
        return {"error": error}, 500

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
