#!/usr/bin/env python3

"""Formatting helpers."""

__verbose = False
__coloured = True


class Colour:

    green = '\033[92m'
    yellow = '\033[93m'
    red = '\033[91m'
    bold = '\033[1m'
    end = '\033[0m'


def green(msg) -> str:
    formatted = str(msg)
    if __coloured:
        formatted = Colour.green + formatted + Colour.end
    return formatted


def yellow(msg) -> str:
    formatted = str(msg)
    if __coloured:
        formatted = Colour.yellow + formatted + Colour.end
    return formatted


def red(msg) -> str:
    formatted = str(msg)
    if __coloured:
        formatted = Colour.red + formatted + Colour.end
    return formatted


def bold(msg) -> str:
    formatted = str(msg)
    if __coloured:
        formatted = Colour.bold + formatted + Colour.end
    return formatted


def verbose_print(msg: str = '') -> None:
    """
    Print message to stdout if __verbose is True.

    :param msg: message to print
    :return: None
    """
    assert isinstance(msg, str)
    if __verbose:
        print(msg)
