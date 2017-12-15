# Dissertation
[![Build Status](https://travis-ci.com/mfherbst/dissertation.svg?token=mMrhPoF738uUamSScbrZ&branch=master)](https://travis-ci.com/mfherbst/dissertation)

This repository contains the TeX and python source code to build
my PhD thesis.
The whole thing is heavily work in progress right now of course ;).

## Building
Should be as simple as
```sh
git clone --recursive https://github.com/mfherbst/dissertation
cd dissertation
make pdf
```

Note, however, that the build process automatically executes
some `python` scripts during the build, which implicitly rely
on the presence of
[version 0.1.0 of molsturm](https://github.com/molsturm/molsturm/releases/tag/v0.1.0)
together with [`gint`](https://molsturm.org/gint),
[`sturmint`](https://molsturm.org/sturmint) and
[`libint`](https://github.com/evaleev/libint).
Before trying to build the thesis you should make sure,
that the aforementioned programs are properly set up
in your path
... or you try what is explained in the next section.

## Build the thesis without `molsturm`
The continuous integration system I employ for testing the latex builds
does not install molsturm. Much rather it uses some statically generated data
to get around this.
If you want to do the same, this is roughly what you need to do
```sh
# Checkout repos
git clone --recursive https://github.com/mfherbst/dissertation
git clone --recursive https://github.com/mfherbst/dissertation-build-overlay

# Setup build directory
mkdir dissertation/build
cd dissertation/build
cmake ..
. ../../dissertation-build-overlay/setup.sh

# Run the build
make
```
