# Loading python modules
import os
from flask import Flask, render_template
from flask_basicauth import BasicAuth
from recipe_app.db_manager import RecipeAndTagManager

# Loading password config
from instance.pw import admin_password, admin_username

def create_app():

    # Initialization of the app with relative configuration folder named "instance"
    application = Flask(__name__, instance_relative_config=True)

    # App configuration
    application.config.from_mapping(
        DATABASE=os.path.join(application.instance_path, 'recipe_app.sqlite'),  # Path to SQLite database file
        BASIC_AUTH_USERNAME = admin_password,
        BASIC_AUTH_PASSWORD = admin_username,
        BASIC_AUTH_FORCE = True,
        UPLOAD_FOLDER = "upload_folder"
    )

    # Creation of the basic authentification object
    basic_auth = BasicAuth(application)

    # importing the database
    from .db import init_app
    init_app(application)  # Initialize database connection

    # Registering the recipes blueprint
    from . import recipe
    application.register_blueprint(recipe.bp)

    # Registering the book blueprint
    from . import book
    application.register_blueprint(book.bp)

    @application.route('/view_recipe_astable')
    def view_recipe_astable():
        # for development
        Manager = RecipeAndTagManager()
        recipes = Manager.get_all_recipes_detailed()
        return render_template('view_recipe.html', recipes=recipes)

    @application.route('/view_tags_astable')
    def view_tags_astable():
        # for development
        Manager = RecipeAndTagManager()
        tags = Manager.get_all_tags()
        return render_template('view_tags.html', tags=tags)

    # Starting page
    @application.route('/')
    def welcome():
        # First page of the app
        Manager = RecipeAndTagManager()
        last_recipe = Manager.get_last_recipe_basic_info()
        recipe_tags = last_recipe.get_recipe_tags()
        print([(t.tag_name, t.order) for t in Manager.get_all_tags()])
        return render_template('welcome.html', last_recipe=last_recipe, recipe_tags=recipe_tags)

    return application