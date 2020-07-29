import os
if os.path.exists("env.py"):
    import env
from flask import Flask, render_template, redirect, request, url_for, flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.config["MONGO_DBNAME"] = 'breathe'
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')


mongo = PyMongo(app)


@app.route('/')
def index():
    return render_template('index.html', recipes=mongo.db.recipes.find(), workouts=mongo.db.workouts.find())


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', recipes=mongo.db.recipes.find(), workouts=mongo.db.workouts.find())


@app.route('/allrecipe/<category>')
def allrecipe(category):
    # if statements to display the recipes base on category name
    if category == "Pre Workout Meal":
        recipe = mongo.db.recipes.find({"category_name": "Pre Workout Meal"})
    elif category == "Post Workout Meal":
        recipe = mongo.db.recipes.find({"category_name": "Post Workout Meal"})
    else:
        recipe = mongo.db.recipes.find()

    return render_template('allrecipe.html', recipe=recipe, category_title=category, recipes=mongo.db.recipes.find(), isFooter=True)

# ---- SEARCH ----- #


@app.route('/allrecipe/<recipe_name>')
def searchname(recipe_name):
    mongo.db.recipes.find({"$text": {"$search": recipe_name}})
    return render_template('allrecipe.html', name=recipe_name, isFooter=True)


@app.route('/search', methods=["GET", "POST"])
def search():

    search = request.form.get("search")
    results = mongo.db.recipes.find({"$text": {"$search": search}}).limit(2)
    result_count = mongo.db.recipes.find(
        {"$text": {"$search": search}}).count()
    if result_count > 0:
        return render_template("search.html", results=results, search=search, isFooter=True)
    else:
        flash("No results found. Please try again")
        return render_template("search.html", results=results, search=search, isFooter=True)


@app.route('/recipe/<recipe_id>')
def get_recipe(recipe_id):
    recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    return render_template("recipe.html", recipe=recipe, isFooter=True)


@app.route('/add_recipe')
def add_recipe():
    return render_template('addrecipe.html', categories=mongo.db.categories.find(), isFooter=True)


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
        'description': request.form.get('description'),
        'image': request.form.get('image'),
        'prep_time': request.form.get('prep_time'),
        'cook_time': request.form.get('cook_time'),
        'ingredients': request.form.getlist('ingredients'),
        'instructions': request.form.getlist('instructions')
    }
    flash("Thank you for submitting your recipe!")
    mongo.db.recipes.insert_one(recipe)
    return render_template('allrecipe.html', isFooter=True)


@app.route('/edit_recipe/<recipe_id>')
def edit_recipe(recipe_id):
    all_categories = mongo.db.categories.find()
    prerecipes = mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)})
    return render_template('editrecipe.html',
                           recipes=prerecipes, categories=all_categories, isFooter=True)  # to do a find on the categories table.


@app.route('/update_recipe/<recipe_id>', methods=['POST'])
# We pass in the task ID because that's our hook into the primary key.
def update_recipe(recipe_id):
    recipes = mongo.db.recipes
    """ So what we do is we access the tasks collection.
    Then we call the update function.We specify the ID.
    That's our key to uniqueness."""
    recipes.update({'_id': ObjectId(recipe_id)},
                   {
        'recipe_name': request.form.get('recipe_name'),
        'category_name': request.form.get('category_name'),
        'description': request.form.get('description'),
        'image': request.form.get('image'),
        'prep_time': request.form.get('prep_time'),
        'cook_time': request.form.get('cook_time'),
        'ingredients': request.form.getlist('ingredients'),
        'instructions': request.form.getlist('instructions')
    })

    flash("Succesfully updated the recipe!")
    return render_template('allrecipe.html', isFooter=True)


@app.route('/delete_recipe/<recipe_id>')
def delete_recipe(recipe_id):
    mongo.db.recipes.remove({'_id': ObjectId(recipe_id)})
    flash("Succesfully deleted the recipe!")
    return render_template('allrecipe.html', isFooter=True)


@app.route('/workouts')
def workouts():
    return render_template('workouts.html', categories=mongo.db.breathe.find(), workouts=mongo.db.workouts.find(), isFooter=True)


@app.route('/relax')
def relax():
    return render_template('relax.html', categories=mongo.db.categories.find(), recipe=mongo.db.recipes.find(), isFooter=True)


if __name__ == '__main__':

    app.run(host=os.environ.get('IP', '0.0.0.0'),
            port=int(os.environ.get('PORT', '5000')),
            debug=True)
    """
    app.run(host=os.environ.get('IP', '127.0.0.1'),
            port=int(os.environ.get('PORT', '8080')),
            debug=True)
"""
