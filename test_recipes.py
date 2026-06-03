from recipes import Ingredient


def test_ingredient_creation():
    ingredient = Ingredient("Мука", 500, "г")

    assert ingredient.name == "Мука"
    assert ingredient.quantity == 500.0
    assert ingredient.unit == "г"


def test_ingredient_str():
    ingredient = Ingredient("Мука", 500, "г")

    assert str(ingredient) == "Мука: 500.0 г"


def test_ingredient_eq_same_name_and_unit():
    ingredient_1 = Ingredient("Мука", 500, "г")
    ingredient_2 = Ingredient("Мука", 300, "г")

    assert ingredient_1 == ingredient_2


def test_ingredient_eq_different_name():
    ingredient_1 = Ingredient("Мука", 500, "г")
    ingredient_2 = Ingredient("Сахар", 500, "г")

    assert ingredient_1 != ingredient_2


def test_ingredient_eq_different_unit():
    ingredient_1 = Ingredient("Мука", 500, "г")
    ingredient_2 = Ingredient("Мука", 500, "кг")

    assert ingredient_1 != ingredient_2

import pytest

from recipes import Recipe


def test_recipe_creation():
    flour = Ingredient("Мука", 500, "г")
    cheese = Ingredient("Сыр", 200, "г")

    recipe = Recipe("Пицца", [flour, cheese])

    assert recipe.title == "Пицца"
    assert len(recipe.ingredients) == 2
    assert recipe.ingredients[0] == flour
    assert recipe.ingredients[1] == cheese


def test_recipe_add_new_ingredient():
    flour = Ingredient("Мука", 500, "г")
    recipe = Recipe("Пицца", [flour])

    cheese = Ingredient("Сыр", 200, "г")
    recipe.add_ingredient(cheese)

    assert len(recipe.ingredients) == 2
    assert cheese in recipe.ingredients


def test_recipe_add_existing_ingredient_sums_quantity():
    flour_1 = Ingredient("Мука", 500, "г")
    flour_2 = Ingredient("Мука", 300, "г")

    recipe = Recipe("Пицца", [flour_1])
    recipe.add_ingredient(flour_2)

    assert len(recipe.ingredients) == 1
    assert recipe.ingredients[0].name == "Мука"
    assert recipe.ingredients[0].unit == "г"
    assert recipe.ingredients[0].quantity == 800.0


def test_recipe_scale_returns_new_recipe():
    flour = Ingredient("Мука", 500, "г")
    cheese = Ingredient("Сыр", 200, "г")

    recipe = Recipe("Пицца", [flour, cheese])
    scaled_recipe = recipe.scale(2)

    assert isinstance(scaled_recipe, Recipe)
    assert scaled_recipe is not recipe


def test_recipe_scale_multiplies_quantities():
    flour = Ingredient("Мука", 500, "г")
    cheese = Ingredient("Сыр", 200, "г")

    recipe = Recipe("Пицца", [flour, cheese])
    scaled_recipe = recipe.scale(2)

    assert scaled_recipe.ingredients[0].quantity == 1000.0
    assert scaled_recipe.ingredients[1].quantity == 400.0


def test_recipe_scale_does_not_change_original_recipe():
    flour = Ingredient("Мука", 500, "г")
    cheese = Ingredient("Сыр", 200, "г")

    recipe = Recipe("Пицца", [flour, cheese])
    scaled_recipe = recipe.scale(2)

    assert recipe.ingredients[0].quantity == 500.0
    assert recipe.ingredients[1].quantity == 200.0
    assert scaled_recipe.ingredients[0].quantity == 1000.0
    assert scaled_recipe.ingredients[1].quantity == 400.0


def test_recipe_scale_invalid_ratio():
    flour = Ingredient("Мука", 500, "г")
    recipe = Recipe("Пицца", [flour])

    with pytest.raises(ValueError):
        recipe.scale(0)


def test_recipe_len():
    flour = Ingredient("Мука", 500, "г")
    cheese = Ingredient("Сыр", 200, "г")
    flour_again = Ingredient("Мука", 300, "г")

    recipe = Recipe("Пицца", [flour, cheese, flour_again])

    assert len(recipe) == 2

from recipes import ShoppingList


def test_shopping_list_add_recipe():
    flour = Ingredient("Мука", 500, "г")
    cheese = Ingredient("Сыр", 200, "г")
    recipe = Recipe("Пицца", [flour, cheese])

    shopping_list = ShoppingList()
    shopping_list.add_recipe(recipe, 2)

    result = shopping_list.get_list()

    assert len(result) == 2
    assert result[0].name == "Мука"
    assert result[0].quantity == 1000.0
    assert result[0].unit == "г"
    assert result[1].name == "Сыр"
    assert result[1].quantity == 400.0
    assert result[1].unit == "г"


