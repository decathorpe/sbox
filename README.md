# sbox - simple application sandboxing

This "fun boredom project" is a WIP / Proof-of-concept of a sandboxing approach that uses the same
sandboxing technology as [flatpak](https://github.com/flatpak/flatpak)
([bubblewrap](https://github.com/projectatomic/bubblewrap)), but without doing packaging as well -
it uses the usual distribution-provided binaries.

So, in contrast to flatpak, there's no split between Application (in `/app`) and Runtime
(in `/usr`). Otherwise, the setup of the sandbox aims to be similar to how flatpak does things
(where possible).

Since my effort is already at a "Proof-of-concept" stage (though it's really crude if you look at
the code), running an example is as easy as executing the `sbox.py` script:

```sh
# Using the example application profile
# Hint: Mostly works, but not everything behaves as expected (WIP, as I said)
./sbox.py org.gnome.gedit

# Using a normal binary
# Hint: if no profile is found, the system default settings are used
./sbox.py gedit
```

