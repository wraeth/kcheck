#!/usr/bin/env python3

import logging

log = logging.getLogger('portage')


def generate_config(kcheck_config: str) -> int:
    """
    Entry point for generating required kernel configuration items from portage installed packages.

    :param kcheck_config: path to kcheck config file to write into
    :return: integer to be returned by commandline util (0 for success, etc)
    """
    assert isinstance(kcheck_config, str)

    log.debug('Module loaded - generating required configuration')
    # TODO: put stuff here
    return 0
