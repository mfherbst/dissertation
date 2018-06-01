# Dissertation
[![Build Status](https://travis-ci.org/mfherbst/dissertation.svg?branch=master)](https://travis-ci.org/mfherbst/dissertation)

This repository contains the `LaTeX` and `python` source code to build my
[PhD thesis](https://michael-herbst.com/phd-thesis.html)
titled **Development of a modular quantum-chemistry framework for the investigation
of novel basis functions**.
For more details about my PhD thesis see
[this article on my blog](https://michael-herbst.com/phd-thesis.html).

Either you [build the pdf](#building-the-thesis-for-yourself) for yourself
or alternatively you directly download the
[pdf document](https://michael-herbst.com/publications/2018.05_phd_corrected.pdf).
For citing my work please use the DOI 10.11588/heidok.00024519 or
[this bibtex file](https://michael-herbst.com/publications/2018.05_phd.bib).

## Building the thesis for yourself
In theory building should be as simple as
```sh
git clone --recursive https://github.com/mfherbst/dissertation
cd dissertation
make pdf
```

The build process automatically executes some `python` scripts,
which implicitly rely on a few packages. This includes `matplotlib`,
`numpy`, `scipy`, `pyyaml` and most importantly
[version 0.0.3 of `molsturm`](https://github.com/molsturm/molsturm/releases/tag/v0.0.3)
as well as [`gint`](https://molsturm.org/gint).
From `gint` the interfaces for
[`sturmint`](https://molsturm.org/sturmint) and
[`libint`](https://github.com/evaleev/libint)
should be enabled.
Before trying to build this PhD thesis you should make sure,
that the aforementioned programs are properly set up
in your path
... or you try what is explained in the next section.

## Building the thesis without `molsturm`
The Travis continuous integration system, which this repo employs
does not actually install `molsturm` to build the pdf documents.
Much rather it relies on some statically generated data to get around
this dependency. If you want to do the same,
this is roughly what you need to do
```sh
# Checkout repos
git clone --recursive https://github.com/mfherbst/dissertation
git clone --recursive https://github.com/mfherbst/dissertation-build-overlay

# Install dependencies (using pip)
pip install pyyaml matplotlib numpy scipy

# Setup build directory
mkdir dissertation/build
cd dissertation/build
cmake ..
. ../../dissertation-build-overlay/setup.sh

# Run the build
make
```
