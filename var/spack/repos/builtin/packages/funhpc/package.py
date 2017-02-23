from spack import *

class Funhpc(CMakePackage):
    """FunHPC: Functional HPC Programming"""
    homepage = "https://bitbucket.org/eschnett/funhpc.cxx"
    url= "https://github.com/eschnett/FunHPC.cxx/archive/version/0.1.0.tar.gz"

    version('0.1.1', 'b8c1dad706409869fd77efd7b79cc571')
    version('0.1.0', 'eee8265c372edb4615ba2128bf0db63d')
    version('master',
            git='https://bitbucket.org/eschnett/funhpc.cxx', branch='master')

    variant('pic', default=True,
            description="Produce position-independent code")

    depends_on('cereal')
    depends_on('hwloc')
    depends_on('jemalloc')
    depends_on('mpi')
    depends_on('qthreads')

    def cmake_args(self):
        spec = self.spec
        options = []
        if '+pic' in spec:
            options.extend(["-DCMAKE_POSITION_INDEPENDENT_CODE:BOOL=true"])
        return options
