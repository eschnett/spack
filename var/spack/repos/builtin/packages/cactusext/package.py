from spack import *
import os
import sys

"""
curl -O https://curl.haxx.se/ca/cacert.pem
export CURL_CA_BUNDLE="$(pwd)/cacert.pem"
export PIP_CERT="$(pwd)/cacert.pem"
export SSL_CERT_FILE="$(pwd)/cacert.pem"

source share/spack/setup-env.sh

./bin/install.sh
"""



# Blue Waters [Spack installs, Cactus builds, submit works]:
# Need setup-env.sh work-around
# Need pkgconfig work-around; see <https://github.com/spack/spack/issues/6861>
"""
spack install -j8 gcc %gcc@6.3.0 ^gdbm@1.12
spack install -j8 cactusext %gcc@7.3.0-spack ^gdbm@1.12 ^openmpi fabrics=pmi,pmix,ugni schedulers=alps
"""

# Cedar [Spack installs, Cactus ???builds, submit FAILS (cannot find
# libfabric on compute nodes) / core dump]:
# Build fails. Need to build manually (without distribute?) Or maybe
# need "module purge" before build?
"""
module --force purge
spack install -j8 gcc %gcc@4.8.5
spack install -j8 cactusext %gcc@7.3.0-spack ^openmpi fabrics=pmix,rdma schedulers=slurm
"""

# [???] Comet
# Don't use too many processes while building. OpenBLAS is
# particularly troublesome as it uses many threads for its self-tests.

# Cori [Spack installs, Cactus builds, submit FAILS (MPI error)]:
# Need pkgconfig work-around; see <https://github.com/spack/spack/issues/6861>
# Disable check for H5Py in SimulationIO's CMakeLists.txt; it's
# actually not needed at all
"""
spack install -j8 gcc %gcc@7.1.0
# spack install -j8 cactusext %gcc@7.3.0-spack ^cmake@3.9.4 ^openmpi schedulers=slurm fabrics=pmi,pmix,rdma,ugni
spack install -j8 cactusext %gcc@7.3.0-spack ^openmpi fabrics=pmi,pmix,rdma,ugni schedulers=slurm
"""

# Cori-KNL [using Spack from Cori, Cactus builds, submit FAILS]

# [BROKEN] Edison:
# Disable check for H5Py in SimulationIO's CMakeLists.txt; it's
# actually not needed at all
"""
spack install -j8 gcc %gcc@6.3.0
spack install -j8 cactusext %gcc@7.3.0-edison-spack
"""

# Graham
# Note: Directories on Graham need to have "g+s" mode, so that newly created
# files belong to the group "def-eschnett", instead of the default group
# "eschnett" which has a very low quota. Do not use rsync's "-p" option.
"""
mkdir -p /project/6001779/eschnett/lib
cp /lib64/libc[.-]* /project/6001779/eschnett/lib
cp /lib64/libcrypt[.-]* /project/6001779/eschnett/lib
cp /lib64/libm[.-]* /project/6001779/eschnett/lib
cp /lib64/libpthread[.-]* /project/6001779/eschnett/lib
module --force purge
newgrp def-eschnett
spack install -j8 gcc %gcc@4.8.5
# spack install -j8 cactusext %gcc@7.3.0-spack ^openmpi +thread_multiple ~vt fabrics=pmix,rdma
spack install -j8 cactusext %gcc@7.3.0-spack ^openmpi fabrics=pmix,rdma
"""

# Holodeck [Spack installs, Cactus builds, submit FAILS]
"""
spack install -j10 gcc %gcc@4.9.2
spack install -j10 cactusext %gcc@7.3.0-spack ^openmpi +thread_multiple ~vt fabrics=pmix,rdma
"""

# Niagara
"""
# module --force purge
# newgroup def-eschnett
# spack install -j8 gcc %gcc@4.8.5
# spack install -j8 cactusext %gcc@7.3.0-spack ^openmpi fabrics=pmix,rdma schedulers=slurm
module load gcc/7.3.0
spack install -j8 gcc %gcc@7.3.0
spack install -j8 cactusext %gcc@7.3.0-spack ^openmpi +thread_multiple ~vt fabrics=pmix,rdma
# module load CCEnv
# module load nixpkgs/16.09
# module load gcc/6.4.0
# module load perl/5.22.4
# spack install -j8 gcc %gcc@6.4.0
"""

