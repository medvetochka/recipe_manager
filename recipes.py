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
