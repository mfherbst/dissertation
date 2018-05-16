#!/usr/bin/env python3

import molsturm
import common
from matplotlib import pyplot as plt
import numpy as np


BASIS_SETS = ["STO-3G", "cc-pVDZ", "pc-1", "pc-3", "cc-pV6Z"]


def plot_overview():
    plt.close()
    plt.figure(figsize=(5.5, 3.5))

    for baset in BASIS_SETS:
        bas = molsturm.construct_basis("gaussian", "H", basis_set_name=baset)
        coeff = common.do_hydrogen_scf(bas)

        rab = np.linspace(0, 1, 5000), np.linspace(1, 10, 5000)
        r = np.concatenate(rab)
        r, locen = common.hydrogen_local_energy(bas, coeff, r, dr=1e-6)
        plt.plot(r, locen, label=baset)

    plt.xlabel(common.XLABEL)
    plt.ylabel(common.ELLABEL)

    plt.ylim(-5, 5)
    if -0.5 not in plt.yticks()[0]:
        plt.yticks(list(plt.yticks()[0]) + [-0.5])
    plt.legend(loc='upper right')


def plot_closeup():
    plt.close()
    plt.figure(figsize=(5.5, 3.5))

    for baset in BASIS_SETS:
        bas = molsturm.construct_basis("gaussian", "H", basis_set_name=baset)
        coeff = common.do_hydrogen_scf(bas)

        rab = np.linspace(0, 0.05, 5000), np.linspace(0.05, 0.5, 5000)
        r = np.concatenate(rab)
        r, locen = common.hydrogen_local_energy(bas, coeff, r, dr=1e-6)
        plt.plot(r, locen, label=baset)

    plt.xlabel(common.XLABEL)
    plt.ylabel(common.ELLABEL)

    plt.ylim(-5, 5)
    if -0.5 not in plt.yticks()[0]:
        plt.yticks(list(plt.yticks()[0]) + [-0.5])


def plot_relative_error(log=False):
    plt.close()
    plt.figure(figsize=(5.5, 3.5))

    for baset in BASIS_SETS:
        bas = molsturm.construct_basis("gaussian", "H", basis_set_name=baset)
        coeff = common.do_hydrogen_scf(bas)

        rab = np.linspace(0, 1, 10000), np.linspace(1, 10, 10000)
        r = np.concatenate(rab)
        r, err = common.hydrogen_relative_error(bas, coeff, r)

        if log:
            plt.semilogy(r, np.abs(err), label=baset)
            extra = "absolute of "
        else:
            plt.plot(r, err, label=baset)
            extra = ""

    plt.xlabel(common.XLABEL)
    plt.ylabel(extra + common.RELABEL)

    plt.legend(loc='lower right')
    plt.ylim(-0.2, 0.2)


def main():
    common.setup()

    plot_overview()
    plt.savefig("local_energy_cgto.pdf", bbox_inches="tight")

    plot_closeup()
    plt.savefig("local_energy_cgto_zoom.pdf", bbox_inches="tight")

    plot_relative_error(log=False)
    plt.savefig("relative_error_cgto.pdf", bbox_inches="tight")


if __name__ == "__main__":
    main()
