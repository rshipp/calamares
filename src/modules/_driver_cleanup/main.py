#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# === This file is part of Chakra - <http://www.chakraos.org> ===
#
#   Copyright 2014 KaOS (http://kaosx.us)
#   Copyright 2015 Chakra (http://www.chakraos.org)
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
#  MA 02110-1301, USA.

import os
import subprocess

import libcalamares


def run():
    """ Clean up unused drivers """

    print('cleaning up video drivers')

    install_path = libcalamares.globalstorage.value("rootMountPoint")

    # remove any db.lck
    db_lock = os.path.join(install_path, "var/lib/pacman/db.lck")
    if os.path.exists(db_lock):
        with misc.raised_privileges():
            os.remove(db_lock)

    """ Clean up Xorg drivers """
    all_drivers = []
    loaded_modules = []
    # read the current installed xorg drivers
    p = subprocess.Popen("pacman -Q | grep xf86-video | cut -d '-' -f 3 | cut -d ' ' -f 1",
                         shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    # Iterates over every found pkg and put each one in a list
    for line in p.stdout.readlines():
        s = line.decode('ascii')
        s = s.rstrip('\n')
        all_drivers.append(s)

    # read the current used modules
    p = subprocess.Popen("lsmod | cut -d' ' -f1",
                         shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    # Iterates over every module found and put each one in a list
    for line in p.stdout.readlines():
        s = line.decode('ascii')
        s = s.rstrip('\n')
        loaded_modules.append(s)

    # adapt some special names to fit the xorg pkg name
    if "radeon" in loaded_modules:
        loaded_modules.append("ati")
    if "i915" in loaded_modules:
        loaded_modules.append("intel")

    # get the list of used drivers by comparing the modules list and the installed drivers
    keep_driver = list(set(all_drivers) & set(loaded_modules))
    # do not remove vesa, add it to the list
    keep_driver.append("vesa")
    
    # Remove every xorg driver not loaded
    for driver in all_drivers:
        if not driver in keep_driver:
            print('Removing xorg driver: ', driver)
            libcalamares.utils.chroot_call(
                ['pacman', '-Rddn', '--noconfirm', 'xf86-video-%s' % (driver)])
    

    print('video driver removal complete')

    print('cleaning up input drivers')

    xorg = open("/var/log/Xorg.0.log",  errors="surrogateescape").read()
    if 'wacom' in xorg:
        print('wacom in use')
    else:
        try:
            libcalamares.utils.chroot_call(['pacman', '-Rncs', '--noconfirm',
                                            'xf86-input-wacom'])
        except Exception as e:
            pass
    if 'synaptics' in xorg:
        print('synaptics in use')
    else:
        try:
            libcalamares.utils.chroot_call(['pacman', '-Rncs', '--noconfirm',
                                            'xf86-input-synaptics'])
        except Exception as e:
            pass

    print('input driver removal complete')

    print('job_cleanup_drivers')

    return None
