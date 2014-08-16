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

import shutil

def run():
    """ Misc postinstall configurations """

    install_path = libcalamares.globalstorage.value( "rootMountPoint" )

    # Add hostname
    # TODO: get hostname

    hostname = 'manjaro'
    hostname_path = os.path.join(install_path, "etc/hostname")
    with open(hostname_path, "w") as hostname_file:
        hostname_file.write(hostname)

    # Add BROWSER var
    os.system("echo \"BROWSER=/usr/bin/xdg-open\" >> %s/etc/environment" % install_path)
    os.system("echo \"BROWSER=/usr/bin/xdg-open\" >> %s/etc/skel/.bashrc" % install_path)
    os.system("echo \"BROWSER=/usr/bin/xdg-open\" >> %s/etc/profile" % install_path)
    # Add TERM var
    if os.path.exists("%s/usr/bin/mate-session" % install_path):
        os.system("echo \"TERM=mate-terminal\" >> %s/etc/environment" % install_path)
        os.system("echo \"TERM=mate-terminal\" >> %s/etc/profile" % install_path)

    # Fix_gnome_apps
    libcalamares.utils.chroot_call(['glib-compile-schemas', '/usr/share/glib-2.0/schemas'])
    libcalamares.utils.chroot_call(['gtk-update-icon-cache', '-q', '-t', '-f', '/usr/share/icons/hicolor'])
    libcalamares.utils.chroot_call(['dconf', 'update'])

    if os.path.exists("%s/usr/bin/gnome-keyring-daemon" % install_path):
        libcalamares.utils.chroot_call(['setcap', 'cap_ipc_lock=ep', '/usr/bin/gnome-keyring-daemon'])

    # Fix_ping_installation
    libcalamares.utils.chroot_call(['setcap', 'cap_net_raw=ep', '/usr/bin/ping'])
    libcalamares.utils.chroot_call(['setcap', 'cap_net_raw=ep', '/usr/bin/ping6'])

    # Remove calamares
    if os.path.exists("%s/usr/bin/calamares" % install_path):
        libcalamares.utils.chroot_call(['pacman', '-R', '--noconfirm', 'calamares'])

    # Setup pacman
    queue_event("action", _("Configuring package manager"))
    queue_event("pulse")

    # Copy mirror list
    shutil.copy2('/etc/pacman.d/mirrorlist',
             os.path.join(install_path, 'etc/pacman.d/mirrorlist'))

    # Copy random generated keys by pacman-init to target
    if os.path.exists("%s/etc/pacman.d/gnupg" % install_path):
        os.system("rm -rf %s/etc/pacman.d/gnupg" % install_path)
    os.system("cp -a /etc/pacman.d/gnupg %s/etc/pacman.d/" % install_path)
    libcalamares.utils.chroot_call(['pacman-key', '--populate', 'archlinux', 'manjaro'])

    return None
