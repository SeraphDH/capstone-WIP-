# models.py
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    worlds = db.relationship('World', backref='creator', lazy=True)
    characters = db.relationship('Character', backref='user', lazy=True)
    plot_data = db.relationship('PlotData', backref='user', lazy=True)  # Added relationship to PlotData

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class World(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    characters = db.relationship('Character', backref='world', lazy=True)
    plots = db.relationship('PlotData', backref='world', lazy=True)


class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    world_id = db.Column(db.Integer, db.ForeignKey('world.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class PlotData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    main_quests = db.Column(db.Text, nullable=True)
    side_quests = db.Column(db.Text, nullable=True)
    plot_hooks = db.Column(db.Text, nullable=True)
    character_quests = db.Column(db.Text, nullable=True)
    fun_twists = db.Column(db.Text, nullable=True)
    big_bad_evil_guy = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    world_id = db.Column(db.Integer, db.ForeignKey('world.id'), nullable=False)
