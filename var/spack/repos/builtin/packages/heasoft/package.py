##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################

import glob
import os

import llnl.util.tty as tty
from spack import *


class Heasoft(AutotoolsPackage):
    """HEASoft: A Unified Release of the FTOOLS and XANADU Software Packages"""

    homepage = "https://heasarc.gsfc.nasa.gov"
    url      = "http://heasarc.gsfc.nasa.gov/FTP/software/lheasoft/release/heasoft-6.21src.tar.gz"

    # Note: The download file is 2 GByte large
    version('6.21', 'db28db52295c00c75a7e8888dc6a6db4')

    variant('python', default=True, description="Support Python")
    variant('x11', default=True, description="Support X11")

    # Also requires C, C++, Fortran compilers
    depends_on('libx11', when='+x11')
    depends_on('ncurses')
    depends_on('perl @5.6.0:', type='build')
    depends_on('python', type=('build', 'run'), when='+python')
    depends_on('readline')
    # depends_on('tcl')
    # depends_on('tk')

    # TODO:
    # - use Spack-provided readline
    # - build with "root" package
    # - enable PNG support
    # - enable OpenMP
    # - build static/shared libraries as is common in Spack

    @property
    def configure_directory(self):
        return join_path(self.stage.source_path, "BUILD_DIR")

    # Don't use "-arch XXX" compiler flags, correct "-rpath" options
    @run_before('configure')
    def remove_arch(self):
        for subdir, dirs, files in os.walk("."):
            for file in files:
                # Ignore "spack-build.*" files so that we don't lose
                # the log files.
                # Ignore data files because they are binary.
                if (file.startswith("spack-build.") or
                    file.endswith(".dat") or file.endswith(".fits")):
                    continue
                filepath = join_path(subdir, file)
                if os.path.isfile(filepath):
                    filter_file(r"-arch\s+(i386|x86_64)", "", filepath,
                                backup=False)
                    filter_file(r"-rpath\s+", "-Wl,-rpath,", filepath,
                                backup=False)

    def configure_args(self):
        components = [
            "GSSC"
            "Xspec",
            "attitude",
            "demo",
            "external",
            "ftools",
            "glast",
            "heacore",
            "heagen",
            "heasim",
            "heatools",
            "hitomi",
            "integral",
            "nustar",
            "suzaku",
            "swift",
            # "tcltk",
            "xmm",
        ]
        args = [
            "--with-components=%s" % " ".join(components),
        ]
        return args
