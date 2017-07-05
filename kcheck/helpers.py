#!/usr/bin/env python3

"""Helper functions"""

__verbose = False


class Colour:
    green = '\033[92m'
    yellow = '\033[93m'
    red = '\033[91m'
    bold = '\033[1m'
    end = '\033[0m'


def verbose_print(msg: str = '') -> None:
    """
    Print message to stdout if __verbose is True.

    :param msg: message to print
    :return: None
    """
    assert isinstance(msg, str)
    if __verbose:
        print(msg)
