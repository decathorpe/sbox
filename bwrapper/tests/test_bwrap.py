from unittest import TestCase

from bwrapper import BubbleWrapper
from bwrapper.tests.contains import contains


class TestBW(TestCase):
    def test_chdir(self):
        dest = "/tmp"

        wrapper = BubbleWrapper()
        wrapper.set_chdir(dest)

        self.assertTrue(contains(["--chdir", dest], wrapper.gen_args()))

    def test_sync_fd(self):
        fd = 42

        wrapper = BubbleWrapper()
        wrapper.add_sync_fd(fd)

        self.assertTrue(contains(["--sync-fd", str(fd)], wrapper.gen_args()))

    def test_lock_file(self):
        path = ".lock"

        wrapper = BubbleWrapper()
        wrapper.use_lock_file(path)

        self.assertTrue(contains(["--lock-file", path], wrapper.gen_args()))

    def test_die_with_parent(self):
        wrapper = BubbleWrapper()
        wrapper.set_die_with_parent()

        self.assertTrue(contains(["--die-with-parent"], wrapper.gen_args()))
