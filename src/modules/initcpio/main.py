#!/usr/bin/env python3
# encoding: utf-8
# === This file is part of Calamares - <http://github.com/calamares> ===
#
#   Copyright 2014, Philip Müller <philm@manjaro.org>
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
import subprocess

import libcalamares

def get_cpu(self):
    # Check if system is an intel system. Not sure if we want to move this to hardware module when its done.
    process1 = subprocess.Popen(["hwinfo", "--cpu"], stdout=subprocess.PIPE)
    process2 = subprocess.Popen(["grep", "Model:[[:space:]]"],
                                stdin=process1.stdout, stdout=subprocess.PIPE)
    process1.stdout.close()
    out, err = process2.communicate()
    return out.decode().lower()

def set_mkinitcpio_hooks_and_modules(self, hooks, modules):
    """ Set up mkinitcpio.conf """

    # TODO: Check if we can set this in run()
    install_path = libcalamares.globalstorage.value( "rootMountPoint" )
    with open("/etc/mkinitcpio.conf", "r") as mkinitcpio_file:
        mklins = [x.strip() for x in mkinitcpio_file.readlines()]

    for i in range(len(mklins)):
        if mklins[i].startswith("HOOKS"):
        mklins[i] = 'HOOKS="%s"' % ' '.join(hooks)
        elif mklins[i].startswith("MODULES"):
        mklins[i] = 'MODULES="%s"' % ' '.join(modules)

    path = os.path.join(install_path, "etc/mkinitcpio.conf")
    with open(path, "w") as mkinitcpio_file:
        mkinitcpio_file.write("\n".join(mklins) + "\n")

def run_mkinitcpio(self):
    """ Runs mkinitcpio """

    # TODO: Check if we can set this in run()
    install_path = libcalamares.globalstorage.value( "rootMountPoint" )
    # Add lvm and encrypt hooks if necessary

    cpu = get_cpu()

    hooks = ["base", "udev", "autodetect", "modconf", "block", "keyboard", "keymap"]
    modules = []

    # It is important that the plymouth hook comes before any encrypt hook

    plymouth_bin = os.path.join(install_path, "usr/bin/plymouth")
    if os.path.exists(plymouth_bin):
        hooks.append("plymouth")

    set_mkinitcpio_hooks_and_modules(hooks, modules)

    # Run mkinitcpio on the target system
    # TODO: set kernel and locale in a config
    # libcalamares.utils.chroot_call(['sh', '-c', 'LANG=%s /usr/bin/mkinitcpio -p %s' % (locale, kernel)])
    libcalamares.utils.chroot_call(['sh', '-c', 'LANG=en_US.uf8 /usr/bin/mkinitcpio -p linux314'])

def run():
    """ Run mkinitcpio """

    # Let's start without using hwdetect for mkinitcpio.conf.
    # I think it should work out of the box most of the time.
    # This way we don't have to fix deprecated hooks.
    # NOTE: With LUKS or LVM maybe we'll have to fix deprecated hooks.
    run_mkinitcpio()

    return None
