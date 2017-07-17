"""
This module contains the main class of this module, `BubbleWrapper`. It encapsulates all available
functionality.
"""

import os
import subprocess
import sys

import psutil

from bwrapper.confinement import BWConfinement
from bwrapper.environment import BWEnvironment
from bwrapper.filesystem import BWFileSystem


class BubbleWrapper:
    """
    This class encapsulates all functionality of the `bwrapper` module.

    If the `bwrap` argument is not specified at initialization, the `bwrap` command found in
    `$PATH` in the usual way will be used.

    :param bwrap: path to bwrap binary (optional)
    """

    def __init__(self, bwrap: str = None):
        if bwrap is not None:
            self.bwrap = bwrap
        else:
            self.bwrap = "bwrap"

        self.filesystem = BWFileSystem()
        self.environment = BWEnvironment()
        self.confinement = BWConfinement()

        self.chdir = None
        self.lock_file = None
        self.sync_fds = list()

        self.die_with_parent = False

    def set_chdir(self, chdir: str):
        """This method sets the directory to change to after entering the sandbox."""
        self.chdir = chdir

    def add_sync_fd(self, fd: int):
        """This method adds a file descriptor to the list of descriptors that will be kept in sync
        during the execution of bwrap."""
        self.sync_fds.append(fd)

    def use_lock_file(self, lock_file: str):
        """This method specifies that bwrap will hold a lock file during the execution of the child
        process."""
        self.lock_file = lock_file

    def set_die_with_parent(self):
        """This method specifies that the bwrap process will die if it's parent process dies."""
        self.die_with_parent = True

    def cleanup(self):
        """This method cleans up after the execution of the child process - it closes any open file
        descriptors and removes any created temporary files."""
        for fd in psutil.Process().open_files():
            if fd > 2:
                os.close(fd)

        for file in self.filesystem.temp_files:
            os.remove(file)

    def gen_args(self) -> list:
        """This method generates the CLI options for `bwrap` from this instance's attributes."""

        args = list()

        args.append(self.bwrap)

        args.extend(self.filesystem.gen_args())
        args.extend(self.environment.gen_args())
        args.extend(self.confinement.gen_args())

        if self.chdir is not None:
            args.extend(["--chdir", self.chdir])

        for fd in self.sync_fds:
            args.extend(["--sync-fd", str(fd)])

        if self.lock_file is not None:
            args.extend(["--lock-file", self.lock_file])

        if self.die_with_parent:
            args.append("--die-with-parent")

        return args

    def exec(self, comm: str, args: list) -> int:
        """
        This method executes the command `comm` with arguments `args` in the sandbox defined by this
        object's parameters. After the child process has terminated, file descriptors are closed and
        temporary files are removed by executing the `.cleanup()` method.

        :param comm: command to execute in the sandbox
        :param args: arguments for the command
        :return: passes through the return value of the child process
        """

        cmd = self.gen_args()

        cmd.append(comm)

        for arg in args:
            cmd.append(arg)

        for fd in psutil.Process().open_files():
            os.set_inheritable(fd)

        try:
            ret = subprocess.run(cmd, restore_signals=True,
                                 stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr)

            if ret.returncode != 0:
                print("Process terminated with an error: {}".format(ret.returncode))

            return ret.returncode

        except IOError as error:
            print("Could not successfully execute subprocess. Original exception:")
            print(error)
            return -1

        finally:
            self.cleanup()
