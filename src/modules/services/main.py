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

import libcalamares

def enable_services(self, services):
    """ Enables all services that are in the list 'services' """

    for name in services:
        libcalamares.utils.chroot_call(['systemctl', 'enable', name + ".service"])

def run():
    """ Setup systemd services """
    install_path = libcalamares.globalstorage.value( "rootMountPoint" )

    # enable services
    enable_services([network_manager, 'remote-fs.target'])

    cups_service = os.path.join(install_path, "usr/lib/systemd/system/cups.service")
    if os.path.exists(cups_service):
        enable_services(['cups'])

    return None
