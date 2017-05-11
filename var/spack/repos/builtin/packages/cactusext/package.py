from spack import *
import os
import sys

# Blue Waters:
# $ spack install -j16 gcc ~binutils %gcc@6.2.0
# $ spack install -j16 cactusext +cuda +julia +valgrind %gcc@7.1.0-spack ^gdbm@1.12

# Comet: Don't use too many processes while building. OpenBLAS is
# particularly troublesome as it uses many threads for its self-tests.

# Cori: Disable check for H5Py in SimulationIO's CMakeLists.txt; it's
# actually not needed at all

# Stampede: Build on compute node [broken]
# module unload intel
# module unload mvapich2
# # spack install cactusext %gcc@7.1.0-spack ^hdf5 ldflags='-L/work/00507/eschnett/lib' ^c-blosc ~avx2
# spack install cactusext %gcc@7.1.0-spack ^c-blosc ~avx2

# Stampede-KNL [on head node]:
# module unload intel impi
# spack install -j8 gcc %gcc@4.8.5
# spack install -j8 cactusext +julia +valgrind %gcc@7.1.0-spack

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
    variant("extras", default=True, description="Enable non-Cactus extras")
    variant("julia", default=False, description="Enable Julia")
    # Cannot combine LLVM and GCC since both provide libgomp
    variant("llvm", default=False, description="Enable LLVM")
    # variant("scalasca", default=False, description="Enable Scalasca")
    variant("rust", default=False, description="Enable Rust")
    variant("valgrind", default=False, description="Enable Valgrind")

    deps = {}
    whens = {}

    # Actual dependencies
    # deps["blas"] = []
    deps["boost"] = ["+mpi"]
    deps["cuda"] = []
    deps["fftw"] = ["+mpi", "+openmp"]
    deps["funhpc"] = []
    deps["gasnet"] = ["+mpi"]
    deps["gdb"] = []
    deps["gsl"] = []
    deps["googletest"] = []
    deps["hdf5"] = ["+mpi"]
    deps["hdf5-blosc"] = []
    deps["highfive"] = ["+mpi"]
    deps["hpx5"] = ["+cxx11", "+metis", "+mpi"]
    deps["hpx5 +cuda"] = ["+cxx11", "+metis", "+mpi"]
    deps["hwloc"] = []
    deps["hwloc +cuda"] = []
    # TODO: kokkos
    # deps["lapack"] = []
    deps["libxsmm"] = ["+header-only"]
    deps["lmod"] = []
    deps["lua"] = []
    deps["mpi"] = []
    deps["opencoarrays"] = []
    deps["openssl"] = []
    deps["papi"] = []
    deps["petsc"] = ["+boost", "+hdf5", "+mpi"]
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
    whens["lua"] = ["+extras"]
    whens["opencoarrays"] = ["+extras"]
    whens["py-ipython"] = ["+extras"]
    whens["py-yt"] = ["+extras"]
    whens["rust"] = ["+rust"]
    whens["simulationio +julia"] = ["+julia"]
    whens["valgrind"] = ["+valgrind"]

    # Configure dependencies for convenience

    # Virtual packages
    deps["openblas"] = []
    deps["openmpi"] = []
    # if sys.platform.startswith("linux"):
    #     deps["openmpi"] += ["fabrics=verbs +rdma"]

    # Initialize dependencies that are mentioned below
    deps["bison"] = []
    deps["bzip2"] = []
    deps["charm"] = []
    deps["cmake"] = []
    deps["freetype"] = []
    deps["gettext"] = []
    deps["git"] = []
    deps["jemalloc"] = []
    deps["jpeg"] = []
    deps["julia"] = []
    deps["libpng"] = []
    deps["libsigsegv"] = []
    deps["llvm"] = []
    deps["pkg-config"] = []
    deps["py-matplotlib"] = []
    deps["py-ipython"] = []
    # deps["py-numpy"] = []
    # deps["py-scipy"] = []
    deps["py-setuptools"] = []
    deps["python"] = []
    deps["qhull"] = []
    deps["rust"] = []
    deps["sqlite"] = []
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

    # Versions
    # TODO: Remove this once Spack chooses the latest 2.7 version by default
    deps["python"] += ["@2.7.13"]
    # py-ipython@6: requires python@3.3:
    deps["py-ipython"] = ["@:5.999.999"]
    # Why?
    deps["py-setuptools"] = ["@:30.999.999"]

    # Compilers
    cactusext_compiler = "gcc@7.1.0-spack"
    darwin_compiler = "clang@8.1.0-apple"
    bison_compiler = cactusext_compiler
    cmake_compiler = cactusext_compiler
    gettext_compiler = cactusext_compiler
    pkg_config_compiler = cactusext_compiler
    python_compiler = cactusext_compiler
    if sys.platform == "darwin":
        bison_compiler = darwin_compiler
        cmake_compiler = darwin_compiler
        gettext_compiler = darwin_compiler
        pkg_config_compiler = darwin_compiler
        python_compiler = darwin_compiler
    
    deps["bison"].append("%"+bison_compiler)
    deps["cmake"].append("%"+cmake_compiler)
    deps["gettext"].append("%"+gettext_compiler)
    deps["pkg-config"].append("%"+pkg_config_compiler)
    deps["py-matplotlib"].append("%"+python_compiler)
    # deps["py-scipy"].append("%"+python_compiler)
    # deps["py-setuptools"].append("%"+python_compiler)
    deps["python"].append("%"+python_compiler)
    
    deps["fftw"].append("%"+cactusext_compiler)
    deps["freetype"].append("%"+cactusext_compiler)
    deps["gsl"].append("%"+cactusext_compiler)
    deps["hdf5"].append("%"+cactusext_compiler)
    deps["hdf5-blosc"].append("%"+cactusext_compiler)
    deps["hwloc"].append("%"+cactusext_compiler)
    deps["jpeg"].append("%"+cactusext_compiler)
    deps["libpng"].append("%"+cactusext_compiler)
    deps["lmod"].append("%"+cactusext_compiler)
    deps["lua"].append("%"+cactusext_compiler)
    deps["openssl"].append("%"+cactusext_compiler)
    deps["papi"].append("%"+cactusext_compiler)
    deps["petsc"].append("%"+cactusext_compiler)
    deps["qhull"].append("%"+cactusext_compiler)
    # deps["py-numpy"].append("%"+cactusext_compiler)
    # deps["scalasca"].append("%"+cactusext_compiler)
    # deps["scorep"].append("%"+cactusext_compiler)
    # deps["tau"].append("%"+cactusext_compiler)
    deps["tar"].append("%"+cactusext_compiler)
    deps["tk"].append("%"+cactusext_compiler)
    deps["zlib"].append("%"+cactusext_compiler)
    
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
