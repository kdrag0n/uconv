import abc


class TupleHash(abc.ABC):
    @abc.abstractmethod
    def to_tuple(self):
        pass

    def __hash__(self):
        return hash(self.to_tuple())

    def __eq__(self, other):
        return self.to_tuple() == other.to_tuple()


class Unit(TupleHash):
    """Information about a single unit."""

    def __init__(self, plural_name, singular_name, aliases):
        self.plural_name = plural_name
        self.singular_name = singular_name
        self.aliases = tuple(aliases)

    def __str__(self):
        return self.plural_name

    def __repr__(self):
        return f"Unit(singular={self.singular_name}, plural={self.plural_name}, aliases={self.aliases})"

    def render(self, amount):
        name = self.singular_name if amount == 1 else self.plural_name
        amount_val = int(amount) if amount.is_integer() else amount
        return f"{amount_val:n} {name}"

    def to_tuple(self):
        return self.singular_name, self.plural_name, self.aliases


class Conversion(TupleHash):
    """Information about a single conversion between two units, used as links in the graph."""

    def __init__(self, from_amount, from_unit, to_amount, to_unit):
        self.from_amount = from_amount
        self.from_unit = from_unit
        self.to_amount = to_amount
        self.to_unit = to_unit

        self.factor = self.to_amount / self.from_amount

    def __str__(self):
        return f"{self.from_unit.render(self.from_amount)} -> {self.to_unit.render(self.to_amount)}"

    def __repr__(self):
        return f"Conversion(from=({self.from_amount}, {self.from_unit.plural_name}), to=({self.to_amount}, {self.to_unit.plural_name}))"

    def convert(self, amount):
        return amount * self.factor

    def to_tuple(self):
        return self.from_unit, self.to_unit, self.factor
