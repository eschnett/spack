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
import shutil


class PlanckLikelihood(Package):
    """2015 Cosmic Microwave Background (CMB) spectra and likelihood code"""

    homepage = "https://wiki.cosmos.esa.int/planckpla2015/index.php/CMB_spectrum_%26_Likelihood_Code"
    url      = "http://irsa.ipac.caltech.edu/data/Planck/release_2/software/COM_Likelihood_Code-v2.0.R2.00.tar.bz2"

    version('2.00', '7a081679ff249dc4f94fb7177e16e818')

    resource(
        name = 'baseline',
        url = "http://irsa.ipac.caltech.edu/data/Planck/release_2/software/COM_Likelihood_Data-baseline_R2.00.tar.gz",
        md5 = '7e784819cea65dbc290ea3619420295a',
        destination = '.')
    # resource(
    #     name = 'lensing-ext',
    #     url = "http://irsa.ipac.caltech.edu/data/Planck/release_2/software/COM_Likelihood_Data-extra-lensing-ext.R2.00.tar.gz",
    #     md5 = '091736f73b47a09162050bee27d68399',
    #     destination = '.')
    # resource(
    #     name = 'plik-DS',
    #     url = "http://irsa.ipac.caltech.edu/data/Planck/release_2/software/COM_Likelihood_Data-extra-plik-DS.R2.00.tar.gz",
    #     md5 = '76ac04f989025eecab3825aba7e41f36',
    #     destination = '.')
    # resource(
    #     name = 'plik-HM-ext',
    #     url = "http://irsa.ipac.caltech.edu/data/Planck/release_2/software/COM_Likelihood_Data-extra-plik-HM-ext.R2.00.tar.gz",
    #     md5 = '1c3bd8221f973b7bf7e76647451fd6e5',
    #     destination = '.')
    # resource(
    #     name = 'plik-unbinned',
    #     url = "http://irsa.ipac.caltech.edu/data/Planck/release_2/software/COM_Likelihood_Data-extra-plik-unbinned.R2.00.tar.gz",
    #     md5 = 'c5869aa6b6581b6863d2a6e0ffd3826c',
    #     destination = '.')

    depends_on('blas')
    depends_on('cfitsio +shared')
    depends_on('lapack')

    # Note: Could also install Python bindings

    parallel = False

    def install(self, spec, prefix):
        # Configure
        makeflags=[
            'PREFIX=%s' % prefix,
            'CFITSIOPATH=%s' % spec['cfitsio'].prefix,
            'CC=cc',
            'FC=fc',
            'IFORTLIBPATH=',
            'IFORTRUNTIME=',
            'GFORTRANLIBPATH=',
            'GFORTRANRUNTIME=-lgfortran -lgomp',
            'LAPACKLIBPATH=',
            'LAPACK=%s %s' % (spec['lapack'].lapack_libs.joined(),
                              spec['blas'].blas_libs.joined()),
            'COPENMP=%s' % self.compiler.openmp_flag,
            'FOPENMP=%s' % self.compiler.openmp_flag,
        ]

        # Build
        make(*makeflags)

        # Install
        make('install', *makeflags)
        fix_darwin_install_name(prefix.lib)
        for res in [
            'plc_2.0',
            # 'lensing_ext',
            # 'plik_DS',
            # 'plik_HM_ext',
            # 'plik_unbinned',
        ]:
            shutil.move(res, join_path(prefix, 'share', 'clik', res))

    def setup_dependent_environment(self, module, spec, dep_spec):
        prefix = self.prefix
        os.environ['CLIK_PATH'] = prefix
        os.environ['CLIK_DATA'] = join_path(prefix, 'share', 'clik')
        os.environ['CLIK_PLUGIN'] = 'rel2015'

    def setup_environment(self, spack_env, run_env):
        prefix = self.prefix
        run_env.set('CLIK_PATH', prefix)
        run_env.set('CLIK_DATA', join_path(prefix, 'share', 'clik'))
        run_env.set('CLIK_PLUGIN', 'rel2015')

    @AutotoolsPackage.sanity_check('install')
    def check_install(self):
        prefix = self.prefix
        clik_example_C = Executable(join_path(prefix.bin, 'clik_example_C'))
        shutil.rmtree('spack-check')
        with working_dir('spack-check', create=True):
            clik_example_C(join_path(prefix, 'share', 'clik',
                                     'plc_2.0', 'hi_l', 'plik',
                                     'plik_dx11dr2_HM_v18_TT.clik'))
        shutil.rmtree('spack-check')
