#!/usr/bin/env python3

"""Generate required kernel config symbols from installed packages and check .config for required symbols."""

from pkg_resources import get_distribution, DistributionNotFound
import os.path

try:
    _dist = get_distribution('foobar')
    # Normalize case for Windows systems
    dist_loc = os.path.normcase(_dist.location)
    here = os.path.normcase(__file__)
    if not here.startswith(os.path.join(dist_loc, 'foobar')):
        # not installed, but there is another version that *is*
        raise DistributionNotFound
except DistributionNotFound:
    __version__ = 'Please install this project with setup.py'
else:
    __version__ = _dist.version

__author__ = "Sam Jorna (wraeth)"
__copyright__ = "Copyright 2017, Sam Jorna"
__license__ = "MIT"
__maintainer__ = "Sam Jorna (wraeth)"
__email__ = "wraeth@wraeth.id.au"
__status__ = "prototype"

ALLOWED_PKGMGR = [
    'portage'
]
