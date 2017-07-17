"""
This python module is a convenience wrapper around the bubblewrap (`bwrap`) CLI.

Methods corresponding to all bwrap CLI options are supported, with the exception of
- `--args FD`,
- `--bind-data FD DEST`, and
- `--ro-bind-data FD DEST`.

Obviously `--help` and `--version` aren't passed through to bwrap either.
"""

from bwrapper.bwrap import BubbleWrapper
