DROP TABLE IF EXISTS recipe;

CREATE TABLE recipe (
    id                              INTEGER     PRIMARY KEY AUTOINCREMENT,
    recipe_name                     TEXT        UNIQUE NOT NULL,
    recipe_name_normalized          TEXT        UNIQUE NOT NULL,
    date_add                        TEXT        NOT NULL,
    for_x_servings                  TEXT        NOT NULL,
    category                        TEXT        NOT NULL,
    category_normalized             TEXT        NOT NULL,
    time_prep                       INTEGER     NOT NULL,
    time_rest                       INTEGER     NOT NULL,
    time_cook                       INTEGER     NOT NULL,
    time_tot                        INTEGER     NOT NULL,
    ingredient                      TEXT        NOT NULL,
    utensil                         TEXT        NOT NULL,
    steps                           TEXT        NOT NULL,
    tips                            TEXT                ,
    author                          TEXT        NOT NULL,
    description                     TEXT                ,
    img_path                        TEXT        NOT NULL
);

-- Add a table to store tags
DROP TABLE IF EXISTS tag;

CREATE TABLE tag (
  id            INTEGER     PRIMARY KEY AUTOINCREMENT,
  tag_name          TEXT        UNIQUE NOT NULL,
  tag_name_normalized       TEXT        UNIQUE NOT NULL
);

-- Create a table to represent the many-to-many relationship between recipes and tags
DROP TABLE IF EXISTS recipe_tag;

CREATE TABLE recipe_tag (
  recipe_id INTEGER,
  tag_id INTEGER,
  FOREIGN KEY(recipe_id) REFERENCES recipe(id),
  FOREIGN KEY(tag_id) REFERENCES tag(id),
  PRIMARY KEY (recipe_id, tag_id)
);

-- Insert test data for recipes
INSERT INTO recipe (recipe_name, recipe_name_normalized, date_add, for_x_servings, category, category_normalized, time_prep, time_rest, time_cook, time_tot, ingredient, utensil, steps, tips, author, description, img_path)
VALUES ('Margarita Pizza', 'margarita_pizza', '2024-03-15', '4', 'Entrée', 'entree', 20, 60, 15, 95, 'pizza dough_1_pc;;tomato sauce_200_ml;;mozzarella cheese_100_g;;basil_3_leaves', 'oven;;pizza stone', 'Preheat oven to 475°F;;Roll out dough and spread sauce;;Add cheese and basil;;Bake until crust is golden.', 'Serve hot with a sprinkle of red pepper flakes.', 'Justine', 'A classic Italian favorite that everyone loves.', '/static/img/recipe_default.jpg');

INSERT INTO recipe (recipe_name, recipe_name_normalized, date_add, for_x_servings, category, category_normalized, time_prep, time_rest, time_cook, time_tot, ingredient, utensil, steps, tips, author, description, img_path)
VALUES ('Pasta Carbonara', 'pasta_carbonara', '2024-03-16', '2', 'Plat principal', 'plat_principal', 10, 0, 15, 25, 'spaghetti_200_g;;eggs_2;;bacon_100_g;;Parmesan cheese_50_g;;black pepper', 'pan;;pot', 'Cook spaghetti;;Cook bacon;;Beat eggs and mix with cheese;;Combine everything;;Serve hot with black pepper.', 'Garnish with parsley.', 'Pierre', 'A delicious Italian pasta dish with creamy sauce.', '/static/img/img_recipe/pasta_carbonara.png');

-- Insert test data for recipes
INSERT INTO recipe (recipe_name, recipe_name_normalized, date_add, for_x_servings, category, category_normalized, time_prep, time_rest, time_cook, time_tot, ingredient, utensil, steps, tips, author, description, img_path)
VALUES ('Calzone Pizza', 'calzone_pizza', '2024-03-15', '4', 'Entrée', 'entree', 20, 60, 15, 95, 'pizza dough_1_pc;;tomato sauce_200_ml;;mozzarella cheese_100_g;;basil_3_leaves', 'oven;;pizza stone', 'Preheat oven to 475°F;;Roll out dough and spread sauce;;Add cheese and basil;;Bake until crust is golden.', 'Serve hot with a sprinkle of red pepper flakes.', 'Justine', 'A classic Italian favorite that everyone loves.', '/static/img/recipe_default.jpg');

