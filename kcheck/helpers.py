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


def green(msg: str) -> str:
    assert isinstance(msg, str)
    formatted = msg
    if __coloured:
        formatted = Colour.green+msg+Colour.end
    return formatted


def yellow(msg: str) -> str:
    assert isinstance(msg, str)
    formatted = msg
    if __coloured:
        formatted = Colour.yellow + msg + Colour.end
    return formatted


def red(msg: str) -> str:
    assert isinstance(msg, str)
    formatted = msg
    if __coloured:
        formatted = Colour.red + msg + Colour.end
    return formatted


def bold(msg: str) -> str:
    assert isinstance(msg, str)
    formatted = msg
    if __coloured:
        formatted = Colour.bold + msg + Colour.end
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
