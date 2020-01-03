from pathlib import Path

import toml

from . import data


def parse_str_pair(units, pair):
    amount_str, unit_name = pair.split(None, 1)
    amount = float(amount_str)
    unit = units[unit_name]

    return amount, unit


def parse_table(path):
    doc_str = Path(path).read_text()
    doc = toml.loads(doc_str)

    # Populate unit table
    units = {}
    for plural_name, (singular_name, *aliases) in doc["units"].items():
        unit = data.Unit(plural_name, singular_name, aliases)

        for name in (plural_name, singular_name, *aliases):
            units[name] = unit

    # Populate graph and link table
    graph = {}
    for from_pair, to_pair in zip(*[iter(doc["conversions"]["table"])] * 2):
        # Extract amounts and units from pairs
        from_amount, from_unit = parse_str_pair(units, from_pair)
        to_amount, to_unit = parse_str_pair(units, to_pair)

        # Add from->to conversion to graph
        from_to_conv = data.Conversion(from_amount, from_unit, to_amount, to_unit)
        if from_unit in graph:
            graph[from_unit].append(from_to_conv)
        else:
            graph[from_unit] = [from_to_conv]

        # Add reverse conversion to graph (adjacency lists require it present both ways)
        to_from_conv = data.Conversion(to_amount, to_unit, from_amount, from_unit)
        if to_unit in graph:
            graph[to_unit].append(to_from_conv)
        else:
            graph[to_unit] = [to_from_conv]

    return units, graph
