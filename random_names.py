from flask import Flask, render_template, request, redirect, url_for, flash, abort
from datetime import datetime, timedelta
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