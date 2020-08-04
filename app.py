import os
if os.path.exists("env.py"):
    import env
from flask import Flask, render_template, redirect, request, url_for, session, flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import bcrypt

app = Flask(__name__)

# Set connection to MongoDB
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')


mongo = PyMongo(app)


# Home page
@app.route('/')
def index():
    """
    Renders the home page for the website.
    """
    return render_template('Pages/index.html', isNav=True)


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

    return render_template('Pages/register.html', categories=mongo.db.categories.find(), isNav=True)


# login page
@app.route('/login', methods=["GET", "POST"])
def login():
    """
    Renders sign-in page and checks multiple username.
    """
    if request.method == 'POST':
        user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if user:
            password = bcrypt.hashpw(request.form['password'].encode('utf-8'),
                                     user['password'])
            if password == user['password']:
                session['username'] = request.form.get("username").lower()
                flash(", great to have you back!")
                return render_template('Pages/allrecipe.html', username=session["username"], isFooter=True)

            flash("Incorrect Username or Password!")
            return redirect(url_for("login", isFooter=True))

    return render_template('Pages/login.html', isFooter=True, isNav=True)


# logout route
@app.route('/logout')
def logout():
    """
    Renders the users logout and clears the session of the user.
    """
    session.clear()
    return redirect(url_for("index"))


# recipe menu
@app.route('/recipes/<category>')
def recipes(category):
    """
    show and filter the recipe by their categories.
    """
    # if statements to display the recipes base on category name
    if category == "Pre Workout Meal":
        recipe = mongo.db.recipes.find({"category_name": "Pre Workout Meal"})
    elif category == "Post Workout Meal":
        recipe = mongo.db.recipes.find({"category_name": "Post Workout Meal"})
    else:
        recipe = mongo.db.recipes.find()

    return render_template('Pages/allrecipe.html', recipe=recipe, category_title=category, recipes=mongo.db.recipes.find(), isFooter=True)


# search recipe
@app.route('/search', methods=["GET", "POST"])
def search():
    """
    Search recipe by name.
    """
    search = request.form.get("search")
    results = mongo.db.recipes.find({"$text": {"$search": search}}).limit(2)
    result_count = mongo.db.recipes.find(
        {"$text": {"$search": search}}).count()
    if result_count > 0:
        return render_template("Pages/search.html", results=results, search=search, isFooter=True)
    else:
        flash("No results found.")
        return render_template("Pages/search.html", results=results, search=search, isFooter=True)


# Add recipe
@app.route('/recipe/add', methods=['GET', 'POST'])
def add_recipe():
    """
    Add recipe into the database.
    """
    if request.method == "POST":
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
        return render_template('Pages/allrecipe.html', isFooter=True)

    return render_template('Pages/addrecipe.html', categories=mongo.db.categories.find(), isFooter=True)


# Recipe page
@app.route('/recipe/<recipe_id>')
def get_recipe(recipe_id):
    """
    Renders the recips page and getting recipe information from the database.
    """
    recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    return render_template("Pages/recipe.html", recipe=recipe, isFooter=True)


# Edit recipe
@app.route('/recipe/edit/<recipe_id>', methods=['GET', 'POST'])
def update_recipe(recipe_id):
    """
    Renders edit page and handles editing of user recipe in the database.
    """
    if request.method == "POST":
        recipes = mongo.db.recipes

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
        return render_template('Pages/allrecipe.html', isFooter=True)

    all_categories = mongo.db.categories.find()
    prerecipes = mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)})
    return render_template('Pages/editrecipe.html',
                           recipes=prerecipes, categories=all_categories, isFooter=True)  # to do a find on the categories table.


# Delete recipe
@app.route('/recipe/delete/<recipe_id>')
def delete_recipe(recipe_id):
    """
    Removes recipe from the database.
    """
    mongo.db.recipes.remove({'_id': ObjectId(recipe_id)})
    flash("Succesfully deleted the recipe!")
    return render_template('Pages/allrecipe.html', isFooter=True)


# contact page
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """
    Renders the contact page.
    """
    if request.method == "POST":
        flash("{}, Thank you for getting in touch! We appreciate you contacting us, one of our colleagues will get back in touch with you soon! Have a great day!".format(
            request.form["name"]))

    return render_template('Pages/contact.html', isFooter=True)


# 404 page
@app.errorhandler(404)
def page_not_found(error):
    """
    Renders an error page with 404 message.
    """
    error_message = str(error)
    return render_template('error-pages/404-page.html', error_message=error_message, isFooter=True), 404


# 500 page
@app.errorhandler(500)
def server_error(error):
    """
    Renders an error page with 500 message.
    """
    error_message = str(error)
    return render_template('error-pages/500-page.html', error_message=error_message, isFooter=True), 500


if __name__ == '__main__':

    app.run(host=os.environ.get('IP', '0.0.0.0'),
            port=int(os.environ.get('PORT', '5000')),
            debug=os.environ.get("DEBUG"))
