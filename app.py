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


@app.route('/add_recipe')
def add_recipe():
    value = mongo.db.recipes.find({'ingredients': ""})
    return render_template('addrecipe.html', categories=mongo.db.categories.find(), value=value)


@app.route('/insert_recipe', methods=['POST'])
def insert_recipe():
    """
    ingredients_doc = {'ingredient': request.form.getlist(
        'ingredients[]')}  # send form to dictionary
    mongo.db.recipes.insert(ingredients_doc)
    """
    """
    recipe = mongo.db.recipes  # var to get db from mongo of tasks
    recipe.insert_one(request.form.to_dict())  # send form to dictionary
    # go to the task.html after sending form
    """

    recipe = {
        'recipe_name': request.form.get('recipe_name'),
        'category_name': request.form.get('category_name'),
        'ingredients': request.form.getlist('ingredients'),
        'instructions': request.form.getlist('instructions'),
        'values': request.form.get('value {($split: [","])}'),
        'image': request.form.get('image'),

    }
    mongo.db.recipes.insert_one(recipe)

    return redirect(url_for('recipe'))


@ app.route('/edit_recipe/<recipe_id>')
def edit_recipe(recipe_id):
    return render_template('editrecipe.html',
                           recipes=mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)}))  # to do a find on the categories table.


@ app.route('/delete_recipe/<recipe_id>')
def delete_recipe(recipe_id):
    mongo.db.recipes.remove({'_id': ObjectId(recipe_id)})
    return redirect(url_for('recipe'))


@ app.route('/workouts')
def workouts():
    return render_template('workouts.html', categories=mongo.db.breathe.find(), workouts=mongo.db.workouts.find())


@ app.route('/relax')
def relax():
    return render_template('relax.html', categories=mongo.db.categories.find(), breathe=mongo.db.breathe.find())


if __name__ == '__main__':

    app.run(host=os.environ.get('IP', '0.0.0.0'),
            port=int(os.environ.get('PORT', '5000')),
            debug=True)
    """
    app.run(host=os.environ.get('IP', '127.0.0.1'),
            port=int(os.environ.get('PORT', '8080')),
            debug=True)
"""
