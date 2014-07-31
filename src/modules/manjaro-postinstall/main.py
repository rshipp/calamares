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

import shutil

def chroot_call(root_mount_point, cmd):
    subprocess.check_call(["chroot", root_mount_point] + cmd)

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
    # chroot_call(root_mount_point, ['sh', '-c', 'LANG=%s /usr/bin/mkinitcpio -p %s' % (locale, kernel)])
    chroot_call(root_mount_point, ['sh', '-c', 'LANG=en_US.uf8 /usr/bin/mkinitcpio -p linux314'])

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

def set_autologin(self):
    """ Enables automatic login for the installed desktop manager """
    # TODO: get username
    username = 'john'

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
            mdm_conf.write('# Thus - Enable automatic login for user\n')
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
            gdm_conf.write('# Thus - Enable automatic login for user\n')
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

def copy_network_config(self):
    """ Copies Network Manager configuration """
    source_nm = "/etc/NetworkManager/system-connections/"
    target_nm = "%s/etc/NetworkManager/system-connections/" % install_path

    # Sanity checks.  We don't want to do anything if a network
    # configuration already exists on the target
    if os.path.exists(source_nm) and os.path.exists(target_nm):
        for network in os.listdir(source_nm):
        # Skip LTSP live
        if network == "LTSP":
            continue

        source_network = os.path.join(source_nm, network)
        target_network = os.path.join(target_nm, network)

        if os.path.exists(target_network):
            continue

        try:
            shutil.copy(source_network, target_network)
        except FileNotFoundError:
            # TODO: print some warning here
            # Can't copy network configuration files
        except FileExistsError:
            pass

def enable_services(self, services):
    """ Enables all services that are in the list 'services' """
    for name in services:
        chroot_call(root_mount_point, ['systemctl', 'enable', name + ".service"])

def change_user_password(self, user, new_password):
    """ Changes the user's password """
    try:
        shadow_password = crypt.crypt(new_password, "$6$%s$" % user)
    except:
        return False

    try:
        self.chroot_call(root_mount_point, ['usermod', '-p', shadow_password, user])
    except:
        return False

    return True

def auto_timesetting(self):
    """ Set hardware clock """
    subprocess.check_call(["hwclock", "--systohc", "--utc"])
    shutil.copy2("/etc/adjtime", "%s/etc/" % self.install_path)


