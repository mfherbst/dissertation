#!/usr/bin/env python3

from matplotlib import pyplot as plt
import matplotlib
import molsturm
import numpy as np
import os
import collections


FIGSIZE = (4.8, 3.2)
dir_of_this_file = os.path.dirname(__file__)
OrbitalSelection = collections.namedtuple("OrbitalSelection",
                                          ["indices", "labels"])


def load_gauss_atom(atom):
    if os.path.isfile(dir_of_this_file + "/" + atom + "_cc-pv5z.hdf5"):
        return molsturm.load_hdf5(dir_of_this_file + "/" + atom +
                                  "_cc-pv5z.hdf5")
    else:
        return molsturm.load_hdf5(dir_of_this_file + "/" + atom +
                                  "_cc-pv6z.hdf5")


def compute_rms_lf(state):
    """
    Computes the root mean square coefficient values
    with respect to l per orbtial f for a Gaussian basis.
    """
    coeff_bf = state["orbcoeff_bf"]

    basis = state.input_parameters.basis
    l_max = max(sh.l for sh in basis.shells)
    rnge = list(range(l_max+1))

    idx_to_l = []
    for sh in basis.shells:
        for i in range(sh.n_bas):
            idx_to_l.append(sh.l)

    def make_predicate(l):
        return lambda i: idx_to_l[i] == l

    ret = np.empty((len(rnge), coeff_bf.shape[1]))
    for qnum in rnge:
        # Mask to filter all basis functions with the desired quantum number
        pred = make_predicate(qnum)
        mask = np.array([pred(i) for i in range(coeff_bf.shape[0])])

        # Build the average sum of squares:
        ret[qnum, :] = np.average(np.square(coeff_bf[mask, :]), axis=0)

        # And take the square root
        ret[qnum, :] = np.sqrt(ret[qnum, :])
    return ret


def compute_rmso_l(state):
    """
    Compute the root mean square coefficient value
    per l for Gaussians.
    """
    noa = state["n_orbs_alpha"]
    na = state["n_alpha"]
    nb = state["n_beta"]

    rms_lf = compute_rms_lf(state)
    rmsa_lf = rms_lf[:, :noa]
    rmsb_lf = rms_lf[:, noa:]

    # Compute the sum of squares:
    tmp = np.average(np.square(rmsa_lf[:, :na]), axis=1)
    tmp += np.average(np.square(rmsb_lf[:, :nb]), axis=1)

    # Build the average, the square root and return
    return np.sqrt(tmp)


def plot_rmso_l(systems):
    plt.close()
    plt.figure(figsize=FIGSIZE)

    data = {}
    for atom in systems:
        state = load_gauss_atom(atom)
        lpop = compute_rmso_l(state)
        ls = np.arange(0, len(lpop))
        plt.semilogy(ls, lpop, "x-", label=atom)
        data[atom] = lpop.tolist()

    plt.ylim([1e-16, 1])
    plt.xlabel(r"Angular momentum quantum number $l$")
    plt.ylabel(r"$\text{RMSO}_l$")
    plt.legend()


def plot_rms_lf_orbitals(atom, selection=None):
    if selection is None:
        selection = OrbitalSelection(list(range(10)),
                                     [str(i) for i in range(10)])

    plt.close()
    plt.figure(figsize=FIGSIZE)

    state = load_gauss_atom(atom)
    data = compute_rms_lf(state)
    ls = np.arange(0, data[:, 0].size)
    for i, f in enumerate(selection.indices):
        plt.semilogy(ls, data[:, f], "x-", label=selection.labels[i])

    plt.ylim([1e-16, 1])
    plt.ylabel(r"Root mean square coefficient value")
    plt.xlabel(r"Angular momentum quantum number $l$")
    plt.legend(loc=1)


def setup():
    tex_premable = [
        r"\usepackage[T1]{fontenc}",
        r"\usepackage[utf8]{inputenc}",
        r"\usepackage{lmodern}",
        r"\usepackage{amsmath}",
    ]
    pgf_with_rc_fonts = {
        "pgf.texsystem": "pdflatex",
        "font.family": "serif",
        "text.usetex": True,
        "text.latex.preamble": tex_premable,
        "pgf.rcfonts": False,
        "pgf.preamble": tex_premable,
    }
    matplotlib.rcParams.update(pgf_with_rc_fonts)


def main():
    setup()

    plot_rmso_l(["Li", "Be", "B", "C", "N", "O", "F", "Ne"])
    plt.savefig("ccpvnz_rmso_period2_vs_l.pdf", bbox_inches="tight")

    plot_rmso_l(["Na", "Mg", "Al", "Si", "P", "S", "Cl", "Ar"])
    plt.savefig("ccpvnz_rmso_period3_vs_l.pdf", bbox_inches="tight")

    selection = {
        "C": OrbitalSelection([1, 3, 9], ["2s", "2p", "3d"]),
        "N": OrbitalSelection([1, 3, 9], ["2s", "2p", "3d"]),
        "O": OrbitalSelection([1, 3, 9], ["2s", "2p", "3d"]),
    }

    plot_rms_lf_orbitals("O", selection["O"])
    plt.savefig("ccpvnz_rms_lf_O.pdf",bbox_inches="tight")

    plot_rms_lf_orbitals("N", selection["N"])
    plt.savefig("ccpvnz_rms_lf_N.pdf",bbox_inches="tight")

    plot_rms_lf_orbitals("C", selection["C"])
    plt.savefig("ccpvnz_rms_lf_C.pdf",bbox_inches="tight")


if __name__ == "__main__":
    main()
