import argparse

from . import ansi, parser
from .converter import Converter


def parse_args():
    arg_parser = argparse.ArgumentParser()

    arg_parser.add_argument("-d", "--debug", default=False, action="store_true", help="enable debug mode")
    arg_parser.add_argument("from_amount", metavar="FROM_AMOUNT", type=float, help="amount of the unit to convert from")
    arg_parser.add_argument(
        "from_unit", metavar="FROM_UNIT", type=str, help="name or symbol of the unit to convert from"
    )
    arg_parser.add_argument("to_unit", metavar="TO_UNIT", type=str, help="name or symbol of the unit to convert to")

    return arg_parser.parse_args()


def main():
    args = parse_args()
    units, graph = parser.parse_table("units.toml")

    try:
        from_unit = units[args.from_unit]
    except KeyError:
        print(ansi.red(f"Unrecognized source unit '{args.from_unit}'"))
        return 1

    try:
        to_unit = units[args.to_unit]
    except KeyError:
        print(ansi.red(f"Unrecognized destination unit '{args.to_unit}'"))
        return 1

    converter = Converter(units, graph, debug=args.debug)
    converted_amount = converter.convert(args.from_amount, from_unit, to_unit)

    if converted_amount is None:
        print(ansi.red(f"No path from {from_unit} to {to_unit}"))
        return 1
    else:
        print(f"{ansi.bold(from_unit.render(args.from_amount))} => {ansi.bold(to_unit.render(converted_amount))}")
        return 0
