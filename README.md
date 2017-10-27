# Dissertation

This repository contains the TeX and python source code to build
my PhD thesis.
The whole thing is healily work in progress right now of course ;).

## Building
Before you can build the thesis you will need the most recent versions
of [`molsturm`](https://molsturm.org)
and [`gint`](https://molsturm.org/gint) to dynamically build the
plots and tables together with the tex code.
As the integral backends we need `sturmint` as well as another Gaussian
library (`libint` is fine).

Building should be as simple as calling a `make all` in the root
directory of the repository.
