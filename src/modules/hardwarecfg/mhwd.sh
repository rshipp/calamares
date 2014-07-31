#!/bin/sh
kernel_cmdline ()
{
    for param in $(/bin/cat /proc/cmdline); do
        case "${param}" in
            $1=*) echo "${param##*=}"; return 0 ;;
            $1) return 0 ;;
            *) continue ;;
        esac
    done
    [ -n "${2}" ] && echo "${2}"
    return 1
}

# chroot_mount()
# prepares target system as a chroot
#
chroot_mount()
{
    [[ -e "${DESTDIR}/sys" ]] || mkdir -m 555 "${DESTDIR}/sys"
    [[ -e "${DESTDIR}/proc" ]] || mkdir -m 555 "${DESTDIR}/proc"
    [[ -e "${DESTDIR}/dev" ]] || mkdir "${DESTDIR}/dev"
    mount -t sysfs sysfs "${DESTDIR}/sys"
    mount -t proc proc "${DESTDIR}/proc"
    mount -o bind /dev "${DESTDIR}/dev"
    chmod 555 "${DESTDIR}/sys"
    chmod 555 "${DESTDIR}/proc"
}

# chroot_umount()
# tears down chroot in target system
#
chroot_umount()
{
    umount "${DESTDIR}/proc"
    umount "${DESTDIR}/sys"
    umount "${DESTDIR}/dev"
}

USENONFREE="$(kernel_cmdline nonfree no)"
VIDEO="$(kernel_cmdline xdriver no)"
DESTDIR="/install"

echo "MHWD-Driver: ${USENONFREE}"
echo "MHWD-Video: ${VIDEO}"

chroot_mount

mkdir -p ${DESTDIR}/opt/livecd
mount -o bind /opt/livecd ${DESTDIR}/opt/livecd > /tmp/mount.pkgs.log
ls ${DESTDIR}/opt/livecd >> /tmp/mount.pkgs.log

# Video driver
if  [ "${USENONFREE}" == "yes" ] || [ "${USENONFREE}" == "true" ]; then
	if  [ "${VIDEO}" == "vesa" ]; then
		chroot ${DESTDIR} mhwd --install pci video-vesa --pmconfig "/opt/livecd/pacman-gfx.conf" 
	else
		chroot ${DESTDIR} mhwd --auto pci nonfree 0300 --pmconfig "/opt/livecd/pacman-gfx.conf" 
	fi
else
	if  [ "${VIDEO}" == "vesa" ]; then
		chroot ${DESTDIR} mhwd --install pci video-vesa --pmconfig "/opt/livecd/pacman-gfx.conf" 
	else
		chroot ${DESTDIR} mhwd --auto pci free 0300 --pmconfig "/opt/livecd/pacman-gfx.conf" 
	fi
fi

# Network driver
mhwd --auto pci free 0200 --pmconfig "/opt/livecd/pacman-gfx.conf"
mhwd --auto pci free 0280 --pmconfig "/opt/livecd/pacman-gfx.conf"

umount ${DESTDIR}/opt/livecd
rmdir ${DESTDIR}/opt/livecd

chroot_umount
