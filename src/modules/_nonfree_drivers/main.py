#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# === This file is part of Chakra - <http://www.chakraos.org> ===
#
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

def run():
    """ Setup graphics drivers and sound """

    install_path = libcalamares.globalstorage.value( "rootMountPoint" )

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
            ['pacman', '-Rdd', '--noconfirm', 'mesa-libgl', 'xf86-video-nouveau'])
        print('installing driver')
        shutil.copytree(
            '/opt/chakra/pkgs', '%s/opt/chakra/pkgs' % (install_path))
        # search for all nvidia packages and filter out those that have 'xx'
        libcalamares.utils.chroot_call(
                ['pacman', '-Ud', '--force', '--noconfirm'] + [ os.path.join(install_path, "opt/chakra/pkgs", pkg) for pkg in glob.glob('/opt/chakra/pkgs/*nvidia*') if "xx" not in pkg  ])
        shutil.rmtree('%s/opt/chakra/pkgs' % (install_path))

    elif os.path.exists('/tmp/nvidia-340xx'):
        print('nvidia-340xx detected')
        print('removing unneeded packages')
        libcalamares.utils.chroot_call(
            ['pacman', '-Rdd', '--noconfirm', 'mesa-libgl', 'xf86-video-nouveau'])
        print('installing driver')
        shutil.copytree(
            '/opt/chakra/pkgs', '%s/opt/chakra/pkgs' % (install_path))
        libcalamares.utils.chroot_call(
                ['pacman', '-Ud', '--force', '--noconfirm'] + [ os.path.join(install_path, "opt/chakra/pkgs", pkg) for pkg in glob.glob('/opt/chakra/pkgs/*nvidia*340xx*') ])
        shutil.rmtree('%s/opt/chakra/pkgs' % (install_path))

    elif os.path.exists('/tmp/nvidia-304xx'):
        print('nvidia-304xx detected')
        print('removing unneeded packages')
        libcalamares.utils.chroot_call(
            ['pacman', '-Rdd', '--noconfirm', 'mesa-libgl', 'xf86-video-nouveau'])
        print('installing driver')
        shutil.copytree(
            '/opt/chakra/pkgs', '%s/opt/chakra/pkgs' % (install_path))
        libcalamares.utils.chroot_call(
                ['pacman', '-Ud', '--force', '--noconfirm'] + [ os.path.join(install_path, "opt/chakra/pkgs", pkg) for pkg in glob.glob('/opt/chakra/pkgs/*nvidia*304xx*') ])
        shutil.rmtree('%s/opt/chakra/pkgs' % (install_path))

    elif os.path.exists('/tmp/catalyst'):
        print('catalyst detected')
        print('removing unneeded packages')
        libcalamares.utils.chroot_call(
            ['pacman', '-Rdd', '--noconfirm', 'mesa-libgl'])
        print('installing driver')
        shutil.copytree(
            '/opt/chakra/pkgs', '%s/opt/chakra/pkgs' % (install_path))
        libcalamares.utils.chroot_call(
                ['pacman', '-Ud', '--force', '--noconfirm'] + [ os.path.join(install_path, "opt/chakra/pkgs", pkg) for pkg in glob.glob('/opt/chakra/pkgs/*catalyst*') ])
        shutil.rmtree('%s/opt/chakra/pkgs' % (install_path))

    elif os.path.exists('/tmp/virtualbox'):
        print('virtualbox VM detected')
        print('installing virtualbox addons')
        libcalamares.utils.chroot_call(
                ['pacman', '-Ud', '--force', '--noconfirm'] + [ os.path.join(install_path, "opt/chakra/pkgs", pkg) for pkg in glob.glob('/opt/chakra/pkgs/*virtualbox-guest-additions*') ])

    print('done setting up hardware')

    return None
