#!/usr/bin/env python3

"""Generate required kernel config symbols from installed packages and check .config for required symbols."""

from pkg_resources import get_distribution, DistributionNotFound
import os.path

__author__ = "Sam Jorna (wraeth)"
__copyright__ = "Copyright 2017, Sam Jorna"
__license__ = "MIT"
__maintainer__ = "Sam Jorna (wraeth)"
__email__ = "wraeth@wraeth.id.au"
__status__ = "prototype"
__version__ = "0.0.2"

ALLOWED_PKGMGR = [
    'portage'
]
MGR_MODULE = {
    'portage': 'pm_portage'
}
