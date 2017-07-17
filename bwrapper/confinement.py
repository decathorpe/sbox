"""
This sub-module provides the code for the confinement options of `bwrap`.
"""

import os


class BWConfinement:
    """
    This class encapsulates the confinement options provided by `bwrap` and is used to generate the
    command line options for them.
    """

    def __init__(self):
        self.new_term_session = False

        self.seccomp_fd = None
        self.info_fd = None
        self.block_fds = list()

        self.exec_label = None
        self.file_label = None

    def use_new_terminal_session(self):
        """This method determines whether a new terminal session will be created for the child
        process with a `setsid()` call."""
        self.new_term_session = True

    def set_seccomp_rules_by_fd(self, fd: int):
        """This method sets the file descriptor that is passed with the `--seccomp` CLI flag to pass
        seccomp rules in the format of compiled eBPF programs."""
        if fd > 2:
            self.seccomp_fd = fd
        else:
            print("File descriptor number '{}' probably too small.".format(fd))

    def set_seccomp_rules_from_file(self, path: str):
        """This method opens a compiled eBPF file and sets the file descriptor that is passed with
        the `--seccomp` CLI flag to pass seccomp rules to `bwrap`."""
        if os.path.exists(path):
            self.seccomp_fd = os.open(path, os.O_RDONLY)
        else:
            print("Seccomp file cannot be found at the specified path.")

    def add_info_fd(self, fd: int):
        """This method sets a file descriptor that is passed to `bwrap`, and to which it writes
        information about the sandbox."""
        self.info_fd = fd

    def add_block_fd(self, fd: int):
        """This method adds file descriptors to the list of descriptors which block execution of the
        child program until data is available."""
        self.block_fds.append(fd)

    def set_exec_label(self, exec_label: str):
        """This method sets the SELinux executable label for the process running in the sandbox."""
        self.exec_label = exec_label

    def set_file_label(self, file_label: str):
        """This method sets the SELinux file label for the contents of the sandbox."""
        self.file_label = file_label

    def gen_args(self) -> list:
        """This method generates the CLI options for `bwrap` from this instance's attributes."""
        args = list()

        if self.new_term_session:
            args.append("--new-session")

        if self.exec_label is not None:
            args.extend(["--exec-label", self.exec_label])

        if self.file_label is not None:
            args.extend(["--file-label", self.file_label])

        if self.seccomp_fd is not None:
            args.extend(["--seccomp", str(self.seccomp_fd)])

        if self.info_fd is not None:
            args.extend(["--info-fd", str(self.info_fd)])

        for fd in self.block_fds:
            args.extend(["--block-fd", str(fd)])

        return args
