import itertools
import re
from pathlib import Path

import toml

from . import data


def parse_compound(units, cmp_str):
    # both " per " and "/", but with any amount of whitespace
    unit_split = list(itertools.chain.from_iterable(s.split("/") for s in re.split(r"\s+per\s+", cmp_str)))

    # A unit recognized as singular but present in the unit table *might* be a compound alias
    if len(unit_split) == 1 and unit_split[0] in units:
        unit = units[unit_split[0]]
        # If it is, return it directly
        if isinstance(unit, data.CompoundUnit):
            return unit

    # Otherwise, construct a compound unit out of the unit splits
    units = list(map(lambda unit_str: units[unit_str], unit_split))
    return data.CompoundUnit(units)


def parse_str_pair(units, pair):
    amount_str, unit_name = pair.split(None, 1)
    amount = float(amount_str)
    unit = parse_compound(units, unit_name)

    return amount, unit


def parse_table(path):
    doc_str = Path(path).read_text()
    doc = toml.loads(doc_str)

    # Populate unit table
    units = {}
    for plural_name, (singular_name, *aliases) in doc["units"].items():
        unit = data.Unit(plural_name, singular_name, aliases)

        if plural_name in units:
            raise ValueError(f"Duplicate plural unit name '{plural_name}'")
        units[plural_name] = unit

        # Duplicates are normal for units with plural == singular
        if singular_name in units and plural_name != singular_name:
            raise ValueError(f"Duplicate singular unit name '{singular_name}'")
        units[singular_name] = unit

        for alias in aliases:
            if alias in units:
                raise ValueError(f"Duplicate unit alias name '{alias}'")
            units[alias] = unit

    # Add compound aliases to unit table
    for alias, unit in doc["compound_aliases"].items():
        if alias in units:
            raise ValueError(f"Duplicate compound unit alias name '{alias}")

        units[alias] = parse_compound(units, unit)

    # Populate graph and link table
    graph = {}
    for from_pair, to_pair in doc["conversions"].items():
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
