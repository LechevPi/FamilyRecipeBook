from recipe_app.db import get_db, close_db
from datetime import datetime
from recipe_app.utility_function import _convert_to_alphanumeric_lowercase, _convert_to_png_and_save, _normalize_name_string

def _read_db(query: str, fetch: str = 'all', params=None):
    """
    Reading a database query
    :param query:
    :param fetch:
    :param params:
    :return:
    """
    db_conn = get_db()
    cursor = db_conn.cursor()

    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)

    if fetch == 'all':
        result = cursor.fetchall()
    elif fetch == 'one':
        result = cursor.fetchone()
    else:
        raise(ValueError, f"The fetch argument \"{fetch}\" is not available")

    close_db()

    return result

class Tag:
    def __init__(self, tag_name_normalized):
        query = """SELECT * FROM tag WHERE tag_name_normalized = ?"""
        self.id, self.tag_name, self.tag_name_normalized = \
            _read_db(query=query, fetch='one', params=(tag_name_normalized,))

class FakeTag:
    def __init__(self):
        self.id, self.tag_name, self.tag_name_normalized = \
            99999, ' ', ' '

class RecipeBasicInfo:
    def __init__(self, recipe_name_normalized):
        query = """SELECT id, recipe_name, recipe_name_normalized, time_tot, img_path  FROM recipe WHERE recipe_name_normalized = ?"""
        result = _read_db(query=query, fetch='one', params=(recipe_name_normalized,))
        self.id = result[0]
        self.recipe_name = result[1]
        self.recipe_name_normalized = result[2]
        self.time_tot = result[3]
        self.img_path = result[4]

    def get_recipe_tags(self):
        query = """
                SELECT t.tag_name_normalized
                FROM recipe r
                JOIN recipe_tag rt ON r.id = rt.recipe_id
                JOIN tag t ON rt.tag_id = t.id
                WHERE r.recipe_name_normalized = ?
                ORDER BY t.tag_name;
            """
        rows = _read_db(query=query, fetch='all', params=(self.recipe_name_normalized,))
        tag_list = []
        for row in rows:
            tag_list.append(Tag(tag_name_normalized=row[0]))

        self.recipe_tags = tag_list
        return tag_list

class RecipeDetailed(RecipeBasicInfo):
    def __init__(self, recipe_name_normalized):
        query = """SELECT *  FROM recipe WHERE recipe_name_normalized = ?"""
        result = _read_db(query=query, fetch='one', params=(recipe_name_normalized,))
        self.id = result[0]
        self.recipe_name = result[1]
        self.recipe_name_normalized = result[2]
        self.date_add = result[3]
        self.for_x_servings = result[4]
        self.category = result[5]
        self.category_normalized = result[6]
        self.time_prep = result[7]
        self.time_rest = result[8]
        self.time_cook = result[9]
        self.time_tot = result[10]
        self.ingredient = result[11]
        self.utensil = result[12]
        self.steps = result[13]
        self.tips = result[14]
        self.author = result[15]
        self.description = result[16]
        self.img_path = result[17]

