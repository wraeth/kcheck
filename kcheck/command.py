#!/usr/bin/env python3

"""
Entry point for utility, option handling.
"""


def main() -> int:
    """
    Entry point for command line utility.

    :return: integer for return code of command line
    """

    import configargparse
    import importlib
    import logging
    import os
    import platform

    from configparser import DuplicateOptionError

    import kcheck
    import kcheck.helpers

    __default_config = '/etc/kcheck.conf'

    parser = configargparse.ArgumentParser(
        add_config_file_help=True,
        default_config_files=[__default_config],
        ignore_unknown_config_file_keys=True,
        formatter_class=lambda prog: configargparse.HelpFormatter(prog,max_help_position=35)
    )
    parser.add_argument('--config', '-c', is_config_file=True, help='kcheck config file')
    parser.add_argument('--kernel', '-k', help='kernel config file', default='/usr/src/linux/.config')
    parser.add_argument('--logfile', '-l', help='file to write logging into')
    parser.add_argument('--debug', '-d', help='increase log verbosity (repeatable)', action='count', default=2)
    parser.add_argument('--verbose', '-v', help='Output extra information', action='store_true')
    parser.add_argument('--version', '-V', help='Print version information and exit', action='store_true')
    parser.add_argument('--nocolour', '-C', help='Disable colour', action='store_false')

    subparsers = parser.add_subparsers(help='commands')

    gen_parser = subparsers.add_parser('genconfig', help='Generate config requirements from installed packages')
    gen_parser.add_argument('-l', '--list', help='list available package manager integrations', action='store_true')
    gen_parser.add_argument('-m', '--manager', help='Package manager', choices=kcheck.ALLOWED_PKGMGR, default='portage')
    gen_parser.add_argument('-o', '--output', help='Path to generate new config', required=True)
    gen_parser.set_defaults(mode='genconfig')

    args = parser.parse_args()

    if args.version:
        print('kcheck %s (Python %s)' % (kcheck.__version__, platform.python_version()))
        return 0

    ## set up logging ##
    # logging output level
    log_level = 50 - (args.debug * 10)

    # format and handler
    if args.logfile:
        logHandler = logging.FileHandler(args.logfile)
        logHandler.setFormatter(logging.Formatter("%(asctime)s [%(name)s] [%(levelname)-5.5s]  %(message)s"))
    else:
        logHandler = logging.NullHandler()
    logging.basicConfig(level=log_level, handlers=[logHandler])

    # initialise logger and log basics
    try:
        log = logging.getLogger('main')
        log.info('kcheck %s' % kcheck.__version__)
        [log.debug(line) for line in parser.format_values().splitlines()]
    except PermissionError as err:
        print('Error: unable to write log file: %s' % err.strerror)
        return -4

    # Warn if there's no config file
    if not args.config:
        args.config = __default_config
    if not os.path.exists(args.config) and not args.mode:
        log.warning('No config file found!')
        print('Warning: No configuration file found. Running this utility without a config is useless.')
        print('         Please create a config file at %r, or specify one with `--config [PATH]`' % __default_config)
        return -3

    kcheck.helpers.__verbose = args.verbose
    kcheck.helpers.__coloured = args.nocolour

    # check for args.mode and call either checker or PM generator
    if 'mode' in args:
        if args.mode == 'genconfig':
            if args.list:
                print('The following package managers can be used for generating required kernel configurations')
                [print('   ', p) for p in kcheck.ALLOWED_PKGMGR]
                return 0

            # get the module name for the package manager, import and hand over
            module = 'kcheck.'+kcheck.MGR_MODULE[args.manager]
            log.debug('Loading module %s' % module)
            try:
                package_manager = importlib.import_module(module)
            except ImportError as exception:
                log.critical("Unable to load module for package manager %s" % module)
                log.exception(exception)
                return -1

            return package_manager.generate_config(args.config, args.output)

    else:
        # no "mode", so run kcheck
        import kcheck.checker

        try:
            return kcheck.checker.check_config(args.config, args.kernel)
        except DuplicateOptionError:
            print('Your config file has duplicate keys in a section.')
            if args.logfile:
                print('See the log file %s for more details' % args.logfile)
            print('Correct your config file and try running this again.')
            return -2

if __name__ == '__main__':
    exit(main())
