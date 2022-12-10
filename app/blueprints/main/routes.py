from . import bp as app
from app.blueprints.main.models import User, AllPokemon
from app import db, login_manager
from flask import redirect, url_for, render_template, request, flash
from flask_login import current_user
from random import randint


@app.route('/')
def home():
    random_ids = [randint(1, 901) for x in range(10)]
    display_pokemon = {}
    for id in random_ids:
        random_pokemon = AllPokemon.query.filter_by(id=id).first()
        display_pokemon[id] = random_pokemon
    return render_template('home.html', user=current_user, pokemon=display_pokemon)


@app.route('/pokemon/<id>')
def pokemon_by_id(id):
    pokemon = AllPokemon.query.get(int(id))
    return render_template('pokemon_single.html.j2', pokemon=pokemon)