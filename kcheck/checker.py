#!/usr/bin/env python3

"""
Check required kernel configuration items.
"""

import argparse
import logging

log = logging.getLogger('checker')


def check_config(args: argparse.Namespace) -> int:
    """
    Entry point for command line utility.

    :param args: argparse.Namespace from command line utility
    :return: return value for command line utility
    """
    assert isinstance(args, argparse.Namespace)

    log.debug('Module loaded - beginning kernel configuration check')
    # TODO: put stuff here
    return 0
