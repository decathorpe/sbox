from unittest import TestCase

from bwrapper import BubbleWrapper
from bwrapper.tests.contains import contains


class TestBWEnvironment(TestCase):
    def test_add_unshare(self):
        unshare = "net"

        wrapper = BubbleWrapper()
        wrapper.environment.add_unshare(unshare)

        self.assertTrue(contains(["--unshare-net"], wrapper.gen_args()))

    def test_share_net(self):
        wrapper = BubbleWrapper()
        wrapper.environment.add_unshare("all")
        wrapper.environment.add_share_net()

        self.assertTrue(contains(["--share-net"], wrapper.gen_args()))
        self.assertTrue(contains(["--unshare-all"], wrapper.gen_args()))

    def test_set_env(self):
        var = "PATH"
        val = "/usr/bin:/usr/sbin"

        wrapper = BubbleWrapper()
        wrapper.environment.set_env(var, val)

        self.assertTrue(contains(["--setenv", var, val], wrapper.gen_args()))

    def test_unset_env(self):
        var = "HOME"

        wrapper = BubbleWrapper()
        wrapper.environment.unset_env(var)

        self.assertTrue(contains(["--unsetenv", var], wrapper.gen_args()))

    def test_set_uid(self):
        uid = 1001

        wrapper = BubbleWrapper()
        wrapper.environment.add_unshare("all")
        wrapper.environment.set_uid(uid)

        self.assertTrue(contains(["--uid", str(uid)], wrapper.gen_args()))

    def test_set_gid(self):
        gid = 1001

        wrapper = BubbleWrapper()
        wrapper.environment.add_unshare("all")
        wrapper.environment.set_gid(gid)

        self.assertTrue(contains(["--gid", str(gid)], wrapper.gen_args()))

    def test_set_hostname(self):
        hostname = "localhost"

        wrapper = BubbleWrapper()
        wrapper.environment.add_unshare("all")
        wrapper.environment.set_hostname(hostname)

        self.assertTrue(contains(["--hostname", hostname], wrapper.gen_args()))
