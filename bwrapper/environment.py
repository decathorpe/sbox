"""
This sub-module provides the code for the environment options of `bwrap`.
"""


class BWEnvironment:
    """
    This class encapsulates the environment options provided by `bwrap` and is used to generate the
    command line options for them.
    """

    def __init__(self):
        self.un_shares = list()
        self.share_net = False

        self.env_vars = dict()
        self.unset_vars = list()

        self.uid = None
        self.gid = None

        self.hostname = None

    def add_unshare(self, share_type: str):
        """This method adds a namespace that is to be un-shared with the child process."""
        if share_type in ["all", "user", "user-try", "ipc", "pid",
                          "net", "uts", "cgroup", "cgroup-try"]:
            if share_type == "all":
                self.un_shares = ["all"]
            elif "all" not in self.un_shares:
                self.un_shares.append(share_type)

        else:
            print("Unrecognised option '--unshare-{}'.".format(share_type))

    def add_share_net(self):
        """This method specifies that the network namespace should not be un-shared from the child
        process (only valid if `--unshare-all` is specified)."""
        if "all" in self.un_shares:
            self.share_net = True
        else:
            print("Network can only shared if '--unshare=all' has been specified.")

    def set_env(self, var: str, val: str):
        """This method specifies an environment variable that will be set in the sandbox."""
        self.env_vars[var] = val

    def unset_env(self, var: str):
        """This method specifies an environment variable that will be unset in the sandbox."""
        self.unset_vars.append(var)

    def set_uid(self, uid: int):
        """This method specifies that a separate UID will be used in the sandbox. This requires
        un-sharing the user namespace."""
        if "all" in self.un_shares or "user" in self.un_shares or "user-try" in self.un_shares:
            self.uid = uid
        else:
            print("Setting a new UID requires a new user namespace.")

    def set_gid(self, gid: int):
        """This method specifies that a separate GID will be used in the sandbox. This requires
        un-sharing the user namespace."""
        if "all" in self.un_shares or "user" in self.un_shares or "user-try" in self.un_shares:
            self.gid = str(gid)
        else:
            print("Setting a new GID requires a new user namespace.")

    def set_hostname(self, hostname: str):
        """This method specifies that a separate hostname will be used in the sandbox. This requires
        un-sharing the UTS namespace."""
        if "all" in self.un_shares or "uts" in self.un_shares:
            self.hostname = hostname
        else:
            print("Setting a new hostname requires a new UTS namespace.")

    def gen_args(self) -> list:
        """This method generates the CLI options for `bwrap` from this instance's attributes."""

        args = list()

        for env in self.env_vars:
            args.append("--setenv")
            args.append(env)
            args.append(self.env_vars[env])

        for env in self.unset_vars:
            args.append("--unsetenv")
            args.append(env)

        for unshare in self.un_shares:
            args.append("--unshare-" + unshare)

        if self.share_net:
            args.append("--share-net")

        if self.uid is not None:
            args.append("--uid")
            args.append(str(self.uid))

        if self.gid is not None:
            args.append("--gid")
            args.append(str(self.gid))

        if self.hostname is not None:
            args.append("--hostname")
            args.append(self.hostname)

        return args
