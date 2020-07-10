import os
if os.path.exists("env.py"):
    import env
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.config["MONGO_DBNAME"] = 'breathe'

mongo = PyMongo(app)


@app.route('/')
def index():
    return render_template('index.html', recipes=mongo.db.recipes.find(), workouts=mongo.db.workouts.find())


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', recipes=mongo.db.recipes.find(), workouts=mongo.db.workouts.find())


@app.route('/recipe')
def recipe():
    return render_template('recipe.html', recipes=mongo.db.recipes.find(), post=mongo.db.post_recipes.find())


@ app.route('/workouts')
def workouts():
    return render_template('workouts.html', recipes=mongo.db.recipes.find(), workouts=mongo.db.workouts.find())


@ app.route('/relax')
def relax():
    return render_template('relax.html', recipes=mongo.db.recipes.find(), workouts=mongo.db.workouts.find())


if __name__ == '__main__':

    app.run(host=os.environ.get('IP', '0.0.0.0'),
            port=int(os.environ.get('PORT', '5000')),
            debug=True)
    """
    app.run(host=os.environ.get('IP', '127.0.0.1'),
            port=int(os.environ.get('PORT', '8080')),
            debug=True)
"""
