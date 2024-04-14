### Python codes to handle recipe: view, add and modify

from flask import Blueprint, render_template, redirect, request
from .db_manager import RecipeAndTagManager, FakeTag

# Define the recipes blueprint
bp = Blueprint('recipe', __name__, url_prefix='/recipe')

# Route to view a specific recipe
@bp.route('/<string:recipe_name_normalized>')
def view_recipe(recipe_name_normalized):
    try:
        Manager = RecipeAndTagManager()
        recipe = Manager.get_recipe_detailed(recipe_name_normalized=recipe_name_normalized)
        recipe_tags = recipe.get_recipe_tags()

        if recipe:
            return render_template('recipe.html', recipe=recipe, recipe_tags=recipe_tags)
        else:
            return "Recipe not found", 404  # Recipe not found error
    except Exception as e:
        return f"An error occurred: {e}", 500  # Generic server error


@bp.route('/add_recipe', methods=['GET'])
def add_recipe_form():
    Manager = RecipeAndTagManager()
    existing_recipe_names = [recipe.recipe_name_normalized for recipe in Manager.get_all_recipes_basic_info()]
    available_tags = Manager.get_all_tags()

    available_tags = [
        tag for tag in available_tags if tag.tag_name not in [
            'Entrée', 'Apéritif', 'Plat principal', 'Dessert', 'Boisson', 'Base culinaire'
        ]
    ]

    return render_template(
        'add_recipe.html',
        existing_recipe_names=existing_recipe_names,
        available_tags=available_tags
    )


@bp.route('/add_recipe', methods=['POST'])
def add_recipe():
    manager = RecipeAndTagManager()
    recipe_name_normalized = manager.add_new_recipe_and_get_name_str(request=request)
    return redirect(f"/recipe/thank_you/{recipe_name_normalized}")  # Redirect to add recipe form

@bp.route('/thank_you/<string:recipe_name_normalized>', methods=['GET'])
def thank_you(recipe_name_normalized):
    return render_template('thank_you.html', recipe_name_normalized=recipe_name_normalized)

@bp.route('/modify_recipe/<string:recipe_name_normalized>', methods=['GET'])
def modify_recipe_form(recipe_name_normalized):
    Manager = RecipeAndTagManager()

    recipe = Manager.get_recipe_detailed(recipe_name_normalized=recipe_name_normalized)
    recipe_tags = recipe.get_recipe_tags()

    recipe_tags = [
        tag for tag in recipe_tags if tag.tag_name not in [
            'Entrée', 'Apéritif', 'Plat principal','Dessert', 'Boisson', 'Base culinaire'
        ]
    ]

    if recipe_tags == []:
        recipe_tags = [FakeTag]

    for (i, tag) in enumerate(recipe_tags):
        tag.nr = i+1

    existing_recipe_names = Manager.available_recipes
    existing_recipe_names = [name for name in existing_recipe_names if name != recipe_name_normalized]

    available_tags = Manager.get_all_tags()
    available_tags = [
        tag for tag in available_tags if tag.tag_name not in [
            'Entrée', 'Apéritif', 'Plat principal', 'Dessert', 'Boisson', 'Base culinaire'
        ]
    ]

    if recipe:
        # Render the modify_recipe.html template with recipe details
        return render_template(
            'modify_recipe.html',
            recipe=recipe,
            existing_recipe_names=existing_recipe_names,
            available_tags=available_tags,
            recipe_tags=recipe_tags
        )

    else:
        # Handle case where recipe_id is not found
        return "Recipe not found", 404

@bp.route('/modify_recipe/<string:recipe_name_normalized>', methods=['POST'])
def modify_recipe(recipe_name_normalized):
    manager = RecipeAndTagManager()
    recipe_name_normalized = manager.update_recipe_and_get_name_str(request=request, recipe_name_normalized=recipe_name_normalized)
    return redirect(f"/recipe/thank_you/{recipe_name_normalized}")  # Redirect to add recipe form


