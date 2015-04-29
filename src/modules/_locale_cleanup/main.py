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
import subprocess

import libcalamares
from .. import pacman_utils


def run():
    """ Package removal module. Cleanup the language packs """

    install_path = libcalamares.globalstorage.value("rootMountPoint")

    # remove any db.lck
    pacman_utils._nuke_pacman_db(install_path)

    ###################################################################################
    # Prepare locale string
    # Normal:
    #   lcLocale = it_CH.UTF8 UTF-8 -> it
    # Special cases:
    #   lcLocale = zh_TW.UTF8 UTF-8 -> zh_TW and zh_CN both installed because
    #                                  we search zh only
    ###################################################################################

    print("Calamares locale: " % libcalamares.globalstorage.value("lcLocale"))
    this_locale = libcalamares.globalstorage.value("lcLocale")[:2]
    print("Final locale: " % this_locale)

    ###################################################################################
    # Remove KDE l10n
    ###################################################################################
    remove_locales("kde-l10n", this_locale)

    ###################################################################################
    # Remove Calligra l10n
    ###################################################################################
    remove_locales("calligra-l10n", this_locale)

    print('locale_cleanup completed')


def remove_locales(basepkgname, keep_locale):
    # Search installed kde locale packages
    list_of_pkgs = []

    cmd = ["pacman -Q | grep -i", str(basepkgname), "| awk '{print $1}'"]

    p = subprocess.Popen(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    list_of_pkgs = p.communicate()
    list_of_pkgs = {"code": p.returncode, "stdout": list_of_pkgs[0],
        "stderr": list_of_pkgs[1].rstrip('\n')}

    print(list_of_pkgs)

    # Remove the pkgs that do not have the locale 'keep_locale'
    # ex: kde-l10n-it 15.04.0-2
    for pkg in list_of_pkgs:
        if pkg[pkg.find(basepkgname + "-")+len(basepkgname + "-"):pkg.rfind(' ')] not in keep_locale:
            print('Removing %s package' % pkg)
            libcalamares.utils.chroot_call(
                ['pacman', '-Rddn', '--noconfirm', '%s' % (pkg)])
