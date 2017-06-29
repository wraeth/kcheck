#!/usr/bin/env python3

"""
Entry point for utility, option handling.
"""


def main() -> int:
    """
    Entry point for command line utility.

    :return: integer for return code of command line
    """

    import argparse
    import importlib
    import logging
    import platform

    import kcheck

    parser = argparse.ArgumentParser(description='Kernel configuration check utility')
    parser.add_argument('-c', '--config', help='kcheck config file', default='/etc/kcheck.conf')
    parser.add_argument('-k', '--kernel', help='kernel config file', default='/usr/src/linux/.config')
    parser.add_argument('-l', '--logfile', help='file to write logging into')
    parser.add_argument('-v', '--verbose', help='Output extra information', action='count', default=2)
    parser.add_argument('-V', '--version', help='Print version information and exit', action='store_true')

    subparsers = parser.add_subparsers(help='commands')

    gen_parser = subparsers.add_parser('genconfig', help='Generate config requirements from installed packages')
    gen_parser.add_argument('-l', '--list', help='list available package manager integrations', action='store_true')
    gen_parser.add_argument('-m', '--manager', help='Package manager', choices=kcheck.ALLOWED_PKGMGR, default='portage')
    gen_parser.set_defaults(mode='genconfig')
    
    args = parser.parse_args()

    ## set up logging ##
    # logging output level
    log_level = 50 - (args.verbose * 10)

    # format and handlers
    handlers = [logging.StreamHandler()]
    if args.logfile:
        lh = logging.FileHandler(args.logfile)
        lh.setFormatter(logging.Formatter("%(asctime)s [%(name)s] [%(levelname)-5.5s]  %(message)s"))
        handlers.append(lh)
    logging.basicConfig(level=log_level, handlers=handlers)

    # initialise logger and log basics
    log = logging.getLogger('main')
    log.info('kcheck %s' % kcheck.__version__)
    log.debug('Called with arguments: %s' % str(args._get_kwargs()))

    if args.version:
        print('kcheck %s (Python %s)' % (kcheck.__version__, platform.python_version()))
        return 0

    if 'mode' in args:
        if args.mode == 'genconfig':
            if args.list:
                print('The following package managers can be used for generating required kernel configurations')
                [print('   ', p) for p in kcheck.ALLOWED_PKGMGR]
                return 0

            # get the module name for the package manager, import and hand over
            module = 'kcheck.'+args.manager
            log.debug('Loading module %s' % module)
            try:
                package_manager = importlib.import_module(module)
            except ImportError as exception:
                log.critical("Unable to load module for package manager %s" % module)
                log.exception(exception)
                return 1

            return package_manager.generate_config(args)

    else:
        # no "mode", so run kcheck
        import kcheck.checker
        return kcheck.checker.check_config(args)

if __name__ == '__main__':
    main()
