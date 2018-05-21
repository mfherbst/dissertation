#!/usr/bin/env python3
import molsturm
from molsturm import construct_basis
import common
from matplotlib import pyplot as plt
import numpy as np

SYSTEM = molsturm.System("H")
BASES = [
    ("--", "cGTO cc-pVDZ", construct_basis("gaussian", SYSTEM,
                                           basis_set_name="cc-pvdz")),
    (":", "cGTO cc-pV6Z", construct_basis("gaussian", SYSTEM,
                                          basis_set_name="cc-pv6z")),
#    ("", "CS $(3,1,1)$ $k = 1.2$", construct_basis("sturmian/atomic", SYSTEM,
#                                                   n_max=3, l_max=1, m_max=1,
#                                                   k_exp=1.2)),
    ("-.", "CS $(3,1,1)$ $k = 0.8$", construct_basis("sturmian/atomic", SYSTEM,
                                                     n_max=3, l_max=1, m_max=1,
                                                     k_exp=0.8)),
    ("", "CS $(4,1,1)$ $k = 0.8$", construct_basis("sturmian/atomic", SYSTEM,
                                                   n_max=4, l_max=1, m_max=1,
                                                   k_exp=0.8)),
]


def plot_relative_error():
    plt.close()
    plt.figure(figsize=(6, 2.5))

    for mark, label, bas in BASES:
        coeff = common.do_hydrogen_scf(bas)
        rab = np.linspace(0, 1, 5000), np.linspace(1, 8, 5000)
        r = np.concatenate(rab)
        r, err = common.hydrogen_relative_error(bas, coeff, r, mirror=False)

        plt.plot(r, err, mark, label=label)

    plt.xlabel(common.XLABEL)
    plt.ylabel(common.RELABEL)

    plt.legend(loc="upper left")
    plt.ylim(-0.5, 0.5)


def plot_local_energy():
    plt.close()
    plt.figure(figsize=(6, 2.5))

    for mark, label, bas in BASES:
        coeff = common.do_hydrogen_scf(bas)
        rab = np.linspace(0, 1, 5000), np.linspace(1, 6, 5000)
        r = np.concatenate(rab)
        r = np.linspace(0, 1, 5000)
        r, locen = common.hydrogen_local_energy(bas, coeff, r, dr=5e-6,
                                                mirror=False)
        plt.plot(r, locen, mark, label=label)

    #plt.plot(r, -0.5*np.ones_like(locen), label="exact")
    plt.xlabel(common.XLABEL)
    plt.ylabel(common.ELLABEL)

    plt.legend(loc='upper right')
    plt.ylim(-2.5, 2.5)


def main():
    common.setup()

    plot_local_energy()
    plt.savefig("local_energy_cgto_cs.pdf", bbox_inches="tight")

    plot_relative_error()
    plt.savefig("relative_error_cgto_cs.pdf", bbox_inches="tight")


if __name__ == "__main__":
    main()
