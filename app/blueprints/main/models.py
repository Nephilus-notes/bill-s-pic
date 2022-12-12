from app import db, login_manager
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import requests


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    username = db.Column(db.String(50), unique=True)
    date_created = db.Column(db.DateTime, default =datetime.utcnow)
    password= db.Column(db.String(200))
    pokemon = db.relationship('UserPokemon', backref="user")

    def hash_my_password(self, password):
        self.password = generate_password_hash(password)

    def check_my_password(self, password):
        return check_password_hash(self.password, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class AllPokemon(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), nullable=False)
    type1= db.Column(db.String(45), nullable=False)
    type2 = db.Column(db.String(45))
    reg_sprite = db.Column(db.String(600), nullable=False)
    shiny_sprite = db.Column(db.String(600))
    ability1 = db.Column(db.String(60), nullable=False)
    ability2 = db.Column(db.String(60))
    ability3 = db.Column(db.String(60))
    has_shiny = db.Column(db.Boolean, default= False, nullable=False)

class Move(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    effect = db.Column(db.String(255), nullable=False)


class UserPokemon(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    pokemon_id = db.Column(db.Integer, db.ForeignKey('all_pokemon.id'), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    type1= db.Column(db.String(45), nullable=False)
    type2 = db.Column(db.String(45))
    sprite = db.Column(db.String(600), nullable=False)
    ability = db.Column(db.String(60), nullable=False)
    move1 = db.Column(db.Integer, db.ForeignKey('move.id'), nullable=False)
    move2 = db.Column(db.Integer, db.ForeignKey('move.id'))
    move3 = db.Column(db.Integer, db.ForeignKey('move.id'))
    move4 = db.Column(db.Integer, db.ForeignKey('move.id'))
    date_caught = db.Column(db.DateTime, default=datetime.utcnow)
    owner = db.relationship('User', backref="user_pokemon", overlaps="pokemon,user")

class PokemonMove(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    pokemon_id = db.Column(db.Integer, db.ForeignKey('all_pokemon.id'), nullable=False)
    move_id = db.Column(db.Integer, db.ForeignKey('move.id'), nullable=False)

class UserMove(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    move_id = db.Column(db.Integer, db.ForeignKey('move.id'), nullable=False)
    owner = db.relationship('User', backref="use_rmove")

def create_pokemon():
    for num in range(1, 901):
        # api call
        response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{num}')

        # making the data available to me in the function
        data = response.json()

        # creating pokemon dict without types, ablities, sprites, or moves
        pokemon = {
        'name': data['name'],
        'id': data['id'],
        }

        # creating type/ability lists to avoid key indexing
        types = [type['type']['name'] for type in data['types']]
        abilities = [ability['ability']['name'] for ability in data['abilities']]

        for index, type in enumerate(types):    
            pokemon[f'type{index+1}'] = type

        for index, ability in enumerate(abilities):    
            pokemon[f'ability{index+1}'] = ability
            
        try:
            if data['sprites']['versions']['generation-v']['black-white']['animated']['front_shiny']:
                pokemon['shiny_sprite'] = data['sprites']['versions']['generation-v']['black-white']['animated']['front_shiny']
                pokemon['has_shiny'] = True
            else:
                raise KeyError
        except:
            if data['sprites']['front_shiny']:
                pokemon['shiny_sprite'] = data['sprites']['front_shiny']
                pokemon['has_shiny'] = True
            else:
                pokemon['has_shiny'] = False

        
        try:
            if data['sprites']['versions']['generation-v']['black-white']['animated']['front_default']:
                pokemon['reg_sprite'] = data['sprites']['versions']['generation-v']['black-white']['animated']['front_default']
            else:
                raise KeyError
        except:
            pokemon['reg_sprite'] = data['sprites']['front_default']

        check_pokemon = AllPokemon.query.filter_by(id=pokemon['id']).first()
        print(pokemon['id'])
        print(check_pokemon)
        if check_pokemon:
            print("updating sprite")
            check_pokemon.reg_sprite = pokemon['reg_sprite']
        else:
            new_pokemon = AllPokemon(**pokemon)
            db.session.add(new_pokemon)
    db.session.commit()

# from app.blueprints.main.models import create_pokemon

def create_move():
    for num in range(1, 901):
        # api call
        response = requests.get(f'https://pokeapi.co/api/v2/move/{num}')

        # making the data available to me in the function
        data = response.json()

        # creating dictionary for the move
        if data['effect_entries']:
            print(f'got move {num}')
            move = {
            'name': data['name'],
            'id': data['id'],
            'effect': data['effect_entries'][0]['short_effect'],
            'description': data['flavor_text_entries'][0]['flavor_text']
            }


            check_move = Move.query.filter_by(id=move['id']).first()

            if check_move:
                print(" We got this one already")
            else:
                new_move = Move(**move)
                db.session.add(new_move)
        else:
            db.session.commit()

# def create_pokemon_move_table():
#     for num in range(1, 901):
#         # api call
#         response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{num}')

#         # making the data available to me in the function
#         data = response.json()
#         for move_num in range(1, 749):
#             print(move_num)
#             move = Move.query.get(move_num)
#             if move.name in data['moves']:
#                 pokemon_move = PokemonMove(pokemon_id = num, move_id=move_num)
#                 db.session.add(pokemon_move)
#     db.session.commit()

# def create_pokemon_move_table_small():
#     for num in range(1, 25):
#         # api call
#         response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{num}')

#         # making the data available to me in the function
#         data = response.json()
#         for move_num in range(1, 749):
#             print(move_num)
#             move = Move.query.get(move_num)
#             if move.name in data['moves']:
#                 pokemon_move = PokemonMove(pokemon_id = num, move_id=move_num)
#                 db.session.add(pokemon_move)
#     db.session.commit()

def create_pokemon_move_table():
    for num in range(1, 10):
        # api call
        response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{num}')

        # making the data available to me in the function
        data = response.json()


        for move_num in range(1, 10):
            move = Move.query.get(move_num)
            for dct in data['moves']:
                if move.name == dct['move']['name']:
                    print(move.name)
                    print(num, move_num)
                    pokemon_move = PokemonMove(pokemon_id = num, move_id=move_num)
                    db.session.add(pokemon_move)
                    break

    db.session.commit()

# from app.blueprints.main.models import create_pokemon_move_table
