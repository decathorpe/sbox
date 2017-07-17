"""
python program to execute other programs in a confined environment (bwrap)
"""

# python program to execute other programs in a confined environment (bwrap)
# Copyright (C) 2017  Fabio Valentini
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import sys

from bwrapper.bwrap import BubbleWrapper

import sbox.profile_parser as pp

HELP_TEXT = """
Usage:
  {} command [args ...]
""".format("sbox")


def main() -> int:
    if len(sys.argv) < 2:
        print(HELP_TEXT)
        return 1

    profile_name = sys.argv[1]

    if not os.path.exists("profiles/" + profile_name + ".json"):
        print("No profile found for this application. Using default settings.")
        options = pp.collect_options("profiles/system.json")
    else:
        options = pp.collect_options("profiles/system.json", "profiles/" + profile_name + ".json")

    wrapper = BubbleWrapper()

    # mount /usr and create expected directory symlinks
    if options["mount-usr"]:
        wrapper.filesystem.add_bind_mount_ro("/usr", "/usr")
        wrapper.filesystem.create_symlink("usr/bin", "/bin")
        wrapper.filesystem.create_symlink("usr/sbin", "/sbin")
        wrapper.filesystem.create_symlink("usr/lib", "/lib")
        wrapper.filesystem.create_symlink("usr/lib64", "/lib64")

    # mount /dev
    if options["mount-dev"]:
        wrapper.filesystem.add_devtmpfs("/dev")

    # mount /proc
    if options["mount-proc"]:
        wrapper.filesystem.add_proc("/proc")

    # mount /tmp
    if options["mount-tmp"]:
        wrapper.filesystem.add_tmpfs("/tmp")

    # mount or create an empty $HOME
    if options["mount-home"] == "ro":
        wrapper.filesystem.add_bind_mount_ro(os.getenv("HOME"), os.getenv("HOME"))
    elif options["mount-home"] == "rw":
        wrapper.filesystem.add_bind_mount_rw(os.getenv("HOME"), os.getenv("HOME"))
    else:
        wrapper.filesystem.create_directory(os.getenv("HOME"))

    # mount XDG_RUNTIME_DIR:
    if options["mount-runtime_dir"]:
        if "XDG_RUNTIME_DIR" in os.environ:
            wrapper.filesystem.add_bind_mount_rw(os.getenv("XDG_RUNTIME_DIR"),
                                                 os.getenv("XDG_RUNTIME_DIR"))
    else:
        dir_xdg_runtime = "/run/user/" + str(os.getuid())
        wrapper.filesystem.create_directory(dir_xdg_runtime)
        wrapper.environment.set_env("XDG_RUNTIME_DIR", dir_xdg_runtime)

    # create specified directories
    for directory in options["directories"]:
        wrapper.filesystem.create_directory(directory)

    # create specified symlinks
    for symlink in options["symlinks"]:
        wrapper.filesystem.create_symlink(options["symlinks"][symlink], symlink)

    # mount requested read-only locations
    for mount_ro in options["mounts-ro"]:
        wrapper.filesystem.add_bind_mount_ro(options["mounts-ro"][mount_ro], mount_ro)

    # mount requested read-write locations
    for mount_rw in options["mounts-rw"]:
        wrapper.filesystem.add_bind_mount_ro(options["mounts-ro"][mount_rw], mount_rw)

    # unshare namespaces as specified
    for confine in options["confine"]:
        wrapper.environment.add_unshare(confine)

    # enable networking
    if options["network"]:
        if "all" in options["confine"]:
            wrapper.environment.add_share_net()

        wrapper.filesystem.add_bind_mount_ro("/etc/resolv.conf", "/etc/resolv.conf")

    if "binary" in options:
        comm = options["binary"]
    else:
        comm = sys.argv[1]

    args = sys.argv[2:]

    return wrapper.exec(comm, args)
