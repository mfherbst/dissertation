#!/usr/bin/env python3

from matplotlib import pyplot as plt
import matplotlib
import molsturm
import numpy as np
import os
import yaml
import rmsl


dir_of_this_file = os.path.dirname(__file__)


def datafile(atom):
    n, l, m = (6, 5, 5)
    file_655 = dir_of_this_file + "/" + atom + "_n" + str(n) + \
        "-l" + str(l) + "-m" + str(m) + ".hdf5"
    file_766 = dir_of_this_file + "/" + atom + "_n" + str(n + 1) + \
        "-l" + str(l + 1) + "-m" + str(m + 1) + ".hdf5"
    if os.path.isfile(file_655):
        return file_655
    else:
        return file_766


def plot_rmso_l(systems):
    plt.close()
    plt.figure(figsize=(5.5, 3.5))

    data = {}
    for atom in systems:
        state = molsturm.load_hdf5(datafile(atom))
        lpop = rmsl.compute_rmso_q(state)
        ls = np.arange(0, len(lpop))
        plt.semilogy(ls, lpop, "x-", label=r"\ce{" + atom + "}")
        data[atom] = lpop.tolist()

    if systems[0] == "Li":
        name = "rmso_period2_data.yaml"
    elif systems[0] == "Na":
        name = "rmso_period3_data.yaml"
    elif systems[0] == "B+":
        name = "rmso_ions_data.yaml"
    else:
        raise NotImplementedError("Only first and second period implemented.")
    with open(name, "w") as f:
        yaml.safe_dump(data, f)

    plt.ylim([1e-16, 1])
    plt.xlabel(r"Orbital angular momentum value $l$")
    plt.ylabel(r"$\text{RMSO}_l$")
    plt.legend()


def plot_rms_lf(atom, orbitals=range(10), labels=None):
    plt.close()
    plt.figure(figsize=(5.5, 3.5))

    state = molsturm.load_hdf5(datafile(atom))
    data = rmsl.compute_rms_qf(state)
    ls = np.arange(0, data[:, 1].size)

    if labels is None:
        labels = [str(i) for i in range(len(orbitals))]
    for i, f in enumerate(orbitals):
        plt.semilogy(ls, data[:, f], "x-", label=labels[i])

    plt.ylim([1e-16, 1])
    plt.ylabel(r"root meam square coefficient value")
    plt.xlabel(r"Orbital angular momentum value $l$")
    plt.legend(loc=1)


def setup():
    tex_premable = [
        r"\usepackage[utf8x]{inputenc}",
        r"\usepackage[T1]{fontenc}",
        r"\usepackage{lmodern}",
        r"\usepackage{amsmath}",
        r"\usepackage[version=3]{mhchem}",
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
    plt.savefig("rmso_period2_vs_l.pdf", bbox_inches="tight")

    plot_rmso_l(["Na", "Mg", "Al", "Si", "P", "S", "Cl", "Ar"])
    plt.savefig("rmso_period3_vs_l.pdf", bbox_inches="tight")

    # missing: Si-, "S+",
    plot_rmso_l(["B+", "C-", "O+", "F-", "Al+", "Cl-"])
    plt.savefig("rmso_ions_vs_l.pdf", bbox_inches="tight")

    plot_rms_lf("O")
    plt.savefig("rms_lf_O.pdf")

    plot_rms_lf("N")
    plt.savefig("rms_lf_N.pdf")

    plot_rms_lf("C")
    plt.savefig("rms_lf_C.pdf")


if __name__ == "__main__":
    main()
