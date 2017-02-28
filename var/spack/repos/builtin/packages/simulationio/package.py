from spack import *
import glob
import os

class Simulationio(CMakePackage):
    """SimulationIO: Efficient and convenient I/O for large PDE simulations"""
    homepage = "https://github.com/eschnett/SimulationIO"
    url= "https://github.com/eschnett/SimulationIO/archive/version/0.1.0.tar.gz"

    # version('0.1.0', '00f7dabc08ed1ab77858785ce0809f50')
    version('master',
            git='https://github.com/eschnett/SimulationIO.git', branch='master')
    version('cmake',
            git='https://github.com/eschnett/SimulationIO.git',
            branch='eschnett/cmake')

    variant('julia', default=False)
    variant('python', default=True)

    variant('pic', default=True,
            description="Produce position-independent code")

    depends_on('julia', when='+julia', type=('build', 'run'))
    depends_on('py-h5py', when='+python', type=('build', 'run'))
    depends_on('py-numpy', when='+python', type=('build', 'run'))
    depends_on('python@2.7.0:2.999.999', when='+python', type=('build', 'run'))
    depends_on('swig', type='build')

    def cmake_args(self):
        spec = self.spec
        pythonpath = (
            glob.glob(join_path(spec['py-h5py'].prefix, "lib", "python2.7",
                                "site-packages", "h5py-*")) +
            glob.glob(join_path(spec['py-numpy'].prefix, "lib", "python2.7",
                                "site-packages", "numpy-*")))
        try:
            pythonpath.append(os.environ["PYTHONPATH"])
        except KeyError:
            pass
        os.environ["PYTHONPATH"] = ":".join(pythonpath)
        options = []
        if '+pic' in spec:
            options.append("-DCMAKE_POSITION_INDEPENDENT_CODE:BOOL=true")
        return options

    def check(self):
        with working_dir(self.build_directory):
            make("test", "CTEST_OUTPUT_ON_FAILURE=1")
