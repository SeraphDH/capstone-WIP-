from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from models import db, World  # Import the db and World from models

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db.init_app(app)  # Initialize the SQLAlchemy instance with your Flask app

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

    if world:
        db.session.delete(world)
        db.session.commit()

    return redirect(url_for('worlds'))

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

if __name__ == '__main__':
    app.run(debug=True)
