from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class World(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    characters = db.relationship('Character', backref='world', lazy=True)

class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)  # Add this line for the description column
    world_id = db.Column(db.Integer, db.ForeignKey('world.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
