#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# === This file is part of Calamares - <http://github.com/calamares> ===
#
#   Copyright 2014-2016, Luca Giambonini <almack@chakraos.org>
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
import sys
import glob
import errno

import libcalamares


def run():
    """ Package removal module. Live only packages, surplus language packs """

    install_path = libcalamares.globalstorage.value("rootMountPoint")
    fw_type = libcalamares.globalstorage.value("firmwareType")

    # remove any db.lck
    db_lock = os.path.join(install_path, "var/lib/pacman/db.lck")
    if os.path.exists(db_lock):
        with misc.raised_privileges():
            os.remove(db_lock)


    # Install postinall packages located in the pacman cache
    #path = install_path + '/var/cache/pacman/pkg/'
    #files = glob.glob(path + '*.tar.gz')
    #for name in files:
    #    try:
    #        print('Installing: ', name)
    #        libcalamares.globalstorage.insert("packageOperations", {'localInstall': [os.path.join(path, name)]})
    #    except IOError as exc:
    #        if exc.errno != errno.EISDIR: # Do not fail if a directory is found, just ignore it.
    #            raise # Propagate other kinds of IOError.


    # Remove surplus bootloader packages
    if fw_type == 'efi':
        print('Removing grub packages')
        libcalamares.utils.chroot_call(
            ['pacman', '-Rns', '--noconfirm', 'grub', 'grub2-themes-sirius', 'grub2-editor'])

    if fw_type == 'bios':
        print('Removing EFI packages')
        libcalamares.utils.chroot_call(
            ['pacman', '-Rns', '--noconfirm', 'efibootmgr'])

    print('package removal completed')
