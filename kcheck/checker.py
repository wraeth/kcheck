#!/usr/bin/env python3

"""
Check required kernel configuration items.
"""

import configparser
import logging

log = logging.getLogger('checker')


def check_config(kcheck_config: str, kernel_config: str) -> int:
    """
    Entry point for command line utility.

    :param kcheck_config: path to kcheck config with required kernel symbols
    :param kernel_config: path to kernel .config or config.gz to check
    :return: return value for command line utility
    """
    assert isinstance(kcheck_config, str)
    assert isinstance(kernel_config, str)
    log.debug('Module loaded - beginning kernel configuration check')

    symbols = load_required_symbols(kcheck_config)
    # TODO: put stuff here
    return 0


def load_required_symbols(config_file: str) -> dict:
    """
    Reads the specified configuration file to get required kernel symbol states.

    :param config_file: path to configuration file
    :return: dict(symbol: [values])
    """
    assert isinstance(config_file, str)

    log.info('Reading required kernel symbols from config')
    config = configparser.ConfigParser(allow_no_value=True)

    symbols = {}

    log.debug('Using config file %s' % config_file)

    try:
        config.read(config_file)
    except configparser.DuplicateOptionError as err:
        log.critical(err.message)
        raise

    if 'ternary' in config.sections():
        log.info('Loading ternary symbols')
        for key in config['ternary']:
            assert isinstance(key, str)
            sym_name = key.upper()

            if not sym_name.startswith('CONFIG_'):
                sym_name = 'CONFIG_'+sym_name

            value = config['ternary'][key]

            if value is None:
                value = 'YM'

            value = list(value.upper())

            log.debug('Got symbol %s with allowed values %s' % (sym_name, str(value)))
            symbols[sym_name] = value

    if 'string' in config.sections():
        log.info('Loading string symbols')
        for key in config['string']:
            assert isinstance(key, str)
            sym_name = key.upper()

            if not sym_name.startswith('CONFIG_'):
                sym_name = 'CONFIG_'+sym_name

            # to retain format, this is encased in list
            value = [config['string'][key]]

            log.debug('Got symbol {!s} with value {!r}'.format(sym_name, value))
            symbols[sym_name] = value

    log.info('Loaded %d kernel symbols to check' % len(symbols.keys()))
    return symbols
