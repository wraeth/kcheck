# Copyright 1999-2017 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2

EAPI=6
PYTHON_COMPAT=( python3_{4,5,6} )

inherit distutils-r1

DESCRIPTION="Check required kernel symbols are set"
HOMEPAGE="https://github.com/wraeth/kcheck"
SRC_URI="https://github.com/wraeth/${PN}/archive/${PV}.tar.gz -> ${P}.tar.gz"

LICENSE="MIT"
SLOT="0"
KEYWORDS="~amd64 ~x86"

DEPEND="${PYTHON_DEPS}
	dev-python/setuptools[${PYTHON_USEDEP}]"
RDEPEND="${DEPEND}
	dev-python/configargparse[${PYTHON_USEDEP}]"

src_install() {
	distutils-r1_src_install
	mkdir ${D}etc || die
	mv -v ${D}{usr/,}etc/kcheck.conf || die
}