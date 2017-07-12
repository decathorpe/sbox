"""
python convenience wrapper around the bubblewrap (bwrap) CLI
"""

#     python convenience wrapper around the bubblewrap (bwrap) CLI
#     Copyright (C) 2017  Fabio Valentini
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.

import subprocess
import sys


class BubbleWrapper:
    def __init__(self):
        self.binds = dict()
        self.robinds = dict()
        self.devbinds = dict()
        self.remountros = list()

        self.proc = None
        self.dev = None
        self.tmpfs = list()
        self.mqueues = list()

        self.dirs = list()
        self.symlinks = dict()

        self.unshares = list()
        self.sharenet = False

        self.envs = dict()
        self.unenvs = list()

        self.uid = None
        self.gid = None

        self.chdir = None
        self.hostname = None
        self.execlabel = None
        self.filelabel = None

        self.lockfile = None
        self.newtermsession = False
        self.diewithparent = False

    def add_bind_mount(self, src: str, dest: str):
        self.binds[dest] = src

    def add_bind_mount_readonly(self, src: str, dest: str):
        self.robinds[dest] = src

    def add_bind_mount_dev(self, src: str, dest: str):
        self.devbinds[dest] = src

    def add_remount_readonly(self, dest: str):
        self.remountros.append(dest)

    def set_proc(self, dest: str):
        self.proc = dest

    def set_dev(self, dest: str):
        self.dev = dest

    def add_tmpfs(self, dest: str):
        self.tmpfs.append(dest)

    def add_mqueue(self, dest: str):
        self.mqueues.append(dest)

    def create_directory(self, dest: str):
        self.dirs.append(dest)

    def create_symlink(self, src: str, dest: str):
        self.symlinks[dest] = src

    def share_net(self):
        self.sharenet = True

    def add_unshare(self, share_type):
        assert share_type in ["all", "user", "user-try", "ipc", "pid",
                              "net", "uts", "cgroup", "cgroup-try"]
        self.unshares.append(share_type)

    def set_env(self, var: str, val: str):
        self.envs[var] = val

    def unset_env(self, var: str):
        self.unenvs.append(var)

    def set_uid(self, uid: int):
        self.uid = str(uid)

    def set_gid(self, gid: int):
        self.gid = str(gid)

    def set_chdir(self, chdir: str):
        self.chdir = chdir

    def set_hostname(self, hostname: str):
        self.hostname = hostname

    def set_exec_label(self, exec_label: str):
        self.execlabel = exec_label

    def set_file_label(self, file_label: str):
        self.filelabel = file_label

    def use_lock_file(self, lock_file: str):
        self.lockfile = lock_file

    def use_new_terminal_session(self):
        self.newtermsession = True

    def die_with_parent(self):
        self.diewithparent = True

    def exec(self, comm: str, args: list) -> int:
        cmd = list()

        cmd.append("bwrap")

        for bind in self.binds:
            cmd.append("--bind")
            cmd.append(self.binds[bind])
            cmd.append(bind)

        for robind in self.robinds:
            cmd.append("--ro-bind")
            cmd.append(self.robinds[robind])
            cmd.append(robind)

        for devbind in self.devbinds:
            cmd.append("--dev-bind")
            cmd.append(self.devbinds[devbind])
            cmd.append(devbind)

        for remountro in self.remountros:
            cmd.append("--remount-ro")
            cmd.append(remountro)

        if self.proc is not None:
            cmd.append("--proc")
            cmd.append(self.proc)

        if self.dev is not None:
            cmd.append("--dev")
            cmd.append(self.dev)

        for tmpfs in self.tmpfs:
            cmd.append("--tmpfs")
            cmd.append(tmpfs)

        for mqueue in self.mqueues:
            cmd.append("--mqueue")
            cmd.append(mqueue)

        for directory in self.dirs:
            cmd.append("--dir")
            cmd.append(directory)

        for symlink in self.symlinks:
            cmd.append("--symlink")
            cmd.append(self.symlinks[symlink])
            cmd.append(symlink)

        for unshare in self.unshares:
            cmd.append("--unshare-" + unshare)

        if self.sharenet:
            cmd.append("--share-net")

        for env in self.envs:
            cmd.append("--setenv")
            cmd.append(env)
            cmd.append(self.envs[env])

        for unenv in self.unenvs:
            cmd.append("--unsetenv")
            cmd.append(unenv)

        if self.uid is not None:
            cmd.append("--uid")
            cmd.append(self.uid)

        if self.gid is not None:
            cmd.append("--gid")
            cmd.append(self.gid)

        if self.chdir is not None:
            cmd.append("--chdir")
            cmd.append(self.chdir)

        if self.hostname is not None:
            cmd.append("--hostname")
            cmd.append(self.hostname)

        if self.execlabel is not None:
            cmd.append("--exec-label")
            cmd.append(self.execlabel)

        if self.filelabel is not None:
            cmd.append("--file-label")
            cmd.append(self.filelabel)

        if self.lockfile is not None:
            cmd.append("--lock-file")
            cmd.append(self.lockfile)

        if self.newtermsession:
            cmd.append("--new-session")

        if self.diewithparent:
            cmd.append("--die-with-parent")

        cmd.append(comm)

        for arg in args:
            cmd.append(arg)

        try:
            ret = subprocess.run(cmd,
                                 stdin=sys.stdin,
                                 stdout=sys.stdout,
                                 stderr=sys.stderr,
                                 restore_signals=True)

            if ret.returncode != 0:
                print("Process terminated with an error: {}".format(ret.returncode))
                return ret.returncode

        except IOError as error:
            print("Could not successfully execute subprocess. Original exception:")
            print(error)
            return -1
