# Dissertation
[![Build Status](https://travis-ci.com/mfherbst/dissertation.svg?token=mMrhPoF738uUamSScbrZ&branch=master)](https://travis-ci.com/mfherbst/dissertation)

This repository contains the `LaTeX` and `python` source code to build by PhD thesis
titled **Development of a modular
quantum-chemistry framework
for the investigation of novel
basis functions**.  

Either you [build the pdf](#building) for yourself
or you download the the
[latest version](https://github.com/mfherbst/dissertation/releases/latest),
where all known errors have been corrected.
Alternatively you can download the version
[printed and published](https://github.com/mfherbst/dissertation/releases/download/v1.0.0/dissertation.pdf)
and live with the typos and errors,
which were already discovered by now.

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
[version 0.0.3 of molsturm](https://github.com/molsturm/molsturm/releases/tag/v0.0.3)
together with [`gint`](https://molsturm.org/gint),
[`sturmint`](https://molsturm.org/sturmint) and
[`libint`](https://github.com/evaleev/libint).
Before trying to build the thesis you should make sure,
that the aforementioned programs are properly set up
in your path
... or you try what is explained in the next section.

## Build the thesis without `molsturm`
The continuous integration system, which is employed to build
the published pdfs does not install `molsturm`.
Much rather it uses some statically generated data to get around this.
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
