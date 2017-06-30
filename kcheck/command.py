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
    import logging
    import platform

    from configparser import DuplicateOptionError

    import kcheck

    parser = configargparse.ArgumentParser(
        add_config_file_help=True,
        default_config_files=['/etc/kcheck.conf'],
        ignore_unknown_config_file_keys=True,
        formatter_class=lambda prog: configargparse.HelpFormatter(prog,max_help_position=35)
    )
    parser.add_argument('--config', '-c', is_config_file=True, help='kcheck config file')
    parser.add_argument('--kernel', '-k', help='kernel config file', default='/usr/src/linux/.config')
    parser.add_argument('--logfile', '-l', help='file to write logging into')
    parser.add_argument('--debug', '-d', help='increase log verbosity (repeatable)', action='count', default=2)
    parser.add_argument('--verbose', '-v', help='Output extra information', action='store_true')
    parser.add_argument('--version', '-V', help='Print version information and exit', action='store_true')

    args = parser.parse_args()

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
    log = logging.getLogger('main')
    log.info('kcheck %s' % kcheck.__version__)
    [log.debug(line) for line in parser.format_values().splitlines()]

    if args.version:
        print('kcheck %s (Python %s)' % (kcheck.__version__, platform.python_version()))
        return 0

    # will check for args.mode here when other functions added
    import kcheck.checker
    kcheck.checker._verbose = args.verbose

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
