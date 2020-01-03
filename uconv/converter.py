from . import search


class Converter:
    def __init__(self, units, graph, debug=False):
        self.units = units
        self.graph = graph
        self.debug = debug

    def dbg(self, *args, **kwargs):
        if self.debug:
            print(*args, **kwargs)

    def convert(self, from_amount, from_unit, to_unit):
        path = search.find_shortest_path(self.graph, from_unit, to_unit)
        self.dbg(f"Found conversion path: {path}")
        if path is None:
            return None

        amount = from_amount
        for conv in path:
            self.dbg(f"Converting {amount} {conv.from_unit} -> {conv.convert(amount)} {conv.to_unit}")
            amount = conv.convert(amount)

        return amount