# Nvidia [Spack installs, Cactus builds, submit works]:
"""
unset MKL
unset MKLROOT
spack install -j4 gcc %gcc@6.3.0
# spack install -j4 cactusext %gcc@7.3.0-spack ^openmpi fabrics=pmix,rdma schedulers=slurm
# spack install -j4 cactusext %gcc@7.3.0-spack ^openmpi fabrics=pmix,rdma
spack install -j4 cactusext %gcc@7.3.0-spack ^openmpi +thread_multiple ~vt fabrics=pmix,rdma
"""

# Redshift [Spack installs, Cactus builds, submit works]:
"""
export PATH=/Users/eschnett/src/spack/bin:/Users/eschnett/bin:/usr/X11R6/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin
unset QTDIR
spack install -j1 gcc %clang@9.0.0-apple
# curl does not build with +libssh2
# spack install -j4 cactusext %gcc@7.3.0-spack ^curl ~libssh2 ^openmpi fabrics=pmix
spack install -j4 cactusext %gcc@7.3.0-spack
"""

# [OLD] Stampede-KNL [on head node]:
"""
module unload intel impi
spack install -j8 gcc %gcc@4.8.5
spack install -j8 cactusext %gcc@7.3.0-spack
"""

# Stampede2 [Spack installs, Cactus builds, submit FAILS]:
# Need to manually add module "gcc/7.1.0" to Spack-generated compiler.yaml
"""
module unload intel impi
module load gcc/7.1.0
spack install -j8 gcc %gcc@7.1.0
spack install -j8 cactusext %gcc@7.3.0-spack ^openmpi fabrics=pmix,rdma schedulers=slurm ^python +ucs4
"""

# Stampede2 SKX [use Spack from Stampede2, Cactus builds, submit FAILS]

# Wheeler [Spack installs, Cactus builds, submit works]:
"""
spack install -j4 gcc %gcc@5.3.0
# spack install -j4 cactusext %gcc@7.3.0-spack ^openmpi fabrics=pmix,verbs schedulers=slurm
# spack install -j4 cactusext %gcc@7.3.0-spack ^openmpi fabrics=pmix,verbs
spack install -j4 cactusext %gcc@7.3.0-spack ^openmpi +thread_multiple ~vt fabrics=pmix,rdma
"""



