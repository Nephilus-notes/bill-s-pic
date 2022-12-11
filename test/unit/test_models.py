from app.blueprints.main.models import User, AllPokemon, Move, PokemonMove, UserPokemon, UserMove
from test.conftest import new_user

def test_new_user():
    """
    Given a user model
    When a new user is created
    THEN check the email, password, and username fields are defined correctly
    """
    user= User(email='pat@gmail.com', username='patty', password='FlaskIsAwesome')
    assert user.email == 'pat@gmail.com'
    assert user.username == 'patty'
    assert user.password == 'FlaskIsAwesome'
    assert user

def test_new_allpokemon():
    """
    Given an allpokemon model
    When a new allpokemon is created
    THEN check the name, type1,type2, reg_sprite, ability1, shiny_sprite, and has_shiny fields are defined correctly
    """
    pokemon = AllPokemon(name='ralts', type1="psychic",reg_sprite = 'something',ability1= 'synchronize')
    assert pokemon.name == 'ralts'
    assert pokemon.type1 == 'psychic'
    assert pokemon.type2 == None
    assert pokemon.reg_sprite == 'something'
    assert pokemon.shiny_sprite == None
    assert pokemon.ability1 == 'synchronize'
    assert pokemon.has_shiny == None

def test_new_move():
    """
    Given a move model
    When a new move is created
    THEN check the name, description, and effect fields are defined correctly
    """

    move = Move(name='mega punch', description='an allout punch', effect='no additional effect')
    assert move.name == 'mega punch'
    assert move.description == 'an allout punch'
    assert move.effect == 'no additional effect'

def test_user_pokemon(new_user):
    """
    Given a move model
    When a new user_pokemon is created
    THEN check user_id, pokemon_id, name, type1, ability
    move1, move2, move3, move4, and date_caught fields are defined correctly
    """
    pokemon = UserPokemon(user_id=1, pokemon_id=4, name='charmander', 
    type1='fire', ability='flash fire', move1='scratch', move2='leer', move3='smokescreen', 
    move4='ember', date_caught='11:59:36', owner= new_user)
    assert pokemon.user_id == 1
    assert pokemon.pokemon_id == 4
    assert pokemon.name == 'charmander'
    assert pokemon.type1 == 'fire'
    assert pokemon.ability == 'flash fire'
    assert pokemon.move1 == 'scratch'
    assert pokemon.move2 == 'leer'
    assert pokemon.move3 == 'smokescreen'
    assert pokemon.move4 == 'ember'
    assert pokemon.date_caught == '11:59:36'
    pokemon.owner == new_user

def test_pokemon_move():
    """
    GIVEN a pokemon_move model
    WHEN  a new pokemon_move is created
    THEN check the id, pokemon_id, and move_id fields are defined correctly
    """

    pokemon_move = PokemonMove(id=1, pokemon_id=2, move_id=3)
    assert pokemon_move.id == 1
    assert pokemon_move.pokemon_id == 2
    assert pokemon_move.move_id == 3

def test_user_move(new_user):
    """
    GIVEN a user_move model
    WHEN  a new user_move is created
    THEN check the id, user_id, and move_id fields are defined correctly
    """

    user_move = UserMove(id=1, user_id=2, move_id=3, owner= new_user)
    assert user_move.id == 1
    assert user_move.user_id == 2
    assert user_move.move_id == 3
    assert user_move.owner == new_user