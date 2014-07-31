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

def chroot_call(root_mount_point, cmd):
    subprocess.check_call(["chroot", root_mount_point] + cmd)

def uncomment_locale_gen(self, locale):
    """ Uncomment selected locale in /etc/locale.gen """

    text = []
    with open("%s/etc/locale.gen" % install_path, "r") as gen:
        text = gen.readlines()

    with open("%s/etc/locale.gen" % install_path, "w") as gen:
        for line in text:
        if locale in line and line[0] == "#":
            # uncomment line
            line = line[1:]
        gen.write(line)

def run():
    """ Setup locale """

    # Generate locales
    # TODO: get variables
    keyboard_layout = 'en'
    keyboard_variant = ''
    locale = 'en_US.utf8'

    uncomment_locale_gen(locale)

    chroot_call(root_mount_point, ['locale-gen'])
    locale_conf_path = os.path.join(install_path, "etc/locale.conf")
    with open(locale_conf_path, "w") as locale_conf:
        locale_conf.write('LANG=%s\n' % locale)

    environment_path = os.path.join(install_path, "etc/environment")
    with open(environment_path, "w") as environment:
        environment.write('LANG=%s\n' % locale)

    # Set /etc/vconsole.conf
    vconsole_conf_path = os.path.join(install_path, "etc/vconsole.conf")
    with open(vconsole_conf_path, "w") as vconsole_conf:
        vconsole_conf.write('KEYMAP=%s\n' % keyboard_layout)

    return None
