class Unit:
    """Information about a single unit."""

    def __init__(self, plural_name, singular_name, aliases):
        self.plural_name = plural_name
        self.singular_name = singular_name
        self.aliases = aliases

    def __str__(self):
        return f"Unit(singular={self.singular_name}, plural={self.plural_name}, aliases={self.aliases})"

    def __repr__(self):
        return str(self)

    # Note: there's no need for a custom hash implementation since we only ever create a single instance of each unit


class Conversion:
    """Information about a single conversion between two units, used as links in the graph."""

    def __init__(self, from_amount, from_unit, to_amount, to_unit):
        self.from_amount = from_amount
        self.from_unit = from_unit
        self.to_amount = to_amount
        self.to_unit = to_unit

        self.factor = self.to_amount / self.from_amount

    def __str__(self):
        return f"Conversion(from=({self.from_amount}, {self.from_unit.plural_name}), to=({self.to_amount}, {self.to_unit.plural_name}))"

    def __repr__(self):
        return str(self)

    def convert(self, amount):
        return amount * self.factor
