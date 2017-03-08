from spack import *
import os
import sys

# Comet: Don't use too many processes while building. OpenBLAS is
# particularly troublesome as it uses many threads for its self-tests.

# Cori: Disable check for H5Py in SimulationIO's CMakeLists.txt; it's
# actually not needed at all

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
    variant("funhpc", default=False, description="Enable FunHPC")
    variant("julia", default=False, description="Enable Julia")
    # Cannot combine LLVM and GCC since both provide libgomp
    variant("llvm", default=False, description="Enable LLVM")
    # variant("scalasca", default=False, description="Enable Scalasca")
    variant("rust", default=False, description="Enable Rust")
    variant("simulationio", default=False, description="Enable SimulationIO")

    deps = {}
    whens = {}

    # Actual dependencies
    # deps["blas"] = []
    deps["boost"] = ["+mpi"]
    deps["cuda"] = []
    deps["fftw"] = ["+mpi", "+openmp"]
    deps["gsl"] = []
    deps["hdf5"] = ["+mpi"]
    deps["hdf5-blosc"] = []
    deps["hwloc"] = []
    # deps["lapack"] = []
    deps["libxsmm"] = []
    deps["lmod"] = []
    deps["lua"] = []
    deps["mpi"] = []
    deps["opencoarrays"] = []
    deps["openssl"] = []
    deps["papi"] = []
    deps["petsc"] = ["+boost", "+hdf5", "+mpi"]
    deps["py-yt"] = []
    # deps["scalasca"] = []   # depends on scorep
    # deps["scorep"] = []   # requires a case sensitive file system
    # deps["tau"] = []   # ["+scorep"]
    deps["tmux"] = []
    deps["zlib"] = []

    whens["charm"] = ["+charm"]
    whens["cuda"] = ["+cuda"]
    whens["funhpc"] = ["+funhpc"]
    whens["julia"] = ["+julia"]

    whens["llvm"] = ["+llvm"]
    whens["rust"] = ["+rust"]
    whens["simulationio"] = ["+simulationio"]
    whens["simulationio+julia"] = ["+simulationio+julia"]

    # Configure dependencies for convenience

    # Virtual packages
    deps["openblas"] = []
    deps["openmpi"] = []

    # Initialize dependencies that are mentioned below
    deps["bison"] = []
    deps["bzip2"] = []
    deps["charm"] = ["-netlrts", "+mpi", "+smp"]
    if sys.platform != "darwin":
        deps["charm"].append("+papi")
    deps["cmake"] = []
    deps["freetype"] = []
    deps["funhpc"] = []
    deps["gettext"] = ["~libxml2"]
    deps["git"] = []
    deps["jemalloc"] = []
    deps["jpeg"] = []
    deps["julia"] = ["+hdf5", "+mpi"]   # "+plots", "+python", "@master"
    deps["libpng"] = []
    deps["libsigsegv"] = []
    deps["llvm"] = []
    deps["pkg-config"] = []
    deps["py-matplotlib"] = []
    deps["python"] = []
    deps["qhull"] = []
    deps["rust"] = []
    deps["simulationio"] = []
    deps["simulationio+julia"] = []
    deps["sqlite"] = []
    deps["tar"] = []
    deps["tk"] = []
    deps["xz"] = [] = []

    whens["gettext"] = ["+julia"]
    whens["git"] = ["+julia"]
    whens["jemalloc"] = ["+funhpc"]

    # # Versions
    # TODO: Remove this once Spack chooses the latest 2.7 version by default
    deps["python"].append("@2.7.13")
    # # TODO: Remove this once Spack chooses the latest correct version by default
    # deps["openssl"].append("@:1.0")

    # Compilers
    cactusext_compiler = "gcc@spack-6.3.0"
    darwin_compiler = "clang@8.0.0-apple"
    bison_compiler = cactusext_compiler
    cmake_compiler = cactusext_compiler
    gettext_compiler = cactusext_compiler
    py_matplotlib_compiler = cactusext_compiler
    pkg_config_compiler = cactusext_compiler
    python_compiler = cactusext_compiler
    if sys.platform == "darwin":
        bison_compiler = darwin_compiler
        cmake_compiler = darwin_compiler
        gettext_compiler = darwin_compiler
        py_matplotlib_compiler = darwin_compiler
        pkg_config_compiler = darwin_compiler
        python_compiler = darwin_compiler

    deps["bison"].append("%"+bison_compiler)
    deps["cmake"].append("%"+cmake_compiler)
    deps["gettext"].append("%"+gettext_compiler)
    deps["pkg-config"].append("%"+pkg_config_compiler)
    deps["py-matplotlib"].append("%"+py_matplotlib_compiler)
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
