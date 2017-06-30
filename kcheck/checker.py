#!/usr/bin/env python3

"""
Check required kernel configuration items.
"""

import configparser
import logging

log = logging.getLogger('checker')
_verbose = False  # this will get updated by command.py when called


def check_config(kcheck_config: str, kernel_config: str) -> int:
    """
    Load and compare symbols from config and kernel.

    :param kcheck_config: path to kcheck config with required kernel symbols
    :param kernel_config: path to kernel .config or config.gz to check
    :return: return value for command line utility
    """
    assert isinstance(kcheck_config, str)
    assert isinstance(kernel_config, str)
    log.debug('Module loaded - beginning kernel configuration check')

    verbose_print('Reading symbols...')

    required_symbols = load_required_symbols(kcheck_config)
    kernel_symbols = read_kernel_config(kernel_config)

    incorrect_symbols = {}
    missing_symbols = []

    log.info('Comparing required kernel symbols')

    verbose_print()

    for req_sym in required_symbols.keys():
        req_val = required_symbols[req_sym]

        try:
            cur_val = kernel_symbols[req_sym]
        except KeyError:
            log.warning('Required symbol %s is not in kernel config' % req_sym)
            missing_symbols.append(req_sym)
            continue

        if cur_val in req_val:
            log.info('%s within allowed values' % req_sym)
            verbose_print('%s matches allowed value(s)' % req_sym)
            continue
        else:
            log.warning('%s does not match value %s' % (req_sym, str(req_val)))
            incorrect_symbols[req_sym] = [cur_val, req_val]
            continue

    log.info('%d keys with incorrect values' % len(incorrect_symbols.keys()))
    log.info('%d keys not found in kernel config' % len(missing_symbols))

    verbose_print()
    if len(incorrect_symbols.keys()) > 0:
        print('The following config symbols have incorrect values:')
        for key in incorrect_symbols.keys():
            cur, req = incorrect_symbols[key]
            print('    %s set to %s when it should be %s' % (key, cur, req))
        print()
    else:
        print('No required symbols have incorrect values!')
        print()

    if len(missing_symbols) > 0:
        print('The following required keys were not found in the kernel config:')
        for key in missing_symbols:
            print('    %s' % key)

    return len(incorrect_symbols.keys()) + len(missing_symbols)


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
    verbose_print('%d required symbols loaded from config' % len(symbols.keys()))
    return symbols


def read_kernel_config(kernel_config: str) -> dict:
    """
    Reads the specified kernel configuration into a dict.

    :param kernel_config: path to kernel .config or config.gz
    :return: dict(symbol: value)
    """
    assert isinstance(kernel_config, str)
    log.info('Reading kernel config from %s' % kernel_config)

    # we are but a simple python script - we only guess at what we see
    if kernel_config.endswith('.gz'):
        log.debug('Kernel file assumed to be gzipped based on file extension')
        from gzip import open as myopen
        mode = 'rt'
    else:
        myopen = open
        mode = 'r'

    try:
        log.debug('Opening kernel config')
        fh = myopen(kernel_config, mode=mode)
    except FileNotFoundError as err:
        log.critical('The kernel configuration file "%s" was not found!' % kernel_config)
        log.exception(err)
        raise

    symbols = {}

    log.debug('Processing config lines')
    for line in fh.readlines():
        # throw out the junk
        if not 'CONFIG_' in line:
            continue

        line = line.strip()

        # differentiate unset and set keys, add to dict
        if 'is not set' in line:
            sym = line[2:-11]
            value = line[-10:].upper()
        else:
            sym, value = line.split('=')
            value = value.upper()
            if '"' in value:
                value = value.replace('"', '')

        assert isinstance(sym, str)
        assert isinstance(value, str)

        log.debug('Got symbol %s with value "%s"' % (sym, value))
        symbols[sym] = value

    fh.close()

    log.info('Read %d symbols from kernel config' % len(symbols.keys()))
    verbose_print('%d kernel symbols loaded from %s' % (len(symbols.keys()), kernel_config))
    return symbols


def verbose_print(msg: str = '') -> None:
    """
    Helper for printing messages when --verbose.

    :param msg: Message to print
    :return: None
    """
    assert isinstance(msg, str)
    if _verbose:
        print(msg)
