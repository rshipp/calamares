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

def set_autologin(desktop_manager, username, install_path):
    """ Enables automatic login for the installed desktop manager """

    if desktop_manager == 'mdm':
        # Systems with MDM as Desktop Manager
        mdm_conf_path = os.path.join(install_path, "etc/mdm/custom.conf")
        if os.path.exists(mdm_conf_path):
            with open(mdm_conf_path, "r") as mdm_conf:
                text = mdm_conf.readlines()
            with open(mdm_conf_path, "w") as mdm_conf:
                for line in text:
                    if '[daemon]' in line:
                        line = '[daemon]\nAutomaticLogin=%s\nAutomaticLoginEnable=True\n' % username
                    mdm_conf.write(line)
        else:
            with open(mdm_conf_path, "w") as mdm_conf:
                mdm_conf.write('# Calamares - Enable automatic login for user\n')
                mdm_conf.write('[daemon]\n')
                mdm_conf.write('AutomaticLogin=%s\n' % username)
                mdm_conf.write('AutomaticLoginEnable=True\n')
    elif desktop_manager == 'gdm':
        # Systems with GDM as Desktop Manager
        gdm_conf_path = os.path.join(install_path, "etc/gdm/custom.conf")
        if os.path.exists(gdm_conf_path):
            with open(gdm_conf_path, "r") as gdm_conf:
                text = gdm_conf.readlines()
            with open(gdm_conf_path, "w") as gdm_conf:
                for line in text:
                    if '[daemon]' in line:
                        line = '[daemon]\nAutomaticLogin=%s\nAutomaticLoginEnable=True\n' % username
                    gdm_conf.write(line)
        else:
            with open(gdm_conf_path, "w") as gdm_conf:
                gdm_conf.write('# Calamares - Enable automatic login for user\n')
                gdm_conf.write('[daemon]\n')
                gdm_conf.write('AutomaticLogin=%s\n' % username)
                gdm_conf.write('AutomaticLoginEnable=True\n')
    elif desktop_manager == 'kdm':
        # Systems with KDM as Desktop Manager
        kdm_conf_path = os.path.join(install_path, "usr/share/config/kdm/kdmrc")
        text = []
        with open(kdm_conf_path, "r") as kdm_conf:
            text = kdm_conf.readlines()
        with open(kdm_conf_path, "w") as kdm_conf:
            for line in text:
                if '#AutoLoginEnable=true' in line:
                    line = 'AutoLoginEnable=true\n'
                if 'AutoLoginUser=' in line:
                    line = 'AutoLoginUser=%s\n' % username
                kdm_conf.write(line)
    elif desktop_manager == 'lxdm':
        # Systems with LXDM as Desktop Manager
        lxdm_conf_path = os.path.join(install_path, "etc/lxdm/lxdm.conf")
        text = []
        with open(lxdm_conf_path, "r") as lxdm_conf:
            text = lxdm_conf.readlines()
        with open(lxdm_conf_path, "w") as lxdm_conf:
            for line in text:
                if '# autologin=dgod' in line:
                    line = 'autologin=%s\n' % username
                lxdm_conf.write(line)
    elif desktop_manager == 'lightdm':
        # Systems with LightDM as Desktop Manager
        # Ideally, we should use configparser for the ini conf file,
        # but we just do a simple text replacement for now, as it worksforme(tm)
        lightdm_conf_path = os.path.join(install_path, "etc/lightdm/lightdm.conf")
        text = []
        with open(lightdm_conf_path, "r") as lightdm_conf:
            text = lightdm_conf.readlines()
        with open(lightdm_conf_path, "w") as lightdm_conf:
            for line in text:
                if '#autologin-user=' in line:
                    line = 'autologin-user=%s\n' % username
                lightdm_conf.write(line)
    elif desktop_manager == 'slim':
        # Systems with Slim as Desktop Manager
        slim_conf_path = os.path.join(install_path, "etc/slim.conf")
        text = []
        with open(slim_conf_path, "r") as slim_conf:
            text = slim_conf.readlines()
        with open(slim_conf_path, "w") as slim_conf:
            for line in text:
                if 'auto_login' in line:
                   line = 'auto_login yes\n'
                if 'default_user' in line:
                   line = 'default_user %s\n' % username
                slim_conf.write(line)
    elif desktop_manager == 'sddm':
        # Systems with Sddm as Desktop Manager
        sddm_conf_path = os.path.join(install_path, "etc/sddm.conf")
        text = []
        with open(sddm_conf_path, "r") as sddm_conf:
            text = sddm_conf.readlines()
        with open(sddm_conf_path, "w") as sddm_conf:
            for line in text:
                if 'AutoUser=' in line:
                    line = 'AutoUser=%s\n' % username
                sddm_conf.write(line)

