"""
This sub-module provides the code for the environment options of `bwrap`.
"""

import abc
import os
import tempfile


class BWFileSystemEntry(metaclass=abc.ABCMeta):
    """This abstract class defines that every filesystem entry needs a `.gen_args()` method."""

    @abc.abstractmethod
    def gen_args(self) -> list:
        """This method generates the CLI options for `bwrap` from this instance's attributes."""
        pass


class BWFSMountBind(BWFileSystemEntry):
    """This class defines a read-write mount point (file or directory)."""
    def __init__(self, src: str, dest: str):
        self.src = src
        self.dest = dest

    def gen_args(self) -> list:
        return ["--bind", self.src, self.dest]


class BWFSMountRoBind(BWFileSystemEntry):
    """This class defines a read-only mount point (file or directory)."""
    def __init__(self, src: str, dest: str):
        self.src = src
        self.dest = dest

    def gen_args(self) -> list:
        return ["--ro-bind", self.src, self.dest]


class BWFSMountDevBind(BWFileSystemEntry):
    """This class defines a device mount point."""
    def __init__(self, src: str, dest: str):
        self.src = src
        self.dest = dest

    def gen_args(self) -> list:
        return ["--dev-bind", self.src, self.dest]


class BWFSMountRemountRo(BWFileSystemEntry):
    """This class defines mount point that is to be re-mounted read-only (file or directory)."""
    def __init__(self, dest: str):
        self.dest = dest

    def gen_args(self) -> list:
        return ["--remount-ro", self.dest]


class BWFSMountProc(BWFileSystemEntry):
    """This class defines a proc filesystem mount point."""
    def __init__(self, dest: str):
        self.dest = dest

    def gen_args(self) -> list:
        return ["--proc", self.dest]


class BWFSMountDev(BWFileSystemEntry):
    """This class defines a devtmpfs mount point."""
    def __init__(self, dest: str):
        self.dest = dest

    def gen_args(self) -> list:
        return ["--dev", self.dest]


class BWFSMountTmpfs(BWFileSystemEntry):
    """This class defines a tmpfs mount point."""
    def __init__(self, dest: str):
        self.dest = dest

    def gen_args(self) -> list:
        return ["--tmpfs", self.dest]


class BWFSMountMqueue(BWFileSystemEntry):
    """This class defines an mqueue mount point."""
    def __init__(self, dest: str):
        self.dest = dest

    def gen_args(self) -> list:
        return ["--mqueue", self.dest]


class BWFSCreateDirectory(BWFileSystemEntry):
    """This class defines a directory that is to be created in the sandbox filesystem."""
    def __init__(self, dest: str):
        self.dest = dest

    def gen_args(self) -> list:
        return ["--dir", self.dest]


class BWFSCreateSymlink(BWFileSystemEntry):
    """This class defines a symbolic link that is to be created in the sandbox filesystem."""
    def __init__(self, src: str, dest: str):
        self.src = src
        self.dest = dest

    def gen_args(self) -> list:
        return ["--symlink", self.src, self.dest]


class BWFSCreateFileFromFD(BWFileSystemEntry):
    """This class defines a file that is to be created in the sandbox filesystem. The file's
    contents will be read from the supplied file descriptor."""
    def __init__(self, src: int, dest: str):
        self.src = src
        self.dest = dest

    def gen_args(self) -> list:
        return ["--file", str(self.src), self.dest]


class BWFileSystem:
    """
    This class encapsulates the filesystem options provided by `bwrap` and is used to generate the
    command line options for them.
    """

    def __init__(self):
        self.entries = list()
        self.used_names = list()
        self.temp_files = list()

    def add_bind_mount_rw(self, src: str, dest: str):
        """This method adds a read-write mount point to the file system."""
        if dest in self.used_names:
            print("Destination '{}' supplied multiple times.".format(dest))
        self.entries.append(BWFSMountBind(src, dest))

    def add_bind_mount_ro(self, src: str, dest: str):
        """This method adds a read-only mount point to the file system."""
        if dest in self.used_names:
            print("Destination '{}' supplied multiple times.".format(dest))
        self.entries.append(BWFSMountRoBind(src, dest))

    def add_bind_mount_dev(self, src: str, dest: str):
        """This method adds a device mount point to the file system."""
        if dest in self.used_names:
            print("Destination '{}' supplied multiple times.".format(dest))
        self.entries.append(BWFSMountDevBind(src, dest))

    def add_remount_readonly(self, dest: str):
        """This method specifies that this mount point will be re-mounted as read-only."""
        self.entries.append(BWFSMountRemountRo(dest))

    def add_proc(self, dest: str):
        """This method adds a proc filesystem to the file system."""
        if dest in self.used_names:
            print("Destination '{}' supplied multiple times.".format(dest))
        self.entries.append(BWFSMountProc(dest))

    def add_devtmpfs(self, dest: str):
        """This method adds a devtmpfs filesystem to the file system."""
        if dest in self.used_names:
            print("Destination '{}' supplied multiple times.".format(dest))
        self.entries.append(BWFSMountDev(dest))

    def add_tmpfs(self, dest: str):
        """This method adds a tmpfs filesystem to the file system."""
        if dest in self.used_names:
            print("Destination '{}' supplied multiple times.".format(dest))
        self.entries.append(BWFSMountTmpfs(dest))

    def add_mqueue(self, dest: str):
        """This method adds an mqueue to the file system."""
        if dest in self.used_names:
            print("Destination '{}' supplied multiple times.".format(dest))
        self.entries.append(BWFSMountMqueue(dest))

    def create_directory(self, dest: str):
        """This method adds an empty directory to the file system."""
        if dest in self.used_names:
            print("Destination '{}' supplied multiple times.".format(dest))
        self.entries.append(BWFSCreateDirectory(dest))

    def create_symlink(self, src: str, dest: str):
        """This method adds a symlink to the file system."""
        if dest in self.used_names:
            print("Destination '{}' supplied multiple times.".format(dest))
        self.entries.append(BWFSCreateSymlink(src, dest))

    def create_file_from_file(self, src: str, dest: str) -> int:
        """This method adds a file to the file system. It's contents will be read from the file at
        the specified path."""
        if dest in self.used_names:
            print("Destination '{}' supplied multiple times.".format(dest))

        if not os.path.exists(src):
            print("File at path {} could not be found.".format(src))
            return -1

        if not os.access(src, os.O_RDONLY):
            print("File at path {} could not be read.".format(src))
            return -1

        fd = os.open(src, os.O_RDONLY)
        self.entries.append(BWFSCreateFileFromFD(fd, dest))
        return fd

    def create_file_from_contents(self, contents: str, dest: str) -> int:
        """This method adds a file to the file system. It's contents will be the specified string.
        """
        if dest in self.used_names:
            print("Destination '{}' supplied multiple times.".format(dest))

        fd, path = tempfile.mkstemp(dir=os.getcwd(), prefix=".")
        self.temp_files.append(path)

        with open(path, "w") as file:
            file.write(contents)

        self.entries.append(BWFSCreateFileFromFD(fd, dest))
        return fd

    def create_file_from_fd(self, fd: int, dest: str):
        """This method adds a file to the file system. It's contents will be read from the
        specified file descriptor."""

        if dest in self.used_names:
            print("Destination '{}' supplied multiple times.".format(dest))
        self.entries.append(BWFSCreateFileFromFD(fd, dest))

    def gen_args(self) -> list:
        """This method generates the CLI options for `bwrap` from this instance's attributes."""

        args = list()

        for entry in self.entries:
            args.extend(entry.gen_args())

        return args
