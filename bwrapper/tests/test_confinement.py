import os
from unittest import TestCase

from bwrapper import BubbleWrapper
from bwrapper.tests.contains import contains


class TestBWConfinement(TestCase):
    def test_new_terminal_session(self):
        wrapper = BubbleWrapper()
        wrapper.confinement.use_new_terminal_session()

        self.assertTrue(contains(["--new-session"], wrapper.gen_args()))

    def test_seccomp_rules_from_fd(self):
        src = 42

        wrapper = BubbleWrapper()
        wrapper.confinement.set_seccomp_rules_by_fd(src)

        self.assertTrue(contains(["--seccomp", str(src)], wrapper.gen_args()))

    def test_seccomp_rules_from_file(self):
        # Just use a random file here
        src = "README.md"

        wrapper = BubbleWrapper()
        wrapper.confinement.set_seccomp_rules_from_file(src)
        os.close(wrapper.confinement.seccomp_fd)

        self.assertTrue(contains(["--seccomp", str(wrapper.confinement.seccomp_fd)],
                                 wrapper.gen_args()))

    def test_info_fd(self):
        dest = 42

        wrapper = BubbleWrapper()
        wrapper.confinement.add_info_fd(dest)

        self.assertTrue(contains(["--info-fd", str(dest)], wrapper.gen_args()))

    def test_block_fd(self):
        dest = 42

        wrapper = BubbleWrapper()
        wrapper.confinement.add_block_fd(dest)

        self.assertTrue(contains(["--block-fd", str(dest)], wrapper.gen_args()))

    def test_exec_label(self):
        label = "test"

        wrapper = BubbleWrapper()
        wrapper.confinement.set_exec_label(label)

        self.assertTrue(contains(["--exec-label", label], wrapper.gen_args()))

    def test_file_label(self):
        label = "test"

        wrapper = BubbleWrapper()
        wrapper.confinement.set_file_label(label)

        self.assertTrue(contains(["--file-label", label], wrapper.gen_args()))
