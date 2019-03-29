# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Tiledb(CMakePackage):
    """TileDB: Array data management made fast and easy"""

    homepage = "https://tiledb.io"
    url      = "https://github.com/TileDB-Inc/TileDB/archive/1.4.2.tar.gz"

    version('1.4.2', sha256='20b1b4f97b9e40d36261982835f67f3d2f4f2c8c5d33b6b4709914e55049094d')

    variant('static', default=False,
            description="Build static libraries as well")

    depends_on('bzip2')
    depends_on('intel-tbb')
    depends_on('lz4')
    depends_on('openssl')
    depends_on('zlib')
    depends_on('zstd')

    def cmake_args(self):
        args = ['-DTILEDB_WERROR=OFF']
        if '+static' in self.spec:
            args.append('-DTILEDB_STATIC=ON')
        return args

    install_targets = ['install-tiledb']
