# sbox - simple application sandboxing

This "fun boredom project" is a WIP / Proof-of-concept of a sandboxing approach that uses the same
sandboxing technology as [flatpak](https://github.com/flatpak/flatpak)
([bubblewrap](https://github.com/projectatomic/bubblewrap)), but without doing packaging as well -
it uses the usual distribution-provided binaries.

So, in contrast to flatpak, there's no split between Application (in `/app`) and Runtime
(in `/usr`). Otherwise, the setup of the sandbox aims to be similar to how flatpak does things
(where possible).

I've unbundled the python wrapper around bubblewrap and made it it's own project, which can now be
found at [decathorpe/bwrapper](http://github.com/decathorpe/bwrapper). Almost all CLI options of
`bwrap` are available via the wrapper module, and it should be more or less finished.

## sbox in action (WIP)

Since my effort is already at a "Proof-of-concept" stage (though it's really crude if you look at
the code), running an example is as easy as executing the `sbox.py` script:

```sh
# Using the example application profile
# Hint: Mostly works, but not everything behaves as expected (WIP, as I said)
./test.py org.gnome.gedit

# Using a normal binary
# Hint: if no profile is found, the system default settings are used
./test.py bash
```

## What's next?

Right now, I'm looking into how flatpak translates its sandboxing options (e.g. `--share=x11`) down
to the low-level `bwrap` arguments. Then, I'll adapt `sbox` to use the same options and make them
pass the same arguments to `bwrap`. This might take some time, because I'm unfamiliar with GObject
and the flatpak code-base is ... big (one of the files I'm interested in is more than 4K LOC ...).
