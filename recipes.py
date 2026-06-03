class Ingredient:
    def init(self, name, quantity, unit):
        self.name = name
        self.quantity = quantity
        self.unit = unit

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        value = float(value)

        if value <= 0:
            raise ValueError("количество должно быть положительным")

        self._quantity = value

    def str(self):
        return f"{self.name}: {self.quantity} {self.unit}"

    def repr(self):
        return f"Ingredient('{self.name}', {self.quantity}, '{self.unit}')"

    def eq(self, other):
        if not isinstance(other, Ingredient):
            return False

        return self.name == other.name and self.unit == other.unit
class Recipe:
    def init(self, title, ingredients):
        self.title = title
        self.ingredients = []

        for ingredient in ingredients:
            self.add_ingredient(ingredient)

    def add_ingredient(self, ingredient):
        for existing_ingredient in self.ingredients:
            if existing_ingredient == ingredient:
                existing_ingredient.quantity += ingredient.quantity
                return

        self.ingredients.append(ingredient)

    @staticmethod
    def is_valid_ratio(ratio):
        try:
            ratio = float(ratio)
        except (TypeError, ValueError):
            return False

        return ratio > 0

    def scale(self, ratio):
        if not self.is_valid_ratio(ratio):
            raise ValueError("коэффициент должен быть положительным числом")

        ratio = float(ratio)
        scaled_ingredients = []

        for ingredient in self.ingredients:
            scaled_ingredients.append(
                Ingredient(
                    ingredient.name,
                    ingredient.quantity * ratio,
                    ingredient.unit
                )
            )

        return Recipe(self.title, scaled_ingredients)

    def len(self):
        return len(self.ingredients)

    def str(self):
        result = f"{self.title}\n"

        for ingredient in self.ingredients:
            result += f"- {ingredient}\n"

        return result.strip()
class DietaryRecipe(Recipe):
    def init(self, title, diet_type, ingredients=None):
        if ingredients is None:
            ingredients = []

        super().init(title, ingredients)
        self.diet_type = diet_type

    def scale(self, ratio):
        scaled_recipe = super().scale(ratio)

        return DietaryRecipe(
            self.title,
            self.diet_type,
            scaled_recipe.ingredients
        )

    def str(self):
        parent_str = super().str()
        return f"[{self.diet_type}] {parent_str}"
