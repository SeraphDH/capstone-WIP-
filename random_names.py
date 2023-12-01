from flask import Flask, render_template, request, redirect, url_for, flash, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from datetime import datetime, timedelta
from models import db, World, Character, User
from forms import RegistrationForm, EditProfileForm, ChangePasswordForm
import json, random

app = Flask(__name__)
path_to_race_files = "./race_name_index2.json"
race2names = {}
with open(path_to_race_files, "r") as race_file:
    race2names = json.load(race_file)

@app.route('/name_gen/<race>', methods=['GET'])
def name_gen(race):
    if race in race2names.keys():
        return random.choice(race2names[race])
    else:
        abort(404)

@app.route('/races', methods=['GET'])
def get_races():
    return list(race2names.keys())

if __name__ == '__main__':
    app.run(debug=True, port=5001)