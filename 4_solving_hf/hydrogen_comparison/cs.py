#!/usr/bin/env python3

import molsturm
import common
from matplotlib import pyplot as plt
import numpy as np


LMAX = 1  # Maximal angular momentum used


def plot_local_energy_overview():
    plt.close()
    plt.figure(figsize=(5.5, 3.5))

    sys = molsturm.System("H")
    bases = [
        molsturm.construct_basis("sturmian/atomic", sys, n_max=3, l_max=LMAX,
                                 m_max=LMAX, k_exp=1.4),
        molsturm.construct_basis("sturmian/atomic", sys, n_max=3, l_max=LMAX,
                                 m_max=LMAX, k_exp=1.2),
        molsturm.construct_basis("sturmian/atomic", sys, n_max=3, l_max=LMAX,
                                 m_max=LMAX, k_exp=0.8),
        molsturm.construct_basis("sturmian/atomic", sys, n_max=5, l_max=LMAX,
                                 m_max=LMAX, k_exp=0.8),
    ]

    for bas in bases:
        coeff = common.do_hydrogen_scf(bas)
        rab = np.linspace(0, 1, 5000), np.linspace(1, 10, 5000)
        r = np.concatenate(rab)
        r, locen = common.hydrogen_local_energy(bas, coeff, r, dr=5e-6)

        label = "({},{},{})".format(*np.max(bas.functions, axis=0))
        label += r" $k_\text{exp}=" + "{:.1f}$".format(bas.k_exp)
        plt.plot(r, locen, label=label)

    plt.xlabel(common.XLABEL)
    plt.ylabel(common.ELLABEL)
    plt.ylim(-1.5, 0.5)
    if -0.5 not in plt.yticks()[0]:
        plt.yticks(list(plt.yticks()[0]) + [-0.5])

    plt.plot(r, -0.5*np.ones_like(locen), label=r"exact, $k_\text{exp} = 1.0$")
    plt.legend(loc='upper right')


def plot_local_energy_closeup():
    plt.close()
    plt.figure(figsize=(5.5, 3.5))

    sys = molsturm.System("H")
    bases = [
        molsturm.construct_basis("sturmian/atomic", sys, n_max=3, l_max=LMAX,
                                 m_max=LMAX, k_exp=0.8),
        molsturm.construct_basis("sturmian/atomic", sys, n_max=5, l_max=LMAX,
                                 m_max=LMAX, k_exp=0.8),
        molsturm.construct_basis("sturmian/atomic", sys, n_max=7, l_max=LMAX,
                                 m_max=LMAX, k_exp=0.8),
    ]
    colors = ["tab:green", "tab:red", "tab:orange"]

    for i, bas in enumerate(bases):
        coeff = common.do_hydrogen_scf(bas)

        rab = np.linspace(0, 0.05, 5000), np.linspace(0.05, 0.5, 5000)
        r = np.concatenate(rab)
        r, locen = common.hydrogen_local_energy(bas, coeff, r, dr=1e-6)

        label = "({},{},{})".format(*np.max(bas.functions, axis=0))
        label += r" $k_\text{exp}=" + "{:.1f}$".format(bas.k_exp)
        plt.plot(r, locen, colors[i], label=label)

    plt.xlabel(common.XLABEL)
    plt.ylabel(common.ELLABEL)
    plt.ylim(-1.5, -0.25)
    if -0.5 not in plt.yticks()[0]:
        plt.yticks(list(plt.yticks()[0]) + [-0.5])

    plt.legend()


def plot_relative_error(log=False):
    plt.close()
    plt.figure(figsize=(5.5, 3.5))

    sys = molsturm.System("H")
    bases = [
        molsturm.construct_basis("sturmian/atomic", sys, n_max=3, l_max=LMAX,
                                 m_max=LMAX, k_exp=1.4),
        molsturm.construct_basis("sturmian/atomic", sys, n_max=3, l_max=LMAX,
                                 m_max=LMAX, k_exp=1.2),
        molsturm.construct_basis("sturmian/atomic", sys, n_max=3, l_max=LMAX,
                                 m_max=LMAX, k_exp=0.8),
        molsturm.construct_basis("sturmian/atomic", sys, n_max=5, l_max=LMAX,
                                 m_max=LMAX, k_exp=0.8),
    ]

    for bas in bases:
        coeff = common.do_hydrogen_scf(bas)
        rab = np.linspace(0, 1, 10000), np.linspace(1, 10, 10000)
        r = np.concatenate(rab)
        r, err = common.hydrogen_relative_error(bas, coeff, r)

        label = "({},{},{})".format(*np.max(bas.functions, axis=0))
        label += r" $k_\text{exp}=" + "{:.1f}$".format(bas.k_exp)

        if log:
            plt.semilogy(r, np.abs(err), label=label)
            extra = "absolute of "
        else:
            plt.plot(r, err, label=label)
            extra = ""

    plt.plot(r, np.zeros_like(err), label=r"exact, $k_\text{exp} = 1.0$")
    plt.xlabel(common.XLABEL)
    plt.ylabel(extra + common.RELABEL)
    plt.ylim(-0.2, 0.2)

    plt.legend(loc='upper left')


def main():
    common.setup()

    plot_local_energy_overview()
    plt.savefig("local_energy_cs.pdf", bbox_inches="tight")

    plot_local_energy_closeup()
    plt.savefig("local_energy_cs_zoom.pdf", bbox_inches="tight")

    plot_relative_error(log=False)
    plt.savefig("relative_error_cs.pdf", bbox_inches="tight")


if __name__ == "__main__":
    main()
