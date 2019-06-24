# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Mimalloc(CMakePackage):
    """mimalloc is a compact general purpose allocator with excellent
    performance."""

    homepage = "https://github.com/microsoft/mimalloc"
    git      = "https://github.com/microsoft/mimalloc"

    version('master', branch='master')

    def cmake_args(self):
        return []