def run():
    """ Final install steps
        Set clock, language, timezone
        Run mkinitcpio
        Populate pacman keyring
        Setup systemd services
        ... and more """

    # TODO: configure fstab (see thus code)

    # TODO: get network manager
    network_manager = 'NetworkManager'

    # Copy configured networks in Live medium to target system
    if network_manager == 'NetworkManager':
        copy_network_config()

    # enable services
    enable_services([network_manager, 'remote-fs.target'])

    cups_service = os.path.join(install_path, "usr/lib/systemd/system/cups.service")
    if os.path.exists(cups_service):
        enable_services(['cups'])

    # TODO: set timezone

    # Set user parameters
    # TODO: get variables
    username = 'john'
    fullname = 'John Doe'
    password = 'pwd'
    root_password = 'pwd'
    hostname = 'manjaro'

    sudoers_path = os.path.join(install_path, "etc/sudoers.d/10-installer")

    with open(sudoers_path, "w") as sudoers:
        sudoers.write('%s ALL=(ALL) ALL\n' % username)

    subprocess.check_call(["chmod", "440", sudoers_path])

    default_groups = 'lp,video,network,storage,wheel,audio'

    if settings.get('require_password') is False:
        chroot_call(root_mount_point, ['groupadd', 'autologin'])
        default_groups += ',autologin'

    chroot_call(root_mount_point, ['useradd', '-m', '-s', '/bin/bash', '-g', 'users', '-G', default_groups, username])

    change_user_password(username, password)

    chroot_call(root_mount_point, ['chfn', '-f', fullname, username])

    chroot_call(root_mount_point, ['chown', '-R', '%s:users' % username, "/home/%s" % username])

    hostname_path = os.path.join(install_path, "etc/hostname")
    with open(hostname_path, "w") as hostname_file:
        hostname_file.write(hostname)

    # Set root password
    if not root_password is '':
        change_user_password('root', root_password)
    else:
        change_user_password('root', password)

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

    auto_timesetting()

    # Install configs for root
    chroot_call(root_mount_point, ['cp', '-av', '/etc/skel/.', '/root/'])

    queue_event('info', _("Configuring hardware ..."))
    # Copy generated xorg.xonf to target
    if os.path.exists("/etc/X11/xorg.conf"):
        shutil.copy2('/etc/X11/xorg.conf',
             os.path.join(install_path, 'etc/X11/xorg.conf'))

    # TODO: Maybe we can drop this
    # Configure ALSA
    chroot_call(root_mount_point, ['sh', '-c', 'amixer -c 0 sset Master 70% unmute'])
    chroot_call(root_mount_point, ['sh', '-c', 'amixer -c 0 sset Front 70% unmute'])
    chroot_call(root_mount_point, ['sh', '-c', 'amixer -c 0 sset Side 70% unmute'])
    chroot_call(root_mount_point, ['sh', '-c', 'amixer -c 0 sset Surround 70% unmute'])
    chroot_call(root_mount_point, ['sh', '-c', 'amixer -c 0 sset Center 70% unmute'])
    chroot_call(root_mount_point, ['sh', '-c', 'amixer -c 0 sset LFE 70% unmute'])
    chroot_call(root_mount_point, ['sh', '-c', 'amixer -c 0 sset Headphone 70% unmute'])
    chroot_call(root_mount_point, ['sh', '-c', 'amixer -c 0 sset Speaker 70% unmute'])
    chroot_call(root_mount_point, ['sh', '-c', 'amixer -c 0 sset PCM 70% unmute'])
    chroot_call(root_mount_point, ['sh', '-c', 'amixer -c 0 sset Line 70% unmute'])
    chroot_call(root_mount_point, ['sh', '-c', 'amixer -c 0 sset External 70% unmute'])
    chroot_call(root_mount_point, ['sh', '-c', 'amixer -c 0 sset FM 50% unmute'])
    chroot_call(root_mount_point, ['sh', '-c', 'amixer -c 0 sset Master Mono 70% unmute'])
    chroot_call(root_mount_point, ['sh', '-c', 'amixer -c 0 sset Master Digital 70% unmute'])
    chroot_call(root_mount_point, ['sh', '-c', 'amixer -c 0 sset Analog Mix 70% unmute'])
    chroot_call(root_mount_point, ['sh', '-c', 'amixer -c 0 sset Aux 70% unmute'])
    chroot_call(root_mount_point, ['sh', '-c', 'amixer -c 0 sset Aux2 70% unmute'])
    chroot_call(root_mount_point, ['sh', '-c', 'amixer -c 0 sset PCM Center 70% unmute'])
    chroot_call(root_mount_point, ['sh', '-c', 'amixer -c 0 sset PCM Front 70% unmute'])
    chroot_call(root_mount_point, ['sh', '-c', 'amixer -c 0 sset PCM LFE 70% unmute'])
    chroot_call(root_mount_point, ['sh', '-c', 'amixer -c 0 sset PCM Side 70% unmute'])
    chroot_call(root_mount_point, ['sh', '-c', 'amixer -c 0 sset PCM Surround 70% unmute'])
    chroot_call(root_mount_point, ['sh', '-c', 'amixer -c 0 sset Playback 70% unmute'])
    chroot_call(root_mount_point, ['sh', '-c', 'amixer -c 0 sset PCM,1 70% unmute'])
    chroot_call(root_mount_point, ['sh', '-c', 'amixer -c 0 sset DAC 70% unmute'])
    chroot_call(root_mount_point, ['sh', '-c', 'amixer -c 0 sset DAC,0 70% unmute'])
    chroot_call(root_mount_point, ['sh', '-c', 'amixer -c 0 sset DAC,1 70% unmute'])
    chroot_call(root_mount_point, ['sh', '-c', 'amixer -c 0 sset Synth 70% unmute'])
    chroot_call(root_mount_point, ['sh', '-c', 'amixer -c 0 sset CD 70% unmute'])
    chroot_call(root_mount_point, ['sh', '-c', 'amixer -c 0 sset Wave 70% unmute'])
    chroot_call(root_mount_point, ['sh', '-c', 'amixer -c 0 sset Music 70% unmute'])
    chroot_call(root_mount_point, ['sh', '-c', 'amixer -c 0 sset AC97 70% unmute'])
    chroot_call(root_mount_point, ['sh', '-c', 'amixer -c 0 sset Analog Front 70% unmute'])
    chroot_call(root_mount_point, ['sh', '-c', 'amixer -c 0 sset VIA DXS,0 70% unmute'])
    chroot_call(root_mount_point, ['sh', '-c', 'amixer -c 0 sset VIA DXS,1 70% unmute'])
    chroot_call(root_mount_point, ['sh', '-c', 'amixer -c 0 sset VIA DXS,2 70% unmute'])
    chroot_call(root_mount_point, ['sh', '-c', 'amixer -c 0 sset VIA DXS,3 70% unmute'])

    # set input levels
    chroot_call(root_mount_point, ['sh', '-c', 'amixer -c 0 sset Mic 70% mute'])
    chroot_call(root_mount_point, ['sh', '-c', 'amixer -c 0 sset IEC958 70% mute'])

    # special stuff
    chroot_call(root_mount_point, ['sh', '-c', 'amixer -c 0 sset Master Playback Switch on'])
    chroot_call(root_mount_point, ['sh', '-c', 'amixer -c 0 sset Master Surround on'])
    chroot_call(root_mount_point, ['sh', '-c', 'amixer -c 0 sset SB Live Analog/Digital Output Jack off'])
    chroot_call(root_mount_point, ['sh', '-c', 'amixer -c 0 sset Audigy Analog/Digital Output Jack off'])

    # special stuff
    chroot_call(root_mount_point, ['sh', '-c', 'amixer -c 0 sset Master Playback Switch on'])
    chroot_call(root_mount_point, ['sh', '-c', 'amixer -c 0 sset Master Surround on'])
    chroot_call(root_mount_point, ['sh', '-c', 'amixer -c 0 sset SB Live Analog/Digital Output Jack off'])
    chroot_call(root_mount_point, ['sh', '-c', 'amixer -c 0 sset Audigy Analog/Digital Output Jack off'])

    # Set pulse
    if os.path.exists("/usr/bin/pulseaudio-ctl"):
        chroot_call(root_mount_point, ['pulseaudio-ctl', 'normal'])

    # Save settings
    chroot_call(root_mount_point, ['alsactl', '-f', '/etc/asound.state', 'store'])

    # Install xf86-video driver
    if os.path.exists("/opt/livecd/pacman-gfx.conf"):
        # TODO: get mhwd-script path or port it to python
        mhwd_script_path = '/usr/lib/calamares/modules/manjaro-postinstall/mhwd.sh'
        try:
        subprocess.check_call(["/usr/bin/bash", mhwd_script_path])
        except subprocess.FileNotFoundError as e:
        txt = _("Can't execute the MHWD script")
        # TODO: produce fatal error here
        return False
        except subprocess.CalledProcessError as e:
        txt = "CalledProcessError.output = %s" % e.output
        # TODO: produce fatal error here
        return False

    # Setup slim
    if os.path.exists("/usr/bin/slim"):
        desktop_manager = 'slim'

    # Setup sddm
    if os.path.exists("/usr/bin/sddm"):
        desktop_manager = 'sddm'

    # setup lightdm
    if os.path.exists("%s/usr/bin/lightdm" % install_path):
        chroot_call(root_mount_point, ['mkdir', '-p', '/run/lightdm'])
        chroot_call(root_mount_point, ['getent', 'group', 'lightdm'])
        chroot_call(root_mount_point, ['groupadd', '-g', '620', 'lightdm'])
        chroot_call(root_mount_point, ['getent', 'passwd', 'lightdm'])
        chroot_call(root_mount_point, ['useradd', '-c', '"LightDM Display Manager"',
             '-u', '620', '-g', 'lightdm', '-d', '/var/run/lightdm',
             '-s', '/usr/bin/nologin', 'lightdm'])
        chroot_call(root_mount_point, ['passwd', '-l', 'lightdm'])
        chroot_call(root_mount_point, ['chown', '-R', 'lightdm:lightdm', '/run/lightdm'])
        if os.path.exists("%s/usr/bin/startxfce4" % install_path):
        os.system("sed -i -e 's/^.*user-session=.*/user-session=xfce/' %s/etc/lightdm/lightdm.conf" % install_path)
        os.system("ln -s /usr/lib/lightdm/lightdm/gdmflexiserver %s/usr/bin/gdmflexiserver" % install_path)
        os.system("chmod +r %s/etc/lightdm/lightdm.conf" % install_path)
        desktop_manager = 'lightdm'

    # Setup gdm
    if os.path.exists("%s/usr/bin/gdm" % install_path):
        chroot_call(root_mount_point, ['getent', 'group', 'gdm'])
        chroot_call(root_mount_point, ['groupadd', '-g', '120', 'gdm'])
        chroot_call(root_mount_point, ['getent', 'passwd', 'gdm'])
        chroot_call(root_mount_point, ['useradd', '-c', '"Gnome Display Manager"',
             '-u', '120', '-g', 'gdm', '-d', '/var/lib/gdm',
             '-s', '/usr/bin/nologin', 'gdm'])
        chroot_call(root_mount_point, ['passwd', '-l', 'gdm'])
        chroot_call(root_mount_point, ['chown', '-R', 'gdm:gdm', '/var/lib/gdm'])
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
        chroot_call(root_mount_point, ['getent', 'group', 'mdm'])
        chroot_call(root_mount_point, ['groupadd', '-g', '128', 'mdm'])
        chroot_call(root_mount_point, ['getent', 'passwd', 'mdm'])
        chroot_call(root_mount_point, ['useradd', '-c', '"Linux Mint Display Manager"',
             '-u', '128', '-g', 'mdm', '-d', '/var/lib/mdm',
             '-s', '/usr/bin/nologin', 'mdm'])
        chroot_call(root_mount_point, ['passwd', '-l', 'mdm'])
        chroot_call(root_mount_point, ['chown', 'root:mdm', '/var/lib/mdm'])
        chroot_call(root_mount_point, ['chmod', '1770', '/var/lib/mdm'])
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
        chroot_call(root_mount_point, ['groupadd', '--system', 'lxdm'])
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
        chroot_call(root_mount_point, ['getent', 'group', 'kdm'])
        chroot_call(root_mount_point, ['groupadd', '-g', '135', 'kdm'])
        chroot_call(root_mount_point, ['getent', 'passwd', 'kdm'])
        chroot_call(root_mount_point, ['useradd', '-u', '135', '-g', 'kdm', '-d',
             '/var/lib/kdm', '-s', '/bin/false', '-r', '-M', 'kdm'])
        chroot_call(root_mount_point, ['chown', '-R', '135:135', 'var/lib/kdm'])
        chroot_call(root_mount_point, ['xdg-icon-resource', 'forceupdate', '--theme', 'hicolor'])
        chroot_call(root_mount_point, ['update-desktop-database', '-q'])
        desktop_manager = 'kdm'

    # Add BROWSER var
    os.system("echo \"BROWSER=/usr/bin/xdg-open\" >> %s/etc/environment" % install_path)
    os.system("echo \"BROWSER=/usr/bin/xdg-open\" >> %s/etc/skel/.bashrc" % install_path)
    os.system("echo \"BROWSER=/usr/bin/xdg-open\" >> %s/etc/profile" % install_path)
    # Add TERM var
    if os.path.exists("%s/usr/bin/mate-session" % install_path):
        os.system("echo \"TERM=mate-terminal\" >> %s/etc/environment" % install_path)
        os.system("echo \"TERM=mate-terminal\" >> %s/etc/profile" % install_path)

    # Fix_gnome_apps
    chroot_call(root_mount_point, ['glib-compile-schemas', '/usr/share/glib-2.0/schemas'])
    chroot_call(root_mount_point, ['gtk-update-icon-cache', '-q', '-t', '-f', '/usr/share/icons/hicolor'])
    chroot_call(root_mount_point, ['dconf', 'update'])

    if os.path.exists("%s/usr/bin/gnome-keyring-daemon" % install_path):
        chroot_call(root_mount_point, ['setcap', 'cap_ipc_lock=ep', '/usr/bin/gnome-keyring-daemon'])

    # Fix_ping_installation
    chroot_call(root_mount_point, ['setcap', 'cap_net_raw=ep', '/usr/bin/ping'])
    chroot_call(root_mount_point, ['setcap', 'cap_net_raw=ep', '/usr/bin/ping6'])

    # Remove thus
    if os.path.exists("%s/usr/bin/thus" % install_path):
        queue_event('info', _("Removing live configuration (packages)"))
        chroot_call(root_mount_point, ['pacman', '-R', '--noconfirm', 'thus'])

    # Remove virtualbox driver on real hardware
    p1 = subprocess.Popen(["mhwd"], stdout=subprocess.PIPE)
    p2 = subprocess.Popen(["grep", "0300:80ee:beef"], stdin=p1.stdout, stdout=subprocess.PIPE)
    num_res = p2.communicate()[0]
    if num_res == "0":
        chroot_call(root_mount_point, ['sh', '-c', 'pacman -Rsc --noconfirm $(pacman -Qq | grep virtualbox-guest-modules)'])

    # Set unique machine-id
    chroot_call(root_mount_point, ['dbus-uuidgen', '--ensure=/etc/machine-id'])
    chroot_call(root_mount_point, ['dbus-uuidgen', '--ensure=/var/lib/dbus/machine-id'])


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
    chroot_call(root_mount_point, ['pacman-key', '--populate', 'archlinux', 'manjaro'])
    queue_event('info', _("Finished configuring package manager."))

    consolefh = open("%s/etc/keyboard.conf" % install_path, "r")
    newconsolefh = open("%s/etc/keyboard.new" % install_path, "w")
    for line in consolefh:
        line = line.rstrip("\r\n")
        if(line.startswith("XKBLAYOUT=")):
        newconsolefh.write("XKBLAYOUT=\"%s\"\n" % keyboard_layout)
        elif(line.startswith("XKBVARIANT=") and keyboard_variant != ''):
        newconsolefh.write("XKBVARIANT=\"%s\"\n" % keyboard_variant)
        else:
        newconsolefh.write("%s\n" % line)
    consolefh.close()
    newconsolefh.close()
    chroot_call(root_mount_point, ['mv', '/etc/keyboard.conf', '/etc/keyboard.conf.old'])
    chroot_call(root_mount_point, ['mv', '/etc/keyboard.new', '/etc/keyboard.conf'])

    # Let's start without using hwdetect for mkinitcpio.conf.
    # I think it should work out of the box most of the time.
    # This way we don't have to fix deprecated hooks.
    # NOTE: With LUKS or LVM maybe we'll have to fix deprecated hooks.
    run_mkinitcpio()

    # Set autologin if selected
    # Warning: In openbox "desktop", the post-install script writes /etc/slim.conf
    # so we always have to call set_autologin AFTER the post-install script call.
    if settings.get('require_password') is False:
        set_autologin()

    return None
