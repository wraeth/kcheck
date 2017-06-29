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
    import kcheck
    import logging
    import sys

    parser = argparse.ArgumentParser(description='Kernel configuration check utility')
    parser.add_argument('-c', '--config', help='kcheck config file', default='/etc/kcheck.conf')
    parser.add_argument('-k', '--kernel', help='kernel config file', default='/usr/src/linux/.config')
    parser.add_argument('-v', '--verbose', help='Output extra information', action='count', default=2)
    parser.add_argument('-V', '--version', help='Print version information and exit', action='store_true')

    subparsers = parser.add_subparsers(help='commands')

    gen_parser = subparsers.add_parser('genconfig', help='Generate config requirements from installed packages')
    gen_parser.add_argument('-l', '--list', help='list available package manager integrations', action='store_true')
    gen_parser.add_argument('-m', '--manager', help='Package manager', choices=kcheck.ALLOWED_PKGMGR, default='portage')
    gen_parser.set_defaults(mode='genconfig')
    
    args = parser.parse_args()

    # set up logging
    log_level = 50 - (args.verbose * 10)
    logging.basicConfig(level=log_level)
    log = logging.getLogger('main')

    if args.version:
        print('kcheck', kcheck.__version__)
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
            except ImportError:
                print('Unable to load module for package manager', args.manager, file=sys.stderr)
                return 1

            return package_manager.generate_config(args)

    else:
        # no "mode", so run kcheck
        import kcheck.checker
        return kcheck.checker.check_config(args)

if __name__ == '__main__':
    main()