class Cactusext(Package):
    """Cactus is an open source problem solving environment designed for
    scientists and engineers. Its modular structure easily enables
    parallel computation across different architectures and
    collaborative code development between different groups. Cactus
    originated in the academic research community, where it was
    developed and used over many years by a large international
    collaboration of physicists and computational scientists.
    """
    homepage = "http://www.cactuscode.org"
    url      = "https://github.com/eschnett/empty/archive/1.0.0.tar.gz"

    version("master", "ee69b350db517b309683603bc6bbab14")

    # Cannot install Charm++; it installs many weirdly-named include
    # headers that break other packages
    variant("charm", default=False, description="Enable Charm++")
    variant("cuda", default=False, description="Enable CUDA")
    variant("extras", default=False, description="Enable non-Cactus extras")
    variant("julia", default=False, description="Enable Julia")
    # Cannot combine LLVM and GCC since both provide libgomp
    variant("llvm", default=False, description="Enable LLVM")
    # variant("scalasca", default=False, description="Enable Scalasca")
    variant("rust", default=False, description="Enable Rust")
    variant("valgrind", default=False, description="Enable Valgrind")
    variant("visit", default=False, description="Enable VisIt")

    deps = {}
    whens = {}

    # Actual dependencies
    # deps["adios"] = ["+bzip2", "+hdf5"]
    deps["asdf-cxx"] = []
    # deps["blas"] = []
    deps["boost"] = ["+mpi"]
    deps["cuda"] = []
    deps["fftw"] = ["+mpi", "+openmp"]
    # deps["findutils"] = []
    deps["funhpc"] = []
    deps["gasnet"] = ["+mpi"]
    deps["gdb"] = []
    deps["gsl"] = []
    deps["googletest"] = []
    deps["hdf5"] = ["+fortran", "+cxx", "+hl", "+mpi", "+threadsafe"]
    #TODO deps["hdf5-blosc"] = []
    deps["highfive"] = ["+mpi"]
    # deps["hpx"] = []
    deps["hpx5"] = ["+cxx11", "+metis", "+mpi"]
    deps["hpx5 +cuda"] = ["+cxx11", "+metis", "+mpi"]
    deps["hwloc"] = []
    deps["hwloc +cuda"] = []
    # TODO: kokkos
    # deps["lapack"] = []
    deps["libxsmm"] = ["+header-only"]
    #TODO deps["lmod"] = []
    #TODO deps["lua"] = []
    deps["mpi"] = []
    deps["opencoarrays"] = []
    deps["openssl"] = []
    deps["papi"] = []
    deps["petsc"] = ["+boost", "+hdf5", "+mpi"]
    # deps["py-asdf"] = []   # requires Python @3.3:
    # deps["py-magic-wormhole"] = []
    deps["py-yt"] = []
    deps["rsync"] = []
    # deps["scalasca"] = []   # depends on scorep
    # deps["scorep"] = []   # requires a case sensitive file system
    # deps["tau"] = []   # ["+scorep"]
    deps["simulationio"] = []
    deps["simulationio +julia"] = []
    deps["tmux"] = []
    deps["valgrind"] = []
    deps["vecmathlib"] = []
    deps["visit"] = ["^opengl"]
    deps["zlib"] = []

    # Possible other packages:
    # - adios
    # - boxlib
    # - ccache
    # - gnuplot
    # - hpl
    # - libmng, libpng
    # - likwid
    # - magma
    # - mbedtls
    # - mpich
    # - mvapich2
    # - ninja
    # - paraview
    # - py-flake8
    # - py-ipython
    # - py-jupyter-notebook
    # - rose
    # - samrai
    # - silo
    # - tbb
    # - valgrind

    whens["charm"] = ["+charm"]
    whens["cuda"] = ["+cuda"]
    whens["gasnet"] = ["+extras"]
    whens["gdb"] = ["+extras"]
    whens["highfive"] = ["+extras"]
    whens["hpx5 +cuda"] = ["+cuda"]
    whens["hpx5"] = ["+extras"]
    whens["hwloc +cuda"] = ["+cuda"]
    whens["julia"] = ["+julia"]
    whens["libxsmm"] = ["+extras"]
    whens["llvm"] = ["+llvm"]
    #TODO whens["lua"] = ["+extras"]
    whens["opencoarrays"] = ["+extras"]
    whens["py-ipython"] = ["+extras"]
    whens["py-yt"] = ["+extras"]
    whens["rust"] = ["+rust"]
    whens["simulationio +julia"] = ["+julia"]
    whens["valgrind"] = ["+valgrind"]
    whens["visit"] = ["+visit"]

    # Configure dependencies for convenience

    # Virtual packages
    deps["openblas"] = []
    # deps["openmpi"] = []
    # deps["openmpi"] = ["@:2.999.999 +thread_multiple"] # OpenMPI 3.0.0 hangs
    deps["openmpi"] = ["+thread_multiple ~vt fabrics=pmix"]

    # Unnecessary (?) dependencies:
    # bison, flex, freetype, libevent, libjpeg-turbo, py-matplotlib

    # Initialize dependencies that are mentioned below
    deps["bison"] = []
    deps["bzip2"] = []
    deps["charm"] = []
    deps["cmake"] = []
    deps["flex"] = ["@2.6.3"] # flex@2.6.4 and gcc@7.3.0 conflict (see flex)
    deps["freetype"] = []
    deps["gettext"] = []
    deps["git"] = []
    deps["jemalloc"] = []
    deps["jpeg"] = []
    deps["julia"] = []
    deps["libevent"] = []
    deps["libpng"] = []
    deps["libsigsegv"] = []
    deps["llvm"] = []
    deps["pcre"] = []
    deps["perl"] = []
    deps["pkg-config"] = []
    # deps["py-matplotlib"] = ["+animation"]
    deps["py-matplotlib"] = []
    deps["py-ipython"] = []
    # deps["py-numpy"] = []
    # deps["py-scipy"] = []
    deps["py-setuptools"] = []
    deps["python"] = []
    deps["qhull"] = []
    deps["rust"] = []
    deps["sqlite"] = []
    deps["swig"] = []
    deps["tar"] = []
    deps["tk"] = []
    deps["xz"] = []

    deps["charm"] += ["-netlrts", "+mpi", "+smp"]
    if sys.platform != "darwin":
        deps["charm"] += ["+papi"]
    deps["gettext"] += ["~curses", "~libxml2"]
    deps["julia"] += ["+hdf5", "+mpi", "+simd"]   # "+plots", "+python", "@master"
    if sys.platform == "darwin":
        deps["llvm"] += ["~lldb"]

    # whens["gettext"] = ["+julia"]
    # whens["git"] = ["+julia"]

    # Variants
    deps["pcre"] += ["+jit"]

    # Versions
    # TODO: Remove this once Spack chooses the latest 2.7 version by default
    # deps["python"] += ["@2.7.14"]
    deps["python"] += ["@2.7.13"]
    # py-ipython@6: requires python@3.3:
    deps["py-ipython"] = ["@:5.999.999"]
    # Why?
    deps["py-setuptools"] = ["@:30.999.999"]

    # Compilers
    cactusext_compiler = "gcc@7.3.0-spack"
    darwin_compiler = "clang@9.0.0-apple"
    bison_compiler = cactusext_compiler
    cmake_compiler = cactusext_compiler
    gettext_compiler = cactusext_compiler
    git_compiler = cactusext_compiler
    libevent_compiler = cactusext_compiler
    openssl_compiler = cactusext_compiler
    perl_compiler = cactusext_compiler
    pkg_config_compiler = cactusext_compiler
    python_compiler = cactusext_compiler
    rsync_compiler = cactusext_compiler
    zlib_compiler = cactusext_compiler
    if sys.platform == "darwin":
        bison_compiler = darwin_compiler
        cmake_compiler = darwin_compiler
        gettext_compiler = darwin_compiler
        git_compiler = darwin_compiler      # gcc syslog issue
        libevent_compiler = darwin_compiler # gcc syslog issue
        openssl_compiler = darwin_compiler  # gcc syslog issue
        perl_compiler = darwin_compiler     # gcc syslog issue
        pkg_config_compiler = darwin_compiler
        python_compiler = darwin_compiler
        rsync_compiler = darwin_compiler # gcc syslog issue
        zlib_compiler = darwin_compiler  # used by gcc
    
    deps["bison"].append("%"+bison_compiler)
    deps["cmake"].append("%"+cmake_compiler)
    deps["gettext"].append("%"+gettext_compiler)
    deps["git"].append("%"+git_compiler)
    deps["libevent"].append("%"+libevent_compiler)
    deps["openssl"].append("%"+openssl_compiler)
    deps["perl"].append("%"+perl_compiler)
    deps["pkg-config"].append("%"+pkg_config_compiler)
    deps["py-matplotlib"].append("%"+python_compiler)
    # deps["py-scipy"].append("%"+python_compiler)
    # deps["py-setuptools"].append("%"+python_compiler)
    deps["python"].append("%"+python_compiler)
    deps["rsync"].append("%"+rsync_compiler)
    deps["zlib"].append("%"+zlib_compiler)
    
    deps["fftw"].append("%"+cactusext_compiler)
    deps["freetype"].append("%"+cactusext_compiler)
    deps["gsl"].append("%"+cactusext_compiler)
    deps["hdf5"].append("%"+cactusext_compiler)
    #TODO deps["hdf5-blosc"].append("%"+cactusext_compiler)
    deps["hwloc"].append("%"+cactusext_compiler)
    deps["jpeg"].append("%"+cactusext_compiler)
    deps["libpng"].append("%"+cactusext_compiler)
    #TODO deps["lmod"].append("%"+cactusext_compiler)
    #TODO deps["lua"].append("%"+cactusext_compiler)
    deps["papi"].append("%"+cactusext_compiler)
    deps["petsc"].append("%"+cactusext_compiler)
    deps["qhull"].append("%"+cactusext_compiler)
    # deps["py-numpy"].append("%"+cactusext_compiler)
    # deps["scalasca"].append("%"+cactusext_compiler)
    # deps["scorep"].append("%"+cactusext_compiler)
    # deps["tau"].append("%"+cactusext_compiler)
    deps["tar"].append("%"+cactusext_compiler)
    deps["tk"].append("%"+cactusext_compiler)
    
    deps["openblas"].append("%"+cactusext_compiler)
    deps["openmpi"].append("%"+cactusext_compiler)
    
    deps["charm"].append("%"+cactusext_compiler)
    deps["funhpc"].append("%"+cactusext_compiler)
    deps["julia"].append("%"+cactusext_compiler)
    deps["llvm"].append("%"+cactusext_compiler)
    deps["rust"].append("%"+cactusext_compiler)
    deps["simulationio"].append("%"+cactusext_compiler)
    
    # These are apparently not deduced -- why?
    deps["bzip2"].append("%"+cactusext_compiler)
    deps["libsigsegv"].append("%"+cactusext_compiler)
    deps["sqlite"].append("%"+cactusext_compiler)
    deps["swig"].append("%"+cactusext_compiler)
    deps["xz"].append("%"+cactusext_compiler)

    # Set dependencies
    for pkg, opts in sorted(deps.iteritems()):
        try:
            when = " ".join(whens[pkg])
        except:
            when = None
        depends_on(pkg + " " + " ".join(opts), when=when)

    def install(self, spec, prefix):
        # This package does not install anything per se; it only
        # installs many of the dependencies that Cactus-based
        # applications require.
        mkdirp(prefix.lib)
