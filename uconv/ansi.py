"""ANSI color codes for terminal output."""

RED = "\u001b[1;31m"
BOLD = "\u001b[1m"
RESET = "\u001b[0m"


def red(content):
    return RED + str(content) + RESET


def bold(content):
    return BOLD + str(content) + RESET
