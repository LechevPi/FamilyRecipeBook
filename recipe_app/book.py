from flask import Blueprint, render_template
from recipe_app.db_manager import RecipeAndTagManager

# Define the recipes blueprint
bp = Blueprint('book', __name__, url_prefix='/book')

@bp.route('/show')
def show():
    """
    Route to display the recipe book, i.e. the list of recipe
    :return: rendered html page book.html
    """
    try:
        manager = RecipeAndTagManager()
        recipe_list = manager.get_all_recipes_basic_info()
        tag_list = manager.get_all_tags()
        recipe_tags = {r.recipe_name_normalized: r.get_recipe_tags() for r in recipe_list}
        return render_template(
            'book.html',
            recipe_list=recipe_list,
            tag_list=tag_list,
            recipe_tags=recipe_tags)

    except Exception as e:
        return f"An error occurred, we couldn't load this page: {e}", 500  # Generic server error

