from . import search


class ConversionError(Exception):
    pass


class Converter:
    def __init__(self, units, graph, debug=False):
        self.units = units
        self.graph = graph
        self.debug = debug

    def dbg(self, *args, **kwargs):
        if self.debug:
            print(*args, **kwargs)

    def compound_convert(self, from_amount, from_units, to_units):
        if len(from_units.units) != len(to_units.units):
            raise ConversionError(f"Cannot convert compound units with differing numbers of simple units")

        amount = from_amount
        for idx, (from_unit, to_unit) in enumerate(zip(from_units.units, to_units.units)):
            self.dbg(f"Converting {from_unit} to {to_unit}... (unit {idx + 1} of {len(from_units.units)})")

            # Operation for the first unit is the same, but subsequent divided units are the opposite
            op = "*" if idx == 0 else "/"
            amount = self.convert(amount, from_unit, to_unit, op, in_compound=True)

        return amount

    def convert(self, from_amount, from_unit, to_unit, op="*", in_compound=False):
        self.dbg("Looking for simple conversion path...")
        path = search.find_shortest_path(self.graph, from_unit, to_unit)

        # None means no path is available
        if path is None:
            if in_compound:
                raise ConversionError(f"No path from {from_unit} to {to_unit}")
            else:
                self.dbg("Not found, looking for compound conversion paths...")
                return self.compound_convert(from_amount, from_unit, to_unit)

        friendly_path = ", ".join(map(str, path))
        self.dbg(f"Found conversion path: {friendly_path}")

        amount = from_amount
        for conv in path:
            converted = conv.convert(amount, op)
            self.dbg(f"Converting {conv.from_unit.render(amount)} -> {conv.to_unit.render(converted)}")
            amount = converted

        return amount
