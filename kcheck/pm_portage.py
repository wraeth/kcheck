#!/usr/bin/env python3

import configparser
import logging
import os
import re

from collections import OrderedDict

import portage
from kcheck.helpers import *

log = logging.getLogger('portage')
re_sym = re.compile('^.*\s(linux_chkconfig_\w+)\s+([A-Za-z0-9_]*).*$')
_add_to_config = True


def generate_config(kcheck_config: str, outputfile: str = 'kcheck.conf') -> int:
    """
    Entry point for generating required kernel configuration items from portage installed packages.

    :param kcheck_config: path to kcheck config file for checking existing options
    :param outputfile: path to write new keys into (default: 'kcheck.conf' in cwd)
    :return: integer to be returned by commandline util (0 for success, etc)
    """
    assert isinstance(kcheck_config, str)
    log.debug('Module loaded')

    master_config = configparser.ConfigParser(allow_no_value=True)
    if _add_to_config:
        log.debug('Opening config file')
        if os.path.isfile(kcheck_config):
            master_config.read(kcheck_config)
            log.debug('Config loaded')
        else:
            log.debug('No config file to open')

    # config object in which to add new keys
    config = configparser.ConfigParser(allow_no_value=True, dict_type=OrderedDict)

    # much of this section of code based on `kernel-config-check.py` by mrueg
    log.debug('Finding installed packages with kernel checks')
    verbose_print('Finding ebuilds...')
    ebuild_paths = []
    vartree = portage.db[portage.root]['vartree']
    all_cpv = vartree.dbapi.cpv_all()

    for cpv in all_cpv:
        inherit = vartree.dbapi.aux_get(cpv, ['INHERITED'])[0]
        if 'linux-info' in inherit:
            pv = portage.catsplit(cpv)[1]
            ebuild_paths.append(vartree.dbapi.getpath(cpv)+'/'+pv+'.ebuild')

    log.info('Got %d ebuilds inheriting kernel utilties' % len(ebuild_paths))
    symbols = []
    symbol_count = 0
    errors = 0

    # check listed ebuilds for known kernel config check helpers
    verbose_print('Checking %d ebuilds' % len(ebuild_paths))
    for ebuild in ebuild_paths:
        log.debug('Checking ebuild %s' % ebuild)

        # little helper object to save code repetition
        option = {
            'linux_chkconfig_present': 'YM',
            'linux_chkconfig_module': 'M',
            'linux_chkconfig_builtin': 'Y'
        }

        esymbols = 0
        eerrors = 0
        for line in open(ebuild).readlines():
            line = line.strip()
            match = re_sym.match(line)
            if not match:
                continue

            try:
                checker = match.group(1)
                mode = option[checker]
                symbol = match.group(2)
            except AttributeError:
                log.error('Failed getting symbol from line: %s' % line)
                eerrors += 1
                continue

            # check if symbol already found, warn if so
            if symbol in symbols:
                log.warning('Additional instance of symbol %s found with value %s' % (symbol, mode))
                verbose_print('Found additional instance of %s - only the first will be used' % bold(symbol))
                continue
            log.debug('Got symbol %s using %s (%s)' % (symbol, checker, mode))

            # check if we already have this symbol in the master config
            try:
                notused = master_config['ternary'][symbol]
                # no exception, so it already exists
                log.warning('Symbol %s found in master config - skipping' % symbol)
                verbose_print('Symbol %s already in config' % bold(symbol))
                del notused
                continue
            except KeyError:
                # nothing to see here
                pass
            except configparser.NoSectionError:
                # These are not the exceptions you're looking for. Move along
                pass

            esymbols += 1

            if _add_to_config:
                # make sure the section exists
                if 'ternary' not in config.sections():
                    config.add_section('ternary')

                source = os.path.basename(ebuild)
                config.set('ternary', '; from %s' % source)
                config.set('ternary', symbol, mode)
            verbose_print('  Got symbol %s using %s (%s)' % (bold(symbol), checker, yellow(mode)))

        log.info('Got %d symbols and %d errors from ebuild' % (esymbols, eerrors))
        symbol_count += esymbols
        errors += eerrors

    verbose_print('Got %s symbols and %s errors from %s ebuilds' % (bold(symbol_count), yellow(errors), green(len(ebuild_paths))))

    # write out (if necessary)
    if _add_to_config:
        log.info('Writing values to config file')
        with open(outputfile, 'w') as fh:
            config.write(fh)
        log.debug('Config file written')
        print('%s discovered required symbol(s) written to %s.' % (bold(symbol_count), green(outputfile)))

    # return with how many failed reads we go (the only really significant error count here)
    return errors


if __name__ == '__main__':
    # allow running this manually and printing to stdout instead
    _add_to_config = False
    _verbose = True
    exit(generate_config(''))
