import argparse
import locale

from . import ansi, parser
from .converter import ConversionError, Converter


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
    # Set locale for localized number formatting
    locale.setlocale(locale.LC_ALL, "")

    args = parse_args()
    try:
        units, graph = parser.parse_table("units.toml")
    except ValueError as e:
        print(ansi.red(str(e)))
        return 1

    try:
        from_unit = parser.parse_compound(units, args.from_unit)
    except KeyError:
        print(ansi.red(f"Unrecognized source unit '{args.from_unit}'"))
        return 1

    try:
        to_unit = parser.parse_compound(units, args.to_unit)
    except KeyError:
        print(ansi.red(f"Unrecognized destination unit '{args.to_unit}'"))
        return 1

    converter = Converter(units, graph, debug=args.debug)
    try:
        converted_amount = converter.convert(args.from_amount, from_unit, to_unit)
    except ConversionError as e:
        print(ansi.red(str(e)))
        return 1

    print(f"{ansi.bold(from_unit.render(args.from_amount))} => {ansi.bold(to_unit.render(converted_amount))}")
    return 0
