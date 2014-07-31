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

def run():
    """ Configure the hardware """

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
        mhwd_script_path = '/usr/lib/calamares/modules/hardwarecfg/mhwd.sh'
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

    # Remove virtualbox driver on real hardware
    p1 = subprocess.Popen(["mhwd"], stdout=subprocess.PIPE)
    p2 = subprocess.Popen(["grep", "0300:80ee:beef"], stdin=p1.stdout, stdout=subprocess.PIPE)
    num_res = p2.communicate()[0]
    if num_res == "0":
        chroot_call(root_mount_point, ['sh', '-c', 'pacman -Rsc --noconfirm $(pacman -Qq | grep virtualbox-guest-modules)'])

    # Set unique machine-id
    chroot_call(root_mount_point, ['dbus-uuidgen', '--ensure=/etc/machine-id'])
    chroot_call(root_mount_point, ['dbus-uuidgen', '--ensure=/var/lib/dbus/machine-id'])

    return None
