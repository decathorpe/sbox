#!/usr/bin/python3

import os
import subprocess
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

MOUNT_HOME = True
FRESH_XDG_RUNTIME_DIR = False


def main() -> int:
    cmd = list()

    if len(sys.argv) < 2:
        print(HELP)
        return 1

    prog = sys.argv[1]

    cmd.append("bwrap")

    # bind-mount /usr
    cmd.append("--ro-bind")
    cmd.append("/usr")
    cmd.append("/usr")

    # bind-mount $HOME
    if MOUNT_HOME:
        cmd.append("--bind")
        cmd.append(os.getenv("HOME"))
        cmd.append(os.getenv("HOME"))

    # symlink /usr/lib64 <- /lib64
    cmd.append("--symlink")
    cmd.append("usr/lib64")
    cmd.append("/lib64")

    # symlink /usr/lib <- /lib
    cmd.append("--symlink")
    cmd.append("usr/lib")
    cmd.append("/lib")

    # symlink /usr/bin <- /bin
    cmd.append("--symlink")
    cmd.append("usr/bin")
    cmd.append("/bin")

    # symlink /usr/sbin <- /sbin
    cmd.append("--symlink")
    cmd.append("usr/sbin")
    cmd.append("/sbin")

    # mount tmpfs at /tmp
    cmd.append("--tmpfs")
    cmd.append("/tmp")

    # bind-mount resolv.conf from host
    cmd.append("--ro-bind")
    cmd.append("/etc/resolv.conf")
    cmd.append("/etc/resolv.conf")

    # mount proc filesystem
    cmd.append("--proc")
    cmd.append("/proc")

    # mount dev filesystem
    cmd.append("--dev")
    cmd.append("/dev")

    # unshare everything except network
    cmd.append("--unshare-all")
    cmd.append("--share-net")

    # set XDG_RUNTIME_DIR
    if FRESH_XDG_RUNTIME_DIR:
        dir_xdg_runtime = "/run/user/" + str(os.getuid())

        cmd.append("--dir")
        cmd.append(dir_xdg_runtime)

        cmd.append("--setenv")
        cmd.append("XDG_RUNTIME_DIR")
        cmd.append(dir_xdg_runtime)

    else:
        cmd.append("--bind")
        cmd.append(os.getenv("XDG_RUNTIME_DIR"))
        cmd.append(os.getenv("XDG_RUNTIME_DIR"))

    # bind-mount passwd file
    cmd.append("--ro-bind")
    cmd.append("/etc/passwd")
    cmd.append("/etc/passwd")

    # bind-mount group file
    cmd.append("--ro-bind")
    cmd.append("/etc/group")
    cmd.append("/etc/group")

    # bind-mount font configuration files
    cmd.append("--ro-bind")
    cmd.append("/etc/fonts")
    cmd.append("/etc/fonts")

    cmd.append(prog)

    if len(sys.argv) > 2:
        for arg in sys.argv[2:]:
            cmd.append(arg)

    try:
        subprocess.run(cmd,
                       stdin=sys.stdin,
                       stderr=sys.stderr,
                       stdout=sys.stdout,
                       restore_signals=True)
    except IOError:
        return 1
    except subprocess.SubprocessError:
        return 1
    finally:
        return 0


if __name__ == "__main__":
    sys.exit(main())