class RecipeAndTagManager:
    def __init__(self):
        query1 = "SELECT recipe_name_normalized FROM recipe ORDER BY date_add"
        self.available_recipes = [row[0] for row in _read_db(query=query1, fetch='all')]
        query2 = "SELECT tag_name_normalized FROM tag ORDER BY tag_name_normalized"
        self.available_tags = [row[0] for row in _read_db(query=query2, fetch='all')]

    def get_all_tags(self):
        tag_list = []
        for (i, tag_name_normalized) in enumerate(self.available_tags):
            t = Tag(tag_name_normalized=tag_name_normalized)
            t.order = i+1
            tag_list.append(t)
        return tag_list

    def get_all_recipes_basic_info(self):
        recipe_list = []
        for recipe_name_normalized in self.available_recipes:
            recipe_list.append(RecipeBasicInfo(recipe_name_normalized=recipe_name_normalized))
        return recipe_list

    def get_all_recipes_detailed(self):
        recipe_list = []
        for recipe_name_normalized in self.available_recipes:
            recipe_list.append(RecipeDetailed(recipe_name_normalized=recipe_name_normalized))
        return recipe_list

    def get_recipe_basic_info(self, recipe_name_normalized):
        return RecipeBasicInfo(recipe_name_normalized=recipe_name_normalized)

    def get_recipe_detailed(self, recipe_name_normalized):
        return RecipeDetailed(recipe_name_normalized=recipe_name_normalized)

    def get_last_recipe_basic_info(self):
        return RecipeDetailed(recipe_name_normalized=self.available_recipes[-1])

    def add_new_recipe_and_get_name_str(self, request):

        d = _read_add_recipe_form(request=request)

        db_conn = get_db()
        cursor = db_conn.cursor()

        try:
            # 1. Handling the image first to get the image path
            recipe_image = request.files['recipe_image']
            if recipe_image.filename != '':
                img_path = _convert_to_png_and_save(d['recipe_name_normalized'], recipe_image)
            else:
                img_path = '/static/img/recipe_default.jpg'

            # 2. Adding the recipe and getting the recipe id
            cursor.execute(
                "INSERT INTO recipe "
                "(recipe_name, recipe_name_normalized, date_add, for_x_servings, category, category_normalized, time_prep, time_rest, time_cook, time_tot,"
                "ingredient, utensil, steps, tips, author, description, img_path) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (d['recipe_name'], d['recipe_name_normalized'], d['dt'], d['for_x_servings'], d['category'], d['category_normalized'], d['time_prep'],
                 d['time_rest'],d['time_cook'], d['time_tot'], d['ingredients_str'], d['utensils'], d['steps'],
                 d['tips'], d['author'], d['description'], img_path))

            recipe_id = cursor.lastrowid  # Get the ID of the newly inserted recipe

            # 3. Adding the tags
            tag_ids = []

            # Insert tags into the tag table if they don't exist
            for tag in d['tag_list']:

                tag_name = _normalize_name_string(tag)
                tag_name_normalized = _convert_to_alphanumeric_lowercase(tag)
                cursor.execute("INSERT OR IGNORE INTO tag (tag_name, tag_name_normalized) VALUES (?, ?)", (tag_name, tag_name_normalized))
                db_conn.commit()

                cursor.execute("SELECT id FROM tag WHERE tag_name_normalized = ?", (tag_name_normalized,))
                tag_id = cursor.fetchone()[0]
                tag_ids.append(tag_id)


            # Associate recipe with tags in the recipe_tag table
            for tag_id in tag_ids:
                cursor.execute("INSERT OR IGNORE INTO recipe_tag (recipe_id, tag_id) VALUES (?, ?)", (recipe_id, tag_id))
                db_conn.commit()

            db_conn.commit()
            return d['recipe_name_normalized']
        except Exception as e:
            db_conn.rollback()  # Rollback changes if an error occurs
            return f"An error occurred: {e}", 500  # Generic server error
        finally:
            close_db()  # Ensure database connection is closed

    def update_recipe_and_get_name_str(self, request, recipe_name_normalized):

        old_recipe = self.get_recipe_detailed(recipe_name_normalized=recipe_name_normalized)
        old_tags = [tag.tag_name for tag in old_recipe.get_recipe_tags()]

        d = _read_add_recipe_form(request=request)
        db_conn = get_db()
        cursor = db_conn.cursor()

        try:
            # 1. Handling the image first to get the image path
            recipe_image = request.files['recipe_image']
            if recipe_image.filename != '':
                img_path = _convert_to_png_and_save(d['recipe_name_normalized'], recipe_image)
            else:
                img_path = old_recipe.img_path

            # 2. Adding the recipe and getting the recipe id
            cursor.execute(
            "UPDATE recipe SET recipe_name=?, recipe_name_normalized=?, date_add=?, for_x_servings=?, category=?, category_normalized=?, "
            "time_prep=?, time_rest=?, time_cook=?, time_tot=?, ingredient=?, utensil=?, "
            "steps=?, tips=?, author=?, description=?, img_path=? WHERE id=?",
            (d['recipe_name'], d['recipe_name_normalized'], d['dt'], d['for_x_servings'], d['category'], d['category_normalized'],
             d['time_prep'], d['time_rest'], d['time_cook'], d['time_tot'],
             d['ingredients_str'], d['utensils'], d['steps'], d['tips'],
             d['author'], d['description'], img_path, old_recipe.id)
            )

            recipe_id = old_recipe.id

            # 3.1 Adding the new tags
            tag_ids = []

            for tag in d['tag_list']:
                tag_name = _normalize_name_string(tag_name)

                if tag_name not in old_tags:
                    tag_name_normalized = _convert_to_alphanumeric_lowercase(tag)
                    cursor.execute("INSERT OR IGNORE INTO tag (tag_name, tag_name_normalized) VALUES (?, ?)", (tag_name, tag_name_normalized))
                    db_conn.commit()

                    cursor.execute("SELECT id FROM tag WHERE tag_name_normalized = ?", (tag_name_normalized,))
                    tag_id = cursor.fetchone()[0]
                    tag_ids.append(tag_id)

            # Associate recipe with tags in the recipe_tag table
            for tag_id in tag_ids:
                cursor.execute("INSERT OR IGNORE INTO recipe_tag (recipe_id, tag_id) VALUES (?, ?)",
                               (recipe_id, tag_id))
                db_conn.commit()


            # 3.2. Handling deleted tags
            for tag in old_tags:
                if tag not in d['tag_list']:
                    tag_id = cursor.execute("SELECT id FROM tag WHERE tag_name = ?", (tag_name,)).fetchone()[0]
                    cursor.execute("DELETE FROM recipe_tag WHERE recipe_id = ? AND tag_id = ?", (recipe_id, tag_id))
                    db_conn.commit()

            #3.3 remove useless tags

            # Get the list of tag_ids that are used in recipe_tag
            cursor.execute("SELECT DISTINCT tag_id FROM recipe_tag")
            used_tag_ids = [row[0] for row in cursor.fetchall()]

            # Get all tag_ids from the tag table
            cursor.execute("SELECT id FROM tag")
            all_tag_ids = [row[0] for row in cursor.fetchall()]

            # Find the tag_ids that are not used
            unused_tag_ids = set(all_tag_ids) - set(used_tag_ids)

            # Delete unused tags from the tag table
            for tag_id in unused_tag_ids:
                cursor.execute("DELETE FROM tag WHERE id = ?", (tag_id,))

            db_conn.commit()
            return d['recipe_name_normalized']
        except Exception as e:
            db_conn.rollback()  # Rollback changes if an error occurs
            return f"An error occurred: {e}", 500  # Generic server error
        finally:
            close_db()  # Ensure database connection is closed

