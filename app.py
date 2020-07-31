import os
if os.path.exists("env.py"):
    import env
from flask import Flask, render_template, redirect, request, url_for, session, flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import bcrypt

app = Flask(__name__)

app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')


mongo = PyMongo(app)


@app.route('/')
def index():
    return render_template('index.html', isNav=True)


# Register Account page
@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Create new user and insert into the database for account registration
    """
    if request.method == 'POST':
        existing_user = mongo.db.users.find_one(
            {'username': request.form['username']})
        password = request.form['password']
        repeat_password = request.form['repeat_password']

        # check if the username matches username in the database
        if existing_user:
            flash("Username already exists! Please try again.")
            return redirect(url_for('register'))

        # check passwords is equal then will insert the new user
        if password == repeat_password:
            password_hashpass = bcrypt.hashpw(
                request.form['password'].encode('utf-8'), bcrypt.gensalt())
            register = {
                "email": request.form.get("email").lower(),
                "username": request.form.get("username").lower(),
                "password": password_hashpass
            }
            mongo.db.users.insert_one(register)

            session["username"] = request.form.get("username").lower()
            flash(", thank you for registering! you can now access all the recipes and you can submit your favourite recipe! enjoy!")
            return render_template('allrecipe.html', username=session["username"])

        flash('The passwords dont match.')
        return redirect(url_for('register'))

    return render_template('register.html', categories=mongo.db.categories.find(), isNav=True)


# Sign-in/login page
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if user:
            password = bcrypt.hashpw(request.form['password'].encode('utf-8'),
                                     user['password'])
            if password == user['password']:
                session['username'] = request.form.get("username").lower()
                flash(", great to have you back!")
                return render_template('allrecipe.html', username=session["username"], isFooter=True)

            flash("Incorrect Username or Password!")
            return redirect(url_for("login", isFooter=True))

    return render_template('login.html', isFooter=True, isNav=True)


# logout route
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("index",  isNav=True))


@app.route('/about')
def about():
    return render_template('about.html', recipes=mongo.db.recipes.find(), workouts=mongo.db.workouts.find())


@app.route('/recipes/<category>')
def recipes(category):
    # if statements to display the recipes base on category name
    if category == "Pre Workout Meal":
        recipe = mongo.db.recipes.find({"category_name": "Pre Workout Meal"})
    elif category == "Post Workout Meal":
        recipe = mongo.db.recipes.find({"category_name": "Post Workout Meal"})
    else:
        recipe = mongo.db.recipes.find()

    return render_template('allrecipe.html', recipe=recipe, category_title=category, recipes=mongo.db.recipes.find(), isFooter=True)

# ---- SEARCH ----- #


@app.route('/search/<recipe_name>')
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


@app.route('/recipe/add')
def add_recipe():
    return render_template('addrecipe.html', categories=mongo.db.categories.find(), isFooter=True)


@app.route('/recipe/insert', methods=['POST'])
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


@app.route('/recipe/edit/<recipe_id>')
def edit_recipe(recipe_id):
    all_categories = mongo.db.categories.find()
    prerecipes = mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)})
    return render_template('editrecipe.html',
                           recipes=prerecipes, categories=all_categories, isFooter=True)  # to do a find on the categories table.


@app.route('/recipe/update/<recipe_id>', methods=['POST'])
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


@app.route('/recipe/delete/<recipe_id>')
def delete_recipe(recipe_id):
    mongo.db.recipes.remove({'_id': ObjectId(recipe_id)})
    flash("Succesfully deleted the recipe!")
    return render_template('allrecipe.html', isFooter=True)


@app.route('/workouts')
def workouts():
    return render_template('workouts.html', categories=mongo.db.breathe.find(), workouts=mongo.db.workouts.find(), isFooter=True)


if __name__ == '__main__':

    app.run(host=os.environ.get('IP', '0.0.0.0'),
            port=int(os.environ.get('PORT', '5000')),
            debug=os.environ.get("DEBUG"))
