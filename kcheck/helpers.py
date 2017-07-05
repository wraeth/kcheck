#!/usr/bin/env python3

"""Helper functions"""

__verbose = False


def verbose_print(msg: str = '') -> None:
    """
    Print message to stdout if __verbose is True.

    :param msg: message to print
    :return: None
    """
    assert isinstance(msg, str)
    if __verbose:
        print(msg)