def test_shopping_list_add_recipe_invalid_portions():
    flour = Ingredient("Мука", 500, "г")
    recipe = Recipe("Пицца", [flour])

    shopping_list = ShoppingList()

    with pytest.raises(ValueError):
        shopping_list.add_recipe(recipe, 0)


def test_shopping_list_remove_recipe():
    flour = Ingredient("Мука", 500, "г")
    cheese = Ingredient("Сыр", 200, "г")
    pizza = Recipe("Пицца", [flour, cheese])

    sugar = Ingredient("Сахар", 100, "г")
    cake = Recipe("Пирог", [sugar])

    shopping_list = ShoppingList()
    shopping_list.add_recipe(pizza, 1)
    shopping_list.add_recipe(cake, 1)

    shopping_list.remove_recipe("Пицца")

    result = shopping_list.get_list()

    assert len(result) == 1
    assert result[0].name == "Сахар"
    assert result[0].quantity == 100.0


def test_shopping_list_remove_missing_recipe_does_nothing():
    flour = Ingredient("Мука", 500, "г")
    recipe = Recipe("Пицца", [flour])

    shopping_list = ShoppingList()
    shopping_list.add_recipe(recipe, 1)

    shopping_list.remove_recipe("Несуществующий рецепт")

    result = shopping_list.get_list()

    assert len(result) == 1
    assert result[0].name == "Мука"
    assert result[0].quantity == 500.0


def test_shopping_list_get_list_sums_same_ingredients():
    flour_1 = Ingredient("Мука", 500, "г")
    pizza = Recipe("Пицца", [flour_1])

    flour_2 = Ingredient("Мука", 300, "г")
    cake = Recipe("Пирог", [flour_2])

    shopping_list = ShoppingList()
    shopping_list.add_recipe(pizza, 2)
    shopping_list.add_recipe(cake, 3)

    result = shopping_list.get_list()

    assert len(result) == 1
    assert result[0].name == "Мука"
    assert result[0].unit == "г"
    assert result[0].quantity == 1900.0


def test_shopping_list_get_list_sorted_by_name():
    cheese = Ingredient("Сыр", 200, "г")
    flour = Ingredient("Мука", 500, "г")
    tomato = Ingredient("Томаты", 100, "г")

    recipe = Recipe("Пицца", [cheese, flour, tomato])

    shopping_list = ShoppingList()
    shopping_list.add_recipe(recipe, 1)

    result = shopping_list.get_list()

    names = [ingredient.name for ingredient in result]

    assert names == ["Мука", "Сыр", "Томаты"]


def test_shopping_list_add_combines_two_lists():
    flour = Ingredient("Мука", 500, "г")
    pizza = Recipe("Пицца", [flour])

    sugar = Ingredient("Сахар", 100, "г")
    cake = Recipe("Пирог", [sugar])

    shopping_list_1 = ShoppingList()
    shopping_list_1.add_recipe(pizza, 1)

    shopping_list_2 = ShoppingList()
    shopping_list_2.add_recipe(cake, 1)

    combined_list = shopping_list_1 + shopping_list_2

    result = combined_list.get_list()

    assert len(result) == 2
    assert result[0].name == "Мука"
    assert result[1].name == "Сахар"


def test_shopping_list_add_does_not_change_original_lists():
    flour = Ingredient("Мука", 500, "г")
    pizza = Recipe("Пицца", [flour])

    sugar = Ingredient("Сахар", 100, "г")
    cake = Recipe("Пирог", [sugar])

    shopping_list_1 = ShoppingList()
    shopping_list_1.add_recipe(pizza, 1)

    shopping_list_2 = ShoppingList()
    shopping_list_2.add_recipe(cake, 1)

    combined_list = shopping_list_1 + shopping_list_2

    result_1 = shopping_list_1.get_list()
    result_2 = shopping_list_2.get_list()
    result_combined = combined_list.get_list()

    assert len(result_1) == 1
    assert result_1[0].name == "Мука"

    assert len(result_2) == 1
    assert result_2[0].name == "Сахар"

    assert len(result_combined) == 2

from recipes import ShoppingList


