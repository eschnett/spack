# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libuv(AutotoolsPackage):
    """Multi-platform library with a focus on asynchronous IO"""
    homepage = "http://libuv.org"
    url      = "https://github.com/libuv/libuv/archive/v1.9.0.tar.gz"

    version('1.27.0', sha256='4afcdc84cd315b77c8e532e7b3fde43d536af0e2e835eafbd0e75518ed26dbed')
    version('1.26.0', sha256='e414cf74615b7dae768f0f5667092f1d4975f5067c087bcbe0641e241ebe4693')
    version('1.25.0', '31a1873ebceacae42573bac8ec5da687')
    version('1.10.0', 'f7a12f3a8ee021c20cfbc9af4cc5b793')
    version('1.9.0',  '14737f9c76123a19a290dabb7d1cd04c')

    depends_on('automake', type='build')
    depends_on('autoconf', type='build')
    depends_on('libtool', type='build')

    def autoreconf(self, spec, prefix):
        # This is needed because autogen.sh generates on-the-fly
        # an m4 macro needed during configuration
        bash = which("bash")
        bash('autogen.sh')