INSERT INTO recipe (recipe_name, recipe_name_normalized, date_add, for_x_servings, category, category_normalized, time_prep, time_rest, time_cook, time_tot, ingredient, utensil, steps, tips, author, description, img_path)
VALUES ('Quiche', 'quiche', '2024-03-16', '2', 'Plat principal', 'plat_principal', 10, 0, 15, 25, 'spaghetti_200_g;;eggs_2;;bacon_100_g;;Parmesan cheese_50_g;;black pepper', 'pan;;pot', 'Cook spaghetti;;Cook bacon;;Beat eggs and mix with cheese;;Combine everything;;Serve hot with black pepper.', 'Garnish with parsley.', 'Pierre', 'A delicious Italian pasta dish with creamy sauce.', '/static/img/img_recipe/pasta_carbonara.png');

-- Insert test data for recipes
INSERT INTO recipe (recipe_name, recipe_name_normalized, date_add, for_x_servings, category, category_normalized, time_prep, time_rest, time_cook, time_tot, ingredient, utensil, steps, tips, author, description, img_path)
VALUES ('Bolo', 'bolo', '2024-03-15', '4', 'Entrée', 'entree', 20, 60, 15, 95, 'pizza dough_1_pc;;tomato sauce_200_ml;;mozzarella cheese_100_g;;basil_3_leaves', 'oven;;pizza stone', 'Preheat oven to 475°F;;Roll out dough and spread sauce;;Add cheese and basil;;Bake until crust is golden.', 'Serve hot with a sprinkle of red pepper flakes.', 'Justine', 'A classic Italian favorite that everyone loves.', '/static/img/recipe_default.jpg');

INSERT INTO recipe (recipe_name, recipe_name_normalized, date_add, for_x_servings, category, category_normalized, time_prep, time_rest, time_cook, time_tot, ingredient, utensil, steps, tips, author, description, img_path)
VALUES ('Croque monsieur', 'croque_monsieur', '2024-03-16', '2', 'Plat principal', 'plat_principal', 10, 0, 15, 25, 'spaghetti_200_g;;eggs_2;;bacon_100_g;;Parmesan cheese_50_g;;black pepper', 'pan;;pot', 'Cook spaghetti;;Cook bacon;;Beat eggs and mix with cheese;;Combine everything;;Serve hot with black pepper.', 'Garnish with parsley.', 'Pierre', 'A delicious Italian pasta dish with creamy sauce.', '/static/img/img_recipe/pasta_carbonara.png');

-- Insert test data for recipes
INSERT INTO recipe (recipe_name, recipe_name_normalized, date_add, for_x_servings, category, category_normalized, time_prep, time_rest, time_cook, time_tot, ingredient, utensil, steps, tips, author, description, img_path)
VALUES ('Salade', 'salade', '2024-03-15', '4', 'Entrée', 'entree', 20, 60, 15, 95, 'pizza dough_1_pc;;tomato sauce_200_ml;;mozzarella cheese_100_g;;basil_3_leaves', 'oven;;pizza stone', 'Preheat oven to 475°F;;Roll out dough and spread sauce;;Add cheese and basil;;Bake until crust is golden.', 'Serve hot with a sprinkle of red pepper flakes.', 'Justine', 'A classic Italian favorite that everyone loves.', '/static/img/recipe_default.jpg');

INSERT INTO recipe (recipe_name, recipe_name_normalized, date_add, for_x_servings, category, category_normalized, time_prep, time_rest, time_cook, time_tot, ingredient, utensil, steps, tips, author, description, img_path)
VALUES ('Poulet curry super long name', 'poulet_curry_super_long_name', '2024-03-16', '2', 'Plat principal', 'plat_principal', 10, 0, 15, 25, 'spaghetti_200_g;;eggs_2;;bacon_100_g;;Parmesan cheese_50_g;;black pepper', 'pan;;pot', 'Cook spaghetti;;Cook bacon;;Beat eggs and mix with cheese;;Combine everything;;Serve hot with black pepper.', 'Garnish with parsley.', 'Pierre', 'A delicious Italian pasta dish with creamy sauce.', '/static/img/img_recipe/pasta_carbonara.png');

-- Insert test data for tags
INSERT INTO tag (tag_name, tag_name_normalized) VALUES
  ('Entrée', 'entree'),
  ('Plat principal', 'plat_principal'),
  ('Dessert', 'dessert'),
  ('Apéritif', 'aperitif'),
  ('Boisson', 'boisson'),
  ('Base culinaire', 'base_culinaire');


-- Insert test data for recipe-tag relationships
INSERT INTO recipe_tag (recipe_id, tag_id) VALUES
  (1, 1),
  (2, 2),
  (3, 3),
  (4, 4),
  (5, 5),
  (7, 5),
  (8, 1),
  (6, 6);