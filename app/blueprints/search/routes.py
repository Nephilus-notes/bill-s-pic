from . import bp as app
from app.blueprints.main.models import User, AllPokemon, UserPokemon
from app import db, login_manager
from flask import redirect, url_for, render_template, request, flash
from flask_login import current_user
from random import randint
from sqlalchemy import or_


@app.route('/')
def search_pokemon():
    return render_template('search_pokemon.html.j2')

# @app.route('/type/')
# def search_pokemon_type():
#     return render_template('search_pokemon_type.html.j2')

@app.route('/type', methods=["GET", "POST"])
def search_pokemon_type():
    if request.method == 'GET':
        return render_template('search_pokemon_type.html.j2')

    pokemon_type = request.form['type']
    pokemon = db.session.query(AllPokemon).filter(or_(AllPokemon.type1 == pokemon_type, AllPokemon.type2==pokemon_type))
    # pokemon = AllPokemon.query.filter_by(type1=pokemon_type)
    if not pokemon:
        flash('Something went wrong, try again', 'danger')
    return render_template('search_pokemon_type.html.j2', pokemon=pokemon, pokemon_type=pokemon_type)


@app.route('/id', methods=["GET", "POST"])
def search_pokemon_id():
    if request.method == 'GET':
        return render_template('search_pokemon_id.html.j2')

    id = request.form['id']
    pokemon = AllPokemon.query.filter_by(id=id).first()
    if not pokemon:
        flash('Something went wrong, try again', 'danger')
    return render_template('search_pokemon_id.html.j2', pokemon=pokemon)

@app.route('/name', methods=["GET", "POST"])
def search_pokemon_name():
    if request.method == 'GET':
        return render_template('search_pokemon_name.html.j2')

    name = request.form['name']
    pokemon = AllPokemon.query.filter_by(name=name).first()
    if not pokemon:
        flash('Something went wrong, try again', 'danger')
    return render_template('search_pokemon_name.html.j2', pokemon=pokemon)


# @app.route('/ability')
# def search_pokemon_ability():
#     return render_template('search_pokemon_ability.html.j2')

@app.route('/ability', methods=["GET", "POST"])
def search_pokemon_ability():
    if request.method == 'GET':
        return render_template('search_pokemon_ability.html.j2')

    pokemon_ability = request.form['ability']
    pokemon = db.session.query(AllPokemon).filter(or_(AllPokemon.ability1 == pokemon_ability, AllPokemon.ability2==pokemon_ability, AllPokemon.ability3==pokemon_ability))
    # pokemon = AllPokemon.query.filter_by(type1=pokemon_type)
    if not pokemon:
        flash('Something went wrong, try again', 'danger')
    return render_template('search_pokemon_ability.html.j2', pokemon=pokemon, pokemon_ability=pokemon_ability)


# @app.route('/type/<type>')
# def search_pokemon_by_type(type):
#     pokemon = AllPokemon.query.filter_by(type)
#     return render_template('pokemon_single.html.j2', allpokemon=pokemon)

# @app.route('/ability/<ability>')
# def search_pokemon_by_ability(ability):
#     pokemon = AllPokemon.query.filter_by(ability)
#     return render_template('pokemon_single.html.j2', allpokemon=pokemon)

# @app.route('/pokemon/search/name')
# def search_pokemon_name(name=None):
#     return render_template('search_pokemon_name.html.j2')


    return render_template('search_pokemon_name.html.j2')

# @app.route('/name/<name>')
# def search_pokemon_by_name():
#     name = request.form['name']
#     pokemon = AllPokemon.query.get(name)
#     return render_template('pokemon_single.html.j2', pokemon=pokemon)

