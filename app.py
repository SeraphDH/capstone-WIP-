from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import secrets  # Import the secrets module for generating a secret key
from models import db, World, Character  # Import the db and World from models

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = secrets.token_hex(16)  # Set the secret key
db.init_app(app)  # Initialize the SQLAlchemy instance with your Flask app

# Configuring flash message categories
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5) 

# Sample route for the homepage
@app.route('/')
def index():
    return render_template('index.html')

# Sample route for the worlds page
@app.route('/worlds', methods=['GET', 'POST'])
def worlds():
    if request.method == 'POST':
        world_id_to_remove = request.form.get('world_id_to_remove')
        if world_id_to_remove:
            world = World.query.get(world_id_to_remove)
            if world:
                db.session.delete(world)
                db.session.commit()

    worlds = World.query.all()
    return render_template('worlds.html', worlds=worlds)

# New route to handle adding a new world
@app.route('/add_world', methods=['GET', 'POST'])
def add_world():
    if request.method == 'POST':
        new_world_name = request.form.get('new_world_name')
        new_world_description = request.form.get('new_world_description')

        new_world = World(name=new_world_name, description=new_world_description)
        db.session.add(new_world)
        db.session.commit()

        return redirect(url_for('worlds'))

    # Handle the GET request (render the form to add a new world)
    return render_template('add_world.html')

# New route to handle editing an existing world
@app.route('/edit_world/<int:world_id>', methods=['GET', 'POST'])
def edit_world(world_id):
    world = World.query.get(world_id)

    if request.method == 'POST':
        world.name = request.form.get('edit_world_name')
        world.description = request.form.get('edit_world_description')
        db.session.commit()

        return redirect(url_for('world_detail', world_id=world.id))

    return render_template('edit_world.html', world=world)

# New route to handle removing an existing world
@app.route('/remove_world/<int:world_id>', methods=['GET', 'POST'])
def remove_world(world_id):
    world = World.query.get(world_id)

    if request.method == 'POST':
        if world:
            db.session.delete(world)
            db.session.commit()
            flash('World removed successfully', 'success')
            return redirect(url_for('worlds'))

    flash('Are you sure you want to remove this world?', 'warning')
    return render_template('remove_world.html', world=world)


# New route for world detail page
@app.route('/world_detail/<int:world_id>', methods=['GET', 'POST'])
def world_detail(world_id):
    world = World.query.get(world_id)

    if request.method == 'POST':
        if 'edit_world_name' in request.form:
            world.name = request.form.get('edit_world_name')
            world.description = request.form.get('edit_world_description')
            db.session.commit()
        elif 'remove_world' in request.form:
            db.session.delete(world)
            db.session.commit()
            return redirect(url_for('worlds'))

    return render_template('world_detail.html', world=world)

# New route for adding a character
@app.route('/add_character/<int:world_id>', methods=['POST'])
def add_character(world_id):
    if request.method == 'POST':
        new_character_name = request.form.get('new_character_name')
        new_character_description = request.form.get('new_character_description')

        new_character = Character(name=new_character_name, description=new_character_description, world_id=world_id)
        db.session.add(new_character)
        db.session.commit()

        return redirect(url_for('world_detail', world_id=world_id))

    # Handle the GET request (render the form to add a new character)
    return render_template('add_character.html', world_id=world_id)

# New route for the character detail page
@app.route('/character_detail/<int:character_id>')
def character_detail(character_id):
    character = Character.query.get(character_id)
    return render_template('character_detail.html', character=character)

# New route for removing a character
@app.route('/remove_character/<int:character_id>', methods=['POST'])
def remove_character(character_id):
    character = Character.query.get(character_id)

    if character:
        db.session.delete(character)
        db.session.commit()

    return redirect(url_for('world_detail', world_id=character.world_id))

@app.route('/characters', methods=['GET'])
def character_list():
    characters = Character.query.all()
    return render_template('character_list.html', characters=characters)

@app.route('/edit_character/<int:character_id>', methods=['GET', 'POST'])
def edit_character(character_id):
    character = Character.query.get(character_id)

    if request.method == 'POST':
        # Handle the editing logic here
        character.name = request.form.get('edit_character_name')
        character.description = request.form.get('edit_character_description')
        db.session.commit()

        return redirect(url_for('character_detail', character_id=character.id))

    return render_template('edit_character.html', character=character)

if __name__ == '__main__':
    app.run(debug=True)
