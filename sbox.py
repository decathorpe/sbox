#!/usr/bin/python3

import os
import sys

import bwrap

HELP = """
Usage:
  {} command [args ...]
"""

if __name__ == "__main__":
    HELP = HELP.format(sys.argv[0])
else:
    HELP = HELP.format("sbox")

MOUNT_HOME = False
FRESH_XDG_RUNTIME_DIR = False


def main() -> int:
    if len(sys.argv) < 2:
        print(HELP)
        return 1

    wrapper = bwrap.BubbleWrapper()

    wrapper.add_bind_mount_readonly("/usr", "/usr")

    wrapper.create_symlink("usr/bin", "/bin")
    wrapper.create_symlink("usr/sbin", "/sbin")
    wrapper.create_symlink("usr/lib64", "/lib64")
    wrapper.create_symlink("usr/lib", "/lib")

    # wrapper.add_bind_mount_readonly("/etc/resolv.conf", "/etc/resolv.conf")
    # wrapper.add_bind_mount_readonly("/etc/passwd", "/etc/passwd")
    # wrapper.add_bind_mount_readonly("/etc/group", "/etc/group")
    wrapper.add_bind_mount_readonly("/etc/fonts", "/etc/fonts")

    if MOUNT_HOME:
        wrapper.add_bind_mount(os.getenv("HOME"), os.getenv("HOME"))
    else:
        wrapper.create_directory(os.getenv("HOME"))

    wrapper.set_dev("/dev")
    wrapper.set_proc("/proc")
    wrapper.add_tmpfs("/tmp")

    wrapper.add_unshare("all")
    # wrapper.share_net()

    if FRESH_XDG_RUNTIME_DIR:
        dir_xdg_runtime = "/run/user/" + str(os.getuid())
        wrapper.create_directory(dir_xdg_runtime)
        wrapper.set_env("XDG_RUNTIME_DIR", dir_xdg_runtime)
    else:
        wrapper.add_bind_mount(os.getenv("XDG_RUNTIME_DIR"), os.getenv("XDG_RUNTIME_DIR"))

    return wrapper.exec(sys.argv[1], sys.argv[2:])


if __name__ == "__main__":
    sys.exit(main())
