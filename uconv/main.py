from pprint import pprint

from . import parser


def main() -> None:
    units, graph = parser.parse_table("units.toml")
    pprint(units)
    print()
    pprint(graph)