def _read_add_recipe_form(request):
    cat_dict = {
        'entree': 'Entrée', 'aperitif': 'Apéritif', 'plat_principal': 'Plat principal',
        'dessert': 'Dessert', 'boisson': 'Boisson', 'base_culinaire': 'Base culinaire'
    }


    # retrieving all necessary information from the add_recipe.html form
    name = _normalize_name_string(request.form['recipe_name'])
    name_str = _convert_to_alphanumeric_lowercase(name)
    dt = datetime.today().strftime('%Y-%m-%d')
    for_x_servings = request.form['for_x_servings']
    cat_str = request.form['category']
    cat = cat_dict[cat_str]
    time_prep = request.form['time_prep']
    time_rest = request.form['time_rest']
    time_cook = request.form['time_cook']
    time_tot = int(time_prep) + int(time_rest) + int(time_cook)
    ingredient_names = request.form.getlist('ingredient_name[]')
    ingredient_quantities = request.form.getlist('ingredient_quantity[]')
    ingredient_units = request.form.getlist('ingredient_unit[]')

    ingredients = []
    for ingr, quantity, unit in zip(ingredient_names, ingredient_quantities, ingredient_units):
        ingredient = f"{ingr}_{quantity}_{unit}"
        ingredients.append(ingredient)

    ingredients_str = ";;".join(ingredients)
    utensils = ";;".join(request.form.getlist('utensils'))  # Join list of utensils into a string
    steps = ";;".join(request.form.getlist('steps'))  # Join list of steps into a string
    tips = ";;".join(request.form.getlist('tips'))  # Join list of tips into a string
    author = request.form['author']
    description = _normalize_name_string(request.form['recipe_description'])

    tag_list = request.form.getlist('tags')
    tag_list = [_normalize_name_string(tag) for tag in tag_list if (_convert_to_alphanumeric_lowercase(tag) != '')]
    tag_list.append(cat)

    return {
        'recipe_name': name,
        'recipe_name_normalized': name_str,
        'dt': dt,
        'for_x_servings': for_x_servings,
        'category': cat,
        'category_normalized': cat_str,
        'time_prep': time_prep,
        'time_rest': time_rest,
        'time_cook': time_cook,
        'time_tot': time_tot,
        'ingredients_str': ingredients_str,
        'utensils': utensils,
        'steps': steps,
        'tips': tips,
        'author': author,
        'description': description,
        'tag_list': tag_list,
    }

