##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
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


class PyMagicWormhole(PythonPackage):
    """get things from one computer to another, safely"""

    homepage = "https://github.com/warner/magic-wormhole"
    url      = "https://github.com/warner/magic-wormhole/archive/0.10.2.tar.gz"

    version('0.10.2', '45069304baafc1eab9cc43f16e55066f')

    depends_on('autobahn @0.14.1:', type=('build', 'run'))
    depends_on('automat', type=('build', 'run'))
    depends_on('click', type=('build', 'run'))
    depends_on('hkdf', type=('build', 'run'))
    depends_on('humanize', type=('build', 'run'))
    depends_on('ipaddress', type=('build', 'run'))
    depends_on('py-pip', type='build')
    depends_on('pynacl', type=('build', 'run'))
    depends_on('python @2.7:2.8,3.4:3.6')
    depends_on('six', type=('build', 'run'))
    depends_on('spake2 @0.7', type=('build', 'run'))
    depends_on('tqdm @4.13.0:', type=('build', 'run'))
    depends_on('twisted @17.5.0:', type=('build', 'run'))
    depends_on('txtorcon @0.19.3:', type=('build', 'run'))

    def install(self, spec, prefix):
        pip = which('pip')
        pip('install', self.stage.archive_file, '--prefix={0}'.format(prefix))
