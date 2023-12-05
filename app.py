from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from datetime import datetime, timedelta
from models import *
from forms import *
import requests, json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db.init_app(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
races_as_bytes = requests.get('http://127.0.0.1:5001/races').content
races = json.loads(races_as_bytes.decode('UTF-8'))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('worlds'))

        flash('Login failed. Please check your username and password.', 'error')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout successful!', 'success')
    return redirect(url_for('login'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/worlds', methods=['GET', 'POST'])
@login_required
def worlds():
    if request.method == 'POST':
        world_id_to_remove = request.form.get('world_id_to_remove')
        if world_id_to_remove:
            world = World.query.get(world_id_to_remove)
            if world and current_user.id == world.creator_id:
                try:
                    Character.query.filter_by(world_id=world.id).delete()
                    db.session.commit()
                    db.session.delete(world)
                    db.session.commit()
                    flash('World successfully removed!', 'success')
                except IntegrityError:
                    db.session.rollback()
                    flash('Error removing world. Please try again.', 'error')

                return redirect(url_for('worlds'))

    worlds = World.query.all()
    return render_template('worlds.html', worlds=worlds)

@app.route('/add_world', methods=['GET', 'POST'])
@login_required
def add_world():
    if request.method == 'POST':
        new_world_name = request.form.get('new_world_name')
        new_world_description = request.form.get('new_world_description')

        new_world = World(name=new_world_name, description=new_world_description, creator_id=current_user.id)
        db.session.add(new_world)
        try:
            db.session.commit()
            flash('World successfully added!', 'success')
        except IntegrityError:
            db.session.rollback()
            flash('Error adding world. Please try again.', 'error')

        return redirect(url_for('worlds'))

    return render_template('add_world.html')

@app.route('/edit_world/<int:world_id>', methods=['GET', 'POST'])
@login_required
def edit_world(world_id):
    world = World.query.get(world_id)

    if world and current_user.id == world.creator_id:
        if request.method == 'POST':
            world.name = request.form.get('edit_world_name')
            world.description = request.form.get('edit_world_description')
            try:
                db.session.commit()
                flash('World successfully edited!', 'success')
            except IntegrityError:
                db.session.rollback()
                flash('Error editing world. Please try again.', 'error')

            return redirect(url_for('world_detail', world_id=world.id))

        return render_template('edit_world.html', world=world)

    flash('You do not have permission to edit this world.', 'error')
    return redirect(url_for('worlds'))

@app.route('/remove_world/<int:world_id>', methods=['GET', 'POST'])
@login_required
def remove_world(world_id):
    world = World.query.get(world_id)

    if world and current_user.id == world.creator_id:
        if request.method == 'POST':
            try:
                Character.query.filter_by(world_id=world.id).delete()
                db.session.commit()
                db.session.delete(world)
                db.session.commit()
                flash('World successfully removed!', 'success')
            except IntegrityError:
                db.session.rollback()
                flash('Error removing world. Please try again.', 'error')

            return redirect(url_for('worlds'))

        return render_template('remove_world.html', world=world)

    flash('You do not have permission to remove this world.', 'error')
    return redirect(url_for('worlds'))

@app.route('/world_detail/<int:world_id>', methods=['GET', 'POST'])
@login_required
def world_detail(world_id):
    world = World.query.get(world_id)

    if world and current_user.id == world.creator_id:
        if request.method == 'POST':
            if 'edit_world_name' in request.form:
                world.name = request.form.get('edit_world_name')
                world.description = request.form.get('edit_world_description')
                try:
                    db.session.commit()
                    flash('World successfully edited!', 'success')
                except IntegrityError:
                    db.session.rollback()
                    flash('Error editing world. Please try again.', 'error')
            elif 'remove_world' in request.form:
                try:
                    db.session.delete(world)
                    db.session.commit()
                    flash('World successfully removed!', 'success')
                    return redirect(url_for('worlds'))
                except IntegrityError:
                    db.session.rollback()
                    flash('Error removing world. Please try again.', 'error')

        return render_template('world_detail.html', world=world, races=races)

    flash('You do not have permission to view this world.', 'error')
    return redirect(url_for('worlds'))

@app.route('/random_name', methods=['POST'])
@login_required
def random_name():
    if request.method == 'POST':
        race = request.form.get('race')
        response = requests.get(f'http://127.0.0.1:5001/name_gen/{race}')
        if response.status_code == 404:
            flash("That Race does not exist! Try again!", 'error')
            return redirect('/characters')
        else:
            name = response.content.decode('UTF-8')
            return redirect(url_for('character_list', name=name))


@app.route('/add_character/', methods=['POST'])
@login_required
def add_character():
    if request.method == 'POST':
        new_character_name = request.form.get('new_character_name')
        new_character_description = request.form.get('new_character_description')
        world_id = request.form.get("world_id")

        if current_user.is_authenticated:
            new_character = Character(
                name=new_character_name,
                description=new_character_description,
                world_id=world_id if world_id else None,
                user_id=current_user.id
            )
            print(world_id if world_id else None)
            print(world_id)
            db.session.add(new_character)
            try:
                db.session.commit()
                flash('Character successfully added!', 'success')
            except IntegrityError as ie:
                print(ie)
                db.session.rollback()
                flash('Error adding character. Please try again.', 'error')

            if world_id:
                return redirect(url_for('world_detail', world_id=world_id))
            else:
                return redirect(url_for('character_list')) 
            
    return render_template('add_character.html', world_id=world_id)

@app.route('/character_detail/<int:character_id>')
@login_required
def character_detail(character_id):
    character = Character.query.get(character_id)
    return render_template('character_detail.html', character=character)

@app.route('/remove_character/<int:character_id>', methods=['POST'])
@login_required
def remove_character(character_id):
    character = Character.query.get(character_id)

    if character and current_user.id == character.user_id:
        try:
            db.session.delete(character)
            db.session.commit()
            flash('Character successfully removed!', 'success')
        except IntegrityError:
            db.session.rollback()
            flash('Error removing character. Please try again.', 'error')

        return redirect(url_for('world_detail', world_id=character.world_id))

    flash('You do not have permission to remove this character.', 'error')
    return redirect(url_for('character_list'))

@app.route('/characters', methods=['GET'])
@login_required
def character_list():
    characters = Character.query.all()
    name = request.args.get('name')
    worlds = World.query.all()
    if name:
        return render_template('character_list.html', characters=characters, races=races, name=name, worlds = worlds)
    else:
        return render_template('character_list.html', characters=characters, races=races, worlds = worlds)

@app.route('/edit_character/<int:character_id>', methods=['GET', 'POST'])
@login_required
def edit_character(character_id):
    character = Character.query.get(character_id)

    if character and current_user.id == character.user_id:
        if request.method == 'POST':
            character.name = request.form.get('edit_character_name')
            character.description = request.form.get('edit_character_description')
            try:
                db.session.commit()
                flash('Character successfully edited!', 'success')
            except IntegrityError:
                db.session.rollback()
                flash('Error editing character. Please try again.', 'error')

            return redirect(url_for('character_detail', character_id=character.id))

        return render_template('edit_character.html', character=character)

    flash('You do not have permission to edit this character.', 'error')
    return redirect(url_for('character_list'))

@app.route('/plots', methods=['GET', 'POST'])
@login_required
def plots():
    worlds = World.query.all()
    if request.method == 'POST':
        world_id = request.form.get('select_world')
        return redirect(url_for('plots', world_id=world_id))
    else:
        world_id = request.args.get('world_id')
        if world_id:
            world = World.query.get(world_id)
            return render_template('plots.html', worlds=worlds, current_world = world)
        else:
            return render_template('plots.html', worlds=worlds)

@app.route('/update_plot_data/<world_id>', methods=['POST'])
@login_required
def update_plot_data(world_id):
    world = World.query.get(world_id)
    
    if request.method == 'POST':
        main_quest = request.form.get('main_quests')
        if main_quest:
            world.main_quests = main_quest
        
        side_quest = request.form.get('side_quests')
        if side_quest:
            world.side_quests = side_quest

        plot_hook = request.form.get('plot_hooks')
        if plot_hook:
            world.plot_hooks = plot_hook
        
        character_quest = request.form.get('character_quests')
        if character_quest:
            world.character_quests = character_quest
        
        fun_twist = request.form.get('fun_twists')
        if fun_twist:
            world.fun_twists = fun_twist
        
        big_bad_evil_guy = request.form.get('big_bad_evil_guys')
        if big_bad_evil_guy:
            world.big_bad_evil_guys = big_bad_evil_guy
        
        db.session.commit()

        return redirect(url_for('plots', world_id=world_id))
    else:
        return redirect(url_for('plots', world_id=world_id))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username is already taken. Please choose another.', 'error')
            return redirect(url_for('register'))

        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        try:
            db.session.commit()
            login_user(new_user)
            flash('Registration successful! Welcome to the application.', 'success')
        except IntegrityError:
            db.session.rollback()
            flash('Error registering user. Please try again.', 'error')

        return redirect(url_for('index'))

    return render_template('register.html', form=form)

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    change_profile_form = ChangeProfileForm()
    print("TEST")
    if request.method == 'POST':
        if change_profile_form.validate_on_submit():
            new_username = change_profile_form.new_username.data
            print(new_username)
            if new_username:
                current_user.username = new_username
                try:
                    db.session.commit()
                    print('Username successfully updated')
                    flash('Username successfully updated!', 'success')
                except IntegrityError:
                    db.session.rollback()
                    print('Error updating username. Please choose another.')
                    flash('Error updating username. Please choose another.', 'error')

            current_password = change_profile_form.current_password.data
            new_password = change_profile_form.new_password.data
            confirm_new_password = change_profile_form.confirm_new_password.data

            if current_password:
                if current_user.check_password(current_password):
                    if new_password == confirm_new_password:
                        current_user.set_password(new_password)
                        db.session.commit()
                        flash('Password successfully updated!', 'success')
                    else:
                        flash('New password and confirmation do not match.', 'error')
                else:
                    flash('Current password is incorrect.', 'error')

    return render_template('profile.html', change_profile_form=change_profile_form)

@app.route('/delete_account', methods=['POST'])
@login_required
def delete_account():
    # Delete user account
    user_id = current_user.id
    logout_user()
    User.query.filter_by(id=user_id).delete()
    db.session.commit()
    flash('Account successfully deleted!', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)