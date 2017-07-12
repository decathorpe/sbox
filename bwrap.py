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
        self.shares = list()

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

    def exec(self, comm: str, args: list) -> int:
        cmd = list()

        cmd.append("bwrap")

        for bind in self.binds.keys():
            cmd.append("--bind")
            cmd.append(self.binds[bind])
            cmd.append(bind)

        for robind in self.robinds.keys():
            cmd.append("--ro-bind")
            cmd.append(self.robinds[robind])
            cmd.append(robind)

        for devbind in self.devbinds.keys():
            cmd.append("--dev-bind")
            cmd.append(self.devbinds[devbind])
            cmd.append(devbind)

        for remountro in self.remountros:
            cmd.append("--remount-ro")
            cmd.append(remountro)

        if not (self.proc is None):
            cmd.append("--proc")
            cmd.append(self.proc)

        if not (self.dev is None):
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

        for symlink in self.symlinks.keys():
            cmd.append("--symlink")
            cmd.append(self.symlinks[symlink])
            cmd.append(symlink)

        for unshare in self.unshares:
            cmd.append("--unshare-" + unshare)

        for share in self.shares:
            cmd.append("--share-" + share)

        for env in self.envs.keys():
            cmd.append("--setenv")
            cmd.append(env)
            cmd.append(self.envs[env])

        for unenv in self.unenvs:
            cmd.append("--unsetenv")
            cmd.append(unenv)

        if not (self.uid is None):
            cmd.append("--uid")
            cmd.append(self.uid)

        if not (self.gid is None):
            cmd.append("--gid")
            cmd.append(self.gid)

        if not (self.chdir is None):
            cmd.append("--chdir")
            cmd.append(self.chdir)

        if not (self.hostname is None):
            cmd.append("--hostname")
            cmd.append(self.hostname)

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

        except IOError as e:
            print("Could not successfully execute subprocess. Original exception:")
            print(e)
            return -1