def run():
    """ Configure display managers """

    username = libcalamares.globalstorage.value( "autologinUser" )
    install_path = libcalamares.globalstorage.value( "rootMountPoint" )

    # Setup slim
    if os.path.exists("/usr/bin/slim"):
        desktop_manager = 'slim'

    # Setup sddm
    if os.path.exists("/usr/bin/sddm"):
        desktop_manager = 'sddm'

    # setup lightdm
    if os.path.exists("%s/usr/bin/lightdm" % install_path):
        libcalamares.utils.chroot_call(['mkdir', '-p', '/run/lightdm'])
        libcalamares.utils.chroot_call(['getent', 'group', 'lightdm'])
        libcalamares.utils.chroot_call(['groupadd', '-g', '620', 'lightdm'])
        libcalamares.utils.chroot_call(['getent', 'passwd', 'lightdm'])
        libcalamares.utils.chroot_call(['useradd', '-c', '"LightDM Display Manager"',
                                        '-u', '620', '-g', 'lightdm', '-d', '/var/run/lightdm',
                                        '-s', '/usr/bin/nologin', 'lightdm'])
        libcalamares.utils.chroot_call(['passwd', '-l', 'lightdm'])
        libcalamares.utils.chroot_call(['chown', '-R', 'lightdm:lightdm', '/run/lightdm'])
        if os.path.exists("%s/usr/bin/startxfce4" % install_path):
            os.system("sed -i -e 's/^.*user-session=.*/user-session=xfce/' %s/etc/lightdm/lightdm.conf" % install_path)
            os.system("ln -s /usr/lib/lightdm/lightdm/gdmflexiserver %s/usr/bin/gdmflexiserver" % install_path)
        os.system("chmod +r %s/etc/lightdm/lightdm.conf" % install_path)
        desktop_manager = 'lightdm'

    # Setup gdm
    if os.path.exists("%s/usr/bin/gdm" % install_path):
        libcalamares.utils.chroot_call(['getent', 'group', 'gdm'])
        libcalamares.utils.chroot_call(['groupadd', '-g', '120', 'gdm'])
        libcalamares.utils.chroot_call(['getent', 'passwd', 'gdm'])
        libcalamares.utils.chroot_call(['useradd', '-c', '"Gnome Display Manager"',
                                        '-u', '120', '-g', 'gdm', '-d', '/var/lib/gdm',
                                        '-s', '/usr/bin/nologin', 'gdm'])
        libcalamares.utils.chroot_call(['passwd', '-l', 'gdm'])
        libcalamares.utils.chroot_call(['chown', '-R', 'gdm:gdm', '/var/lib/gdm'])
        if os.path.exists("%s/var/lib/AccountsService/users" % install_path):
            os.system("echo \"[User]\" > %s/var/lib/AccountsService/users/gdm" % install_path)
        if os.path.exists("%s/usr/bin/startxfce4" % install_path):
            os.system("echo \"XSession=xfce\" >> %s/var/lib/AccountsService/users/gdm" % install_path)
        if os.path.exists("%s/usr/bin/cinnamon-session" % install_path):
            os.system("echo \"XSession=cinnamon-session\" >> %s/var/lib/AccountsService/users/gdm" % install_path)
        if os.path.exists("%s/usr/bin/mate-session" % install_path):
            os.system("echo \"XSession=mate\" >> %s/var/lib/AccountsService/users/gdm" % install_path)
        if os.path.exists("%s/usr/bin/enlightenment_start" % install_path):
            os.system("echo \"XSession=enlightenment\" >> %s/var/lib/AccountsService/users/gdm" % install_path)
        if os.path.exists("%s/usr/bin/openbox-session" % install_path):
            os.system("echo \"XSession=openbox\" >> %s/var/lib/AccountsService/users/gdm" % install_path)
        if os.path.exists("%s/usr/bin/lxsession" % install_path):
            os.system("echo \"XSession=LXDE\" >> %s/var/lib/AccountsService/users/gdm" % install_path)
        os.system("echo \"Icon=\" >> %s/var/lib/AccountsService/users/gdm" % install_path)
        desktop_manager = 'gdm'

    # Setup mdm
    if os.path.exists("%s/usr/bin/mdm" % install_path):
        libcalamares.utils.chroot_call(['getent', 'group', 'mdm'])
        libcalamares.utils.chroot_call(['groupadd', '-g', '128', 'mdm'])
        libcalamares.utils.chroot_call(['getent', 'passwd', 'mdm'])
        libcalamares.utils.chroot_call(['useradd', '-c', '"Linux Mint Display Manager"',
                                        '-u', '128', '-g', 'mdm', '-d', '/var/lib/mdm',
                                        '-s', '/usr/bin/nologin', 'mdm'])
        libcalamares.utils.chroot_call(['passwd', '-l', 'mdm'])
        libcalamares.utils.chroot_call(['chown', 'root:mdm', '/var/lib/mdm'])
        libcalamares.utils.chroot_call(['chmod', '1770', '/var/lib/mdm'])
        if os.path.exists("%s/usr/bin/startxfce4" % install_path):
            os.system("sed -i 's|default.desktop|xfce.desktop|g' %s/etc/mdm/custom.conf" % install_path)
        if os.path.exists("%s/usr/bin/cinnamon-session" % install_path):
            os.system("sed -i 's|default.desktop|cinnamon.desktop|g' %s/etc/mdm/custom.conf" % install_path)
        if os.path.exists("%s/usr/bin/openbox-session" % install_path):
            os.system("sed -i 's|default.desktop|openbox.desktop|g' %s/etc/mdm/custom.conf" % install_path)
        if os.path.exists("%s/usr/bin/mate-session" % install_path):
            os.system("sed -i 's|default.desktop|mate.desktop|g' %s/etc/mdm/custom.conf" % install_path)
        if os.path.exists("%s/usr/bin/lxsession" % install_path):
            os.system("sed -i 's|default.desktop|LXDE.desktop|g' %s/etc/mdm/custom.conf" % install_path)
        if os.path.exists("%s/usr/bin/enlightenment_start" % install_path):
            os.system("sed -i 's|default.desktop|enlightenment.desktop|g' %s/etc/mdm/custom.conf" % install_path)
        desktop_manager = 'mdm'

    # Setup lxdm
    if os.path.exists("%s/usr/bin/lxdm" % install_path):
        libcalamares.utils.chroot_call(['groupadd', '--system', 'lxdm'])
        if os.path.exists("%s/usr/bin/startxfce4" % install_path):
            os.system("sed -i -e 's|^.*session=.*|session=/usr/bin/startxfce4|' %s/etc/lxdm/lxdm.conf" % install_path)
        if os.path.exists("%s/usr/bin/cinnamon-session" % install_path):
            os.system("sed -i -e 's|^.*session=.*|session=/usr/bin/cinnamon-session|' %s/etc/lxdm/lxdm.conf" % install_path)
        if os.path.exists("%s/usr/bin/mate-session" % install_path):
            os.system("sed -i -e 's|^.*session=.*|session=/usr/bin/mate-session|' %s/etc/lxdm/lxdm.conf" % install_path)
        if os.path.exists("%s/usr/bin/enlightenment_start" % install_path):
            os.system("sed -i -e 's|^.*session=.*|session=/usr/bin/enlightenment_start|' %s/etc/lxdm/lxdm.conf" % install_path)
        if os.path.exists("%s/usr/bin/openbox-session" % install_path):
            os.system("sed -i -e 's|^.*session=.*|session=/usr/bin/openbox-session|' %s/etc/lxdm/lxdm.conf" % install_path)
        if os.path.exists("%s/usr/bin/lxsession" % install_path):
            os.system("sed -i -e 's|^.*session=.*|session=/usr/bin/lxsession|' %s/etc/lxdm/lxdm.conf" % install_path)
        os.system("chgrp -R lxdm %s/var/lib/lxdm" % install_path)
        os.system("chgrp lxdm %s/etc/lxdm/lxdm.conf" % install_path)
        os.system("chmod +r %s/etc/lxdm/lxdm.conf" % install_path)
        desktop_manager = 'lxdm'

    # Setup kdm
    if os.path.exists("%s/usr/bin/kdm" % install_path):
        libcalamares.utils.chroot_call(['getent', 'group', 'kdm'])
        libcalamares.utils.chroot_call(['groupadd', '-g', '135', 'kdm'])
        libcalamares.utils.chroot_call(['getent', 'passwd', 'kdm'])
        libcalamares.utils.chroot_call(['useradd', '-u', '135', '-g', 'kdm', '-d',
                                        '/var/lib/kdm', '-s', '/bin/false', '-r', '-M', 'kdm'])
        libcalamares.utils.chroot_call(['chown', '-R', '135:135', 'var/lib/kdm'])
        libcalamares.utils.chroot_call(['xdg-icon-resource', 'forceupdate', '--theme', 'hicolor'])
        libcalamares.utils.chroot_call(['update-desktop-database', '-q'])
        desktop_manager = 'kdm'

    if username != "None":
        libcalamares.utils.debug("Setting up autologin for user %s." % username)
        set_autologin(desktop_manager, username, install_path)

    return None
