import os
from unittest import TestCase

from bwrapper import BubbleWrapper
from bwrapper.tests.contains import contains


class TestBWFilesystem(TestCase):
    def test_rw(self):
        src = "/usr"
        dest = "/usr"

        wrapper = BubbleWrapper()
        wrapper.filesystem.add_bind_mount_rw(src, dest)

        self.assertTrue(contains(["--bind", src, dest], wrapper.gen_args()))

    def test_ro(self):
        src = "/usr"
        dest = "/usr"

        wrapper = BubbleWrapper()
        wrapper.filesystem.add_bind_mount_ro(src, dest)

        self.assertTrue(contains(["--ro-bind", src, dest], wrapper.gen_args()))

    def test_dev(self):
        src = "/dev/dri"
        dest = "/dev/dri"

        wrapper = BubbleWrapper()
        wrapper.filesystem.add_bind_mount_dev(src, dest)

        self.assertTrue(contains(["--dev-bind", src, dest], wrapper.gen_args()))

    def test_remount_ro(self):
        dest = "/home"

        wrapper = BubbleWrapper()
        wrapper.filesystem.add_remount_readonly(dest)

        self.assertTrue(contains(["--remount-ro", dest], wrapper.gen_args()))

    def test_proc(self):
        dest = "/proc"

        wrapper = BubbleWrapper()
        wrapper.filesystem.add_proc(dest)

        self.assertTrue(contains(["--proc", dest], wrapper.gen_args()))

    def test_devtmpfs(self):
        dest = "/dev"

        wrapper = BubbleWrapper()
        wrapper.filesystem.add_devtmpfs(dest)

        self.assertTrue(contains(["--dev", dest], wrapper.gen_args()))

    def test_tmpfs(self):
        dest = "/tmp"

        wrapper = BubbleWrapper()
        wrapper.filesystem.add_tmpfs(dest)

        self.assertTrue(contains(["--tmpfs", dest], wrapper.gen_args()))

    def test_mqueue(self):
        dest = "/tmp/sboxmqueue"

        wrapper = BubbleWrapper()
        wrapper.filesystem.add_mqueue(dest)

        self.assertTrue(contains(["--mqueue", dest], wrapper.gen_args()))

    def test_dir(self):
        dest = "/home/sbox"

        wrapper = BubbleWrapper()
        wrapper.filesystem.create_directory(dest)

        self.assertTrue(contains(["--dir", dest], wrapper.gen_args()))

    def test_symlink(self):
        src = "/usr/bin"
        dest = "/bin"

        wrapper = BubbleWrapper()
        wrapper.filesystem.create_symlink(src, dest)

        self.assertTrue(contains(["--symlink", src, dest], wrapper.gen_args()))

    def test_file_from_fd(self):
        src = 42
        dest = "/etc/sbox.conf"

        wrapper = BubbleWrapper()
        wrapper.filesystem.create_file_from_fd(src, dest)

        self.assertTrue(contains(["--file", str(src), dest], wrapper.gen_args()))

    def test_file_from_file(self):
        src = "README.md"
        dest = "/home/sbox/README.md"

        wrapper = BubbleWrapper()
        fd = wrapper.filesystem.create_file_from_file(src, dest)
        os.close(fd)

        self.assertTrue(contains(["--file", str(fd), dest], wrapper.gen_args()))

    def test_file_from_contents(self):
        contents = "Test Contents\n"
        dest = "/tmp/sbox/test_file"

        wrapper = BubbleWrapper()
        fd = wrapper.filesystem.create_file_from_contents(contents, dest)
        os.close(fd)

        for path in wrapper.filesystem.temp_files:
            os.remove(path)

        self.assertTrue(contains(["--file", str(fd), dest], wrapper.gen_args()))
