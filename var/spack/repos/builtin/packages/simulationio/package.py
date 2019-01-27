# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Simulationio(CMakePackage):
    """SimulationIO: Efficient and convenient I/O for large PDE simulations"""

    homepage = "https://github.com/eschnett/SimulationIO"
    url      = "https://github.com/eschnett/SimulationIO/archive/version/0.1.0.tar.gz"
    git      = "https://github.com/eschnett/SimulationIO.git"

    version('8.0.0', sha256='c46e84d1ecc3ee3e9f77a25fdb6bdc1ae2ca69c59ce4f2f929e33f4854acfa14')
    version('7.6.0', sha256='805cfb5c3ef579c23688edaadeeaadcf84e13515f16d9256d2e955c12b2f1fcc')
    version('7.5.0', sha256='a0e7ced42db11247ba879343f63543e33cf6f7ebdcd90d574999c33421329e06')
    version('7.4.0', sha256='f80a75a7b568d2ad18e2ead78af529ecaebba35430aec347565299bd3c70d259')
    version('7.3.0', sha256='e8f1288b0f36d8ef7649b909724ac54e0c79af76fa1ff99668215c4b62483e49')
    version('7.2.0', '26eb9d17c064ef1e03fd4590cc6b9f51')
    version('7.1.0', '5e099beb3253732e7224063b2b6e2364')
    version('7.0.0', '29e81342c77c00de878ed18ad9ce9afd')
    version('6.0.0', '2657ad8b93d5d9b9f43bcac3ad290f38')
    version('5.0.0', '815c91eaefad1f9eee53f826f1a99afd')
    version('2.17.0', 'fd68eda3f1a58a245b4165dabd134aaa')
    version('2.16.1', 'd81acb33544c22aa3ed1f8e343693c4b')
    version('2.16.0', '59c635c90868b773f9d278d25b03510f')
    version('2.15.0', 'db02c981e2b7b970d8d26520b13a5a44')
    version('2.13.0', '6702c4e4b8fd8c8a23b2b816ab420e01')
    version('2.12.0', 'a62722574c47753572541219b9328d7f')
    version('2.11.0', '5778c3f9ad847a4a4a5cae1b39436b37')
    version('2.10.0', '95fb2de260399e92d15a7628f1f0607a')
    version('2.9.0', '1b6e616b6c43a4cf2b60a8905c6f4e77')
    version('2.8.0', '013774fa0b521260dfbca840221a5bcd')
    version('2.7.1', 'd14cd62dadad87de82f505bcec48ae8a')
    version('2.7.0', '73fc57f3e4e2114adebdb3c8d6b11c0f')
    version('2.6.0', 'a819e1907b470d95fda0cfe9ca34a063')
    version('2.2.0', '2284d3908767986ef0c3c9d92397cebe')
    version('2.1.0', 'f8dab2873a4d277e9a655a58bb9f259c')
    version('2.0.0', 'e831b10641a6091c12cd0cb3bc2b228d')
    version('1.0.1', '5cbf1d0084eb436d861ffcdd297eaa08')
    version('1.0.0', '5cbf1d0084eb436d861ffcdd297eaa08')
    version('0.1.0', '00f7dabc08ed1ab77858785ce0809f50')

    variant('asdf-cxx', default=True)
    variant('hdf5', default=True)
    variant('julia', default=False)
    variant('python', default=True)

    variant('pic', default=True,
            description="Produce position-independent code")

    depends_on('asdf-cxx @2.1.0:2.999.999', when='@2.0.0:2.999.999 +asdf-cxx')
    depends_on('asdf-cxx @4.0.1:', when='@5.0.0: +asdf-cxx')
    depends_on('asdf-cxx @6.3.0:6.999.999', when='@6.0.0:7.999.999 +asdf-cxx')
    depends_on('asdf-cxx @7.0.0:', when='@8.0.0: +asdf-cxx')
    depends_on('hdf5 +cxx @:1.10.0-patch1', when='+hdf5 @:1.999.999')
    depends_on('hdf5 +cxx @1.10.1:', when='+hdf5 @2.0.0:')
    depends_on('julia', when='+julia', type=('build', 'run'))
    depends_on('py-h5py', when='+python', type=('build', 'run'))
    depends_on('py-numpy', when='+python', type=('build', 'run'))
    depends_on('python@2.7:2.8', when='+python', type=('build', 'run'))
    depends_on('swig', type='build')

    extends('python')

    def cmake_args(self):
        spec = self.spec
        options = []
        if '~asdf-cxx' in spec:
            options.append("-DENABLE_ASDF_CXX=OFF")
        if '~hdf5' in spec:
            options.append("-DENABLE_HDF5=OFF")
        if '+pic' in spec:
            options.append("-DCMAKE_POSITION_INDEPENDENT_CODE:BOOL=true")
        return options

    def check(self):
        with working_dir(self.build_directory):
            make("test", "CTEST_OUTPUT_ON_FAILURE=1")
