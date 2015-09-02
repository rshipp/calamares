#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# === This file is part of Chakra - <http://www.chakraos.org> ===
#
#   Copyright 2014, KaOS (http://kaosx.us)
#   Copyright 2015, Luca Giambonini <gluca86@gmail.com>
#
#   Calamares is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   Calamares is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with Calamares. If not, see <http://www.gnu.org/licenses/>.

import os
import shutil
import glob

import libcalamares
from .. import pacman_utils

def run():
    """ Setup graphics drivers and sound """

    install_path = libcalamares.globalstorage.value("rootMountPoint")

    # remove any db.lck
    db_lock = os.path.join(install_path, "var/lib/pacman/db.lck")
    if os.path.exists(db_lock):
        with misc.raised_privileges():
            os.remove(db_lock)

    # setup proprietary drivers, if detected
    print('setup proprietary drivers')

    if os.path.exists('/tmp/nvidia'):
        print('nvidia detected')
        print('removing unneeded packages')
        libcalamares.utils.chroot_call(
            ['pacman', '-Rdd', '--noconfirm', 'libgl', 'xf86-video-nouveau'])
        print('installing driver')
        shutil.copytree(
            '/opt/chakra/pkgs', '%s/opt/chakra/pkgs' % install_path)
        for nvidia_utils in glob.glob('/opt/chakra/pkgs/nvidia-utils-3*'):
            if 'xx' not in nvidia_utils:
                libcalamares.utils.chroot_call(
                    ['pacman', '-Ud', '--force', '--noconfirm', nvidia_utils])
        for nvidia in glob.glob('/opt/chakra/pkgs/nvidia-3*'):
            if 'xx' not in nvidia:
                libcalamares.utils.chroot_call(
                    ['pacman', '-Ud', '--force', '--noconfirm', nvidia])
        shutil.rmtree('%s/opt/chakra/pkgs' % install_path)
    elif os.path.exists('/tmp/nvidia-340xx'):
        print('nvidia-340xx detected')
        print('removing unneeded packages')
        libcalamares.utils.chroot_call(
            ['pacman', '-Rdd', '--noconfirm', 'libgl', 'xf86-video-nouveau'])
        print('installing driver')
        shutil.copytree(
            '/opt/chakra/pkgs', '%s/opt/chakra/pkgs' % install_path)
        for nvidia_340_utils in glob.glob('/opt/chakra/pkgs/nvidia-340xx-utils*'):
            libcalamares.utils.chroot_call(
                ['pacman', '-Ud', '--force', '--noconfirm', nvidia_340_utils])
        for nvidia_340 in glob.glob('/opt/chakra/pkgs/nvidia-340xx*'):
            libcalamares.utils.chroot_call(
                ['pacman', '-Ud', '--force', '--noconfirm', nvidia_340])
        shutil.rmtree('%s/opt/chakra/pkgs' % install_path)
    elif os.path.exists('/tmp/nvidia-304xx'):
        print('nvidia-304xx detected')
        print('removing unneeded packages')
        libcalamares.utils.chroot_call(
            ['pacman', '-Rdd', '--noconfirm', 'libgl', 'xf86-video-nouveau'])
        print('installing driver')
        shutil.copytree(
            '/opt/chakra/pkgs', '%s/opt/chakra/pkgs' % install_path)
        for nvidia_304_utils in glob.glob('/opt/chakra/pkgs/nvidia-304xx-utils*'):
            libcalamares.utils.chroot_call(
                ['pacman', '-Ud', '--force', '--noconfirm', nvidia_304_utils])
        for nvidia_304 in glob.glob('/opt/chakra/pkgs/nvidia-304xx*'):
            libcalamares.utils.chroot_call(
                ['pacman', '-Ud', '--force', '--noconfirm', nvidia_304])
        shutil.rmtree('%s/opt/chakra/pkgs' % install_path)
    elif os.path.exists('/tmp/catalyst'):
        print('catalyst detected')
        print('removing unneeded packages')
        libcalamares.utils.chroot_call(
            ['pacman', '-Rdd', '--noconfirm', 'libgl'])
        print('installing driver')
        shutil.copytree(
            '/opt/chakra/pkgs', '%s/opt/chakra/pkgs' % install_path)
        for catalyst_utils in glob.glob('/opt/chakra/pkgs/catalyst-utils*'):
            libcalamares.utils.chroot_call(
                ['pacman', '-Ud', '--force', '--noconfirm', catalyst_utils])
        for catalyst in glob.glob('/opt/chakra/pkgs/catalyst-1*'):
            libcalamares.utils.chroot_call(
                ['pacman', '-Ud', '--force', '--noconfirm', catalyst])
        shutil.rmtree('%s/opt/chakra/pkgs' % install_path)

    print('done setting up hardware')

    return None