def test_shopping_list_add_recipe():
    flour = Ingredient("Мука", 500, "г")
    cheese = Ingredient("Сыр", 200, "г")
    recipe = Recipe("Пицца", [flour, cheese])

    shopping_list = ShoppingList()
    shopping_list.add_recipe(recipe, 2)

    result = shopping_list.get_list()

    assert len(result) == 2
    assert result[0].name == "Мука"
    assert result[0].quantity == 1000.0
    assert result[0].unit == "г"
    assert result[1].name == "Сыр"
    assert result[1].quantity == 400.0
    assert result[1].unit == "г"


def test_shopping_list_add_recipe_invalid_portions():
    flour = Ingredient("Мука", 500, "г")
    recipe = Recipe("Пицца", [flour])

    shopping_list = ShoppingList()

    with pytest.raises(ValueError):
        shopping_list.add_recipe(recipe, 0)


def test_shopping_list_remove_recipe():
    flour = Ingredient("Мука", 500, "г")
    cheese = Ingredient("Сыр", 200, "г")
    pizza = Recipe("Пицца", [flour, cheese])

    sugar = Ingredient("Сахар", 100, "г")
    cake = Recipe("Пирог", [sugar])

    shopping_list = ShoppingList()
    shopping_list.add_recipe(pizza, 1)
    shopping_list.add_recipe(cake, 1)

    shopping_list.remove_recipe("Пицца")

    result = shopping_list.get_list()

    assert len(result) == 1
    assert result[0].name == "Сахар"
    assert result[0].quantity == 100.0


def test_shopping_list_remove_missing_recipe_does_nothing():
    flour = Ingredient("Мука", 500, "г")
    recipe = Recipe("Пицца", [flour])

    shopping_list = ShoppingList()
    shopping_list.add_recipe(recipe, 1)

    shopping_list.remove_recipe("Несуществующий рецепт")

    result = shopping_list.get_list()

    assert len(result) == 1
    assert result[0].name == "Мука"
    assert result[0].quantity == 500.0


def test_shopping_list_get_list_sums_same_ingredients():
    flour_1 = Ingredient("Мука", 500, "г")
    pizza = Recipe("Пицца", [flour_1])

    flour_2 = Ingredient("Мука", 300, "г")
    cake = Recipe("Пирог", [flour_2])

    shopping_list = ShoppingList()
    shopping_list.add_recipe(pizza, 2)
    shopping_list.add_recipe(cake, 3)

    result = shopping_list.get_list()

    assert len(result) == 1
    assert result[0].name == "Мука"
    assert result[0].unit == "г"
    assert result[0].quantity == 1900.0


def test_shopping_list_get_list_sorted_by_name():
    cheese = Ingredient("Сыр", 200, "г")
    flour = Ingredient("Мука", 500, "г")
    tomato = Ingredient("Томаты", 100, "г")

    recipe = Recipe("Пицца", [cheese, flour, tomato])

    shopping_list = ShoppingList()
    shopping_list.add_recipe(recipe, 1)

    result = shopping_list.get_list()

    names = [ingredient.name for ingredient in result]

    assert names == ["Мука", "Сыр", "Томаты"]


def test_shopping_list_add_combines_two_lists():
    flour = Ingredient("Мука", 500, "г")
    pizza = Recipe("Пицца", [flour])

    sugar = Ingredient("Сахар", 100, "г")
    cake = Recipe("Пирог", [sugar])

    shopping_list_1 = ShoppingList()
    shopping_list_1.add_recipe(pizza, 1)

    shopping_list_2 = ShoppingList()
    shopping_list_2.add_recipe(cake, 1)

    combined_list = shopping_list_1 + shopping_list_2

    result = combined_list.get_list()

    assert len(result) == 2
    assert result[0].name == "Мука"
    assert result[1].name == "Сахар"


def test_shopping_list_add_does_not_change_original_lists():
    flour = Ingredient("Мука", 500, "г")
    pizza = Recipe("Пицца", [flour])

    sugar = Ingredient("Сахар", 100, "г")
    cake = Recipe("Пирог", [sugar])

    shopping_list_1 = ShoppingList()
    shopping_list_1.add_recipe(pizza, 1)

    shopping_list_2 = ShoppingList()
    shopping_list_2.add_recipe(cake, 1)

    combined_list = shopping_list_1 + shopping_list_2

    result_1 = shopping_list_1.get_list()
    result_2 = shopping_list_2.get_list()
    result_combined = combined_list.get_list()

    assert len(result_1) == 1
    assert result_1[0].name == "Мука"

    assert len(result_2) == 1
    assert result_2[0].name == "Сахар"

    assert len(result_combined) == 2
