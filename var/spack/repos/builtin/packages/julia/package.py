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

from spack import *
import os
import sys


class Julia(Package):
    """The Julia Language: A fresh approach to technical computing"""
    homepage = "http://julialang.org"
    url      = "https://github.com/JuliaLang/julia/releases/download/v0.4.3/julia-0.4.3-full.tar.gz"

    version('master',
            git='https://github.com/JuliaLang/julia.git', branch='master')
    version('release-0.4',
            git='https://github.com/JuliaLang/julia.git', branch='release-0.4')
    version('0.4.6', 'd88db18c579049c23ab8ef427ccedf5d', preferred=True)
    version('0.4.5', '69141ff5aa6cee7c0ec8c85a34aa49a6')
    version('0.4.3', '8a4a59fd335b05090dd1ebefbbe5aaac')

    variant("cxx", default=False, description="Prepare for Julia Cxx package")
    variant("hdf5", default=False, description="Prepare for Julia HDF5 package")
    variant("mpi", default=False, description="Prepare for Julia MPI package")

    patch('gc.patch', when='@0.4:0.4.5')
    patch('openblas.patch', when='@0.4:0.4.5')

    variant('binutils', default=sys.platform!='darwin',
            description="Build via binutils")

    # Build-time dependencies:
    # depends_on("awk")
    depends_on("m4")
    # depends_on("pkg-config")
 
    # Combined build-time and run-time dependencies:
    depends_on("binutils", when='+binutils')
    depends_on("cmake @2.8:")
    depends_on("git")
    depends_on("openssl")
    depends_on("python @2.7:2.999")

    # Run-time dependencies:
    # depends_on("arpack")
    # depends_on("fftw +float")
    # depends_on("gmp")
    # depends_on("libgit")
    # depends_on("mpfr")
    # depends_on("openblas")
    # depends_on("pcre2")

    # ARPACK: Requires BLAS and LAPACK; needs to use the same version
    # as Julia.

    # BLAS and LAPACK: Julia prefers 64-bit versions on 64-bit
    # systems. OpenBLAS has an option for this; make it available as
    # variant.

    # FFTW: Something doesn't work when using a pre-installed FFTW
    # library; need to investigate.

    # GMP, MPFR: Something doesn't work when using a pre-installed
    # FFTW library; need to investigate.

    # LLVM: Julia works only with specific versions, and might require
    # patches. Thus we let Julia install its own LLVM.

    # Other possible dependencies:
    # USE_SYSTEM_OPENLIBM=0
    # USE_SYSTEM_OPENSPECFUN=0
    # USE_SYSTEM_DSFMT=0
    # USE_SYSTEM_SUITESPARSE=0
    # USE_SYSTEM_UTF8PROC=0
    # USE_SYSTEM_LIBGIT2=0

    # Run-time dependencies for Julia packages:
    depends_on("hdf5", when="+hdf5")
    depends_on("mpi", when="+mpi")

    def install(self, spec, prefix):
        # We need git tags
        if os.path.isfile(".git/shallow"):
            git = which("git")
            git("fetch", "--unshallow")
        # Explicitly setting CC, CXX, or FC breaks building libuv, one
        # of Julia's dependencies. This might be a Darwin-specific
        # problem. Given how Spack sets up compilers, Julia should
        # still use Spack's compilers, even if we don't specify them
        # explicitly.
        options = [
            # "CC=cc",
            # "CXX=c++",
            # "FC=fc",
            # "USE_SYSTEM_ARPACK=1",
            # "USE_SYSTEM_FFTW=1",
            # "USE_SYSTEM_GMP=1",
            # "USE_SYSTEM_MPFR=1",
            # "USE_SYSTEM_PCRE=1",
            "prefix=%s" % prefix]
        if "+cxx" in spec:
            if not ("@master" in spec):
                raise InstallError\
                    ("Variant +cxx requires the @master version of Julia")
            options += [
                "BUILD_LLVM_CLANG=1",
                "LLVM_ASSERTIONS=1",
                "USE_LLVM_SHLIB=1"]
        with open('Make.user', 'w') as f:
            f.write('\n'.join(options) + '\n')
        make()
        make("install")
