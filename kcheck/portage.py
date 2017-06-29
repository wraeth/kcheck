#!/usr/bin/env python3

import argparse
import logging

log = logging.getLogger('portage')


def generate_config(args: argparse.Namespace) -> int:
    """
    Entry point for generating required kernel configuration items from portage installed packages.

    :param args: the argparse.Namespace object from the command line
    :return: integer to be returned by commandline util (0 for success, etc)
    """
    assert isinstance(args, argparse.Namespace)

    log.debug('Module loaded - generating required configuration')
    # TODO: put stuff here
    return 0
