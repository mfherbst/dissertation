#!/usr/bin/env python3

from matplotlib import pyplot as plt
import matplotlib
import molsturm
import numpy as np
import os
import yaml
import rmsl
import collections


dir_of_this_file = os.path.dirname(__file__)
OrbitalSelection = collections.namedtuple("OrbitalSelection",
                                          ["indices", "labels"])


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


def plot_rms_lf_orbitals(atom, selection=None):
    if selection is None:
        selection = OrbitalSelection(list(range(10)),
                                     [str(i) for i in range(10)])

    plt.close()
    plt.figure(figsize=(5.5, 3.5))

    state = molsturm.load_hdf5(datafile(atom))
    data = rmsl.compute_rms_qf(state)
    ls = np.arange(0, data[:, 0].size)
    for i, f in enumerate(selection.indices):
        plt.semilogy(ls, data[:, f], "x-", label=selection.labels[i])

    plt.ylim([1e-16, 1])
    plt.ylabel(r"root meam square coefficient value")
    plt.xlabel(r"Orbital angular momentum value $l$")
    plt.legend(loc=1)


def plot_rms_lf_overview(orbmaps):
    plt.close()
    plt.figure(figsize=(5.5, 3.5))

    lines = ["--", "-.", ":"]
    colors = []
    for a, (atom, orbmap) in enumerate(orbmaps.items()):
        state = molsturm.load_hdf5(datafile(atom))
        rms_lf = rmsl.compute_rms_qf(state)
        ls = np.arange(0, rms_lf[:, 0].size)

        for i, f, in enumerate(orbmap.indices):
            if len(colors) > i:
                color = colors[i]
            else:
                color = None

            p = plt.semilogy(ls, rms_lf[:, f], "x" + lines[a],
                             label=r"\ce{" + atom + "} " + orbmap.labels[i],
                             color=color)
            if len(colors) <= i:
                colors.append(p[0].get_color())


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

    selection = {
        "C": OrbitalSelection([1, 3, 6, 8], ["2s", "2p", "3d", "3d"]),
        "N": OrbitalSelection([1, 3, 6, 8], ["2s", "2p", "3d", "3d"]),
        "O": OrbitalSelection([1, 3, 8, 10], ["2s", "2p", "3d", "3d"]),
    }

    plot_rms_lf_orbitals("O", selection["O"])
    plt.savefig("rms_lf_O.pdf", bbox_inches="tight")

    plot_rms_lf_orbitals("N", selection["N"])
    plt.savefig("rms_lf_N.pdf", bbox_inches="tight")

    plot_rms_lf_orbitals("C", selection["C"])
    plt.savefig("rms_lf_C.pdf", bbox_inches="tight")

    # TODO This plot could condense the three above, but it is far too busy
    #      to be sensible
    # plot_rms_lf_overview(selection)
    # plt.savefig("rms_lf_CNO.pdf", bbox_inches="tight")


if __name__ == "__main__":
    main()
