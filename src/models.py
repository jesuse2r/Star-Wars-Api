from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(300), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    eye_color = db.Column(db.String(17), nullable=True)
    homeworld = db.Column(db.String(80), nullable=True)
    gender = db.Column(db.String(80), nullable=True)

    def __repr__(self):
        return '<Character %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "eye_color": self.eye_color,
            "homeworld": self.homeworld,
            "gender": self.gender
        }
class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    population = db.Column(db.String(50), nullable=False)
    climate = db.Column(db.String(17), nullable=True)
    terrain= db.Column(db.String(80), nullable=True)
    faction= db.Column(db.String(80), nullable=True)

    def __repr__(self):
        return '<Planet %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population,
            "homeworld": self.climate,
            "gender": self.terrain,
            "faction": self.faction,
        }
class Favorite(db.Model):

    id= db.Column(db.Integer, primary_key=True)
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'), nullable= True)
    character= db.relationship("Character",backref="favorite")
    planet_id = db.Column(db.Integer,db.ForeignKey('planet.id'), nullable= True)
    planet= db.relationship("Planet", backref="favorite")
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'), nullable = False)
    user= db.relationship("User", backref="favorite")

    def __repr__(self):
        return '<Favorite %r>' % self.name

    def serialize(self):
        return {
        "name": self.planet.name if self.planet.name else self.character.name,
        "character_id": self.character_id,
        "planet_id": self.planet_id,
        "user_id": self.user_id,
        "id": self.id
        
        }
    
    