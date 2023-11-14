from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from models import World

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

# Sample route to render a list of worlds
@app.route('/')
def index():
    worlds = World.query.all()
    return render_template('index.html', worlds=worlds)

# Sample route to render details of a specific world
@app.route('/world/<int:world_id>')
def world_detail(world_id):
    world = World.query.get_or_404(world_id)
    return render_template('world_detail.html', world=world)

if __name__ == '__main__':
    app.run(debug=True)
