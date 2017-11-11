#!/usr/bin/env python3

from matplotlib import pyplot as plt
import matplotlib
import molsturm
import numpy as np
import os
import yaml


def plot_E_ground_state_vs_k(data, methods=["hf", "mp2"]):
    plt.close()
    plt.figure(figsize=(5.5, 3.5))

    for dataset in data:
        n = dataset[0]["n"]
        l = dataset[0]["l"]
        m = dataset[0]["m"]

        ks = np.array([d["k"] for d in dataset])
        sorti = np.argsort(ks)
        ks = ks[sorti]

        hfenes = np.array([d["energy_hf"] for d in dataset])
        mp2enes = np.array([d["energy_mp2"] for d in dataset])

        # Sort the dataset
        hfenes = hfenes[sorti]
        mp2enes = mp2enes[sorti]

        if "hf" in methods:
            p = plt.plot(ks, hfenes, "-",
                         label=r"$(" + str(n) + "," + str(l) +
                         "," + str(m) + ")$ " + r"$E_\text{HF}$")
            mp2color = p[0].get_color()

            min_idx = np.argmin(hfenes)
            plt.plot(ks[min_idx], hfenes[min_idx], "x", color=p[0].get_color())
        else:
            mp2color = None

        if "mp2" in methods:
            p = plt.plot(ks, mp2enes, "--",
                         label=r"$(" + str(n) + "," + str(l) +
                         "," + str(m) + ")$ " + r"$E_\text{MP2}$",
                         color=mp2color)
            min_idx = np.argmin(mp2enes)
            plt.plot(ks[min_idx], mp2enes[min_idx], "+",
                     color=p[0].get_color())

    plt.ylabel("Energy in Hartree")
    plt.xlabel(r"Coulomb-Sturmian exponent $k_\text{exp}$")
    plt.legend()


def plot_hfterm_vs_k(data, terms=["e-e", "e-n", "kin"]):
    plt.close()
    plt.figure(figsize=(5.5, 3.5))

    for dataset in data:
        n = dataset[0]["n"]
        l = dataset[0]["l"]
        m = dataset[0]["m"]

        ks = np.array([d["k"] for d in dataset])
        sorti = np.argsort(ks)
        ks = ks[sorti]

        color = None
        for term in terms:
            if term == "e-e":
                eCoul = np.array([d["energy_coulomb"] for d in dataset])
                eExch = np.array([d["energy_exchange"] for d in dataset])
                enes = eCoul + eExch
                label = r"$E_\text{e2e}$"
                line = "-"
            elif term == "e-n":
                enes = np.array([d["energy_nuclear_attraction"]
                                 for d in dataset])
                label = r"$E_\text{nuc}$"
                line = "--"
            elif term == "kin":
                enes = np.array([d["energy_kinetic"] for d in dataset])
                label = r"$E_\text{kin}$"
                line = ":"

            # Sort the energies:
            enes = enes[sorti]

            p = plt.plot(ks, enes, line,
                         label=r"$(" + str(n) + "," + str(l) +
                         "," + str(m) + ")$ " + label, color=color)
            color = p[0].get_color()

    plt.ylabel("Energy in Hartree")
    plt.xlabel(r"Coulomb-Sturmian exponent $k_\text{exp}$")
    plt.legend(ncol=2)


def plot_orben_vs_k(dataset, orbidxs=[0, 1, 2, 3, 4, 5],
                    orblabels=["1s", "2s", "2p", "2p", "2p", "3s"], beta=False):
    plt.close()
    plt.figure(figsize=(5.5, 3.5))

    ks = np.array([d["k"] for d in dataset])
    sorti = np.argsort(ks)
    ks = ks[sorti]

    orbidxs = np.array(orbidxs)
    if beta:
        orbidxs = orbidxs + len(dataset[0]["orben"]) // 2
    orbens = np.array([d["orben"][orbidxs] for d in dataset])
    orbens = orbens[sorti, :]

    for i in range(len(orbidxs)):
        p = plt.plot(ks, orbens[:, i], label=orblabels[i])
        min_idx = np.argmin(orbens[:, i])
        plt.plot(ks[min_idx], orbens[min_idx, i], "x",
                 color=p[0].get_color())

    plt.ylabel(r"Hartree-Fock orbital energy $\varepsilon_i / E_\text{H}$")
    plt.xlabel(r"Exponent $k_\text{exp}$")
    plt.legend()


def setup():
    # Setup matplotlib
    tex_premable = [
        r"\usepackage[utf8x]{inputenc}",
        r"\usepackage[T1]{fontenc}",
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


def load_data():
    data = []
    dir_of_this_file = os.path.dirname(__file__)
    for n, l, m in [(4, 2, 2), (5, 2, 2), (6, 2, 2)]:
        datafile = dir_of_this_file + "/C_n" + str(n) + \
            "-l" + str(l) + "-m" + str(m) + "-summary.yaml"

        molsturm.yaml_utils.install_constructors()
        with open(datafile, "r") as f:
            data.append(yaml.safe_load(f))
    return data


def main():
    setup()
    data = load_data()

    plot_E_ground_state_vs_k(data)
    plt.ylim([-38, -34])
    plt.savefig("C_ene_gs_vs_k.pdf", bbox_inches="tight")

    plot_hfterm_vs_k(data)
    plt.savefig("C_hfterms_vs_k.pdf", bbox_inches="tight")

    plot_orben_vs_k(data[2])
    plt.savefig("C_orben_622_vs_k.pdf", bbox_inches="tight")


if __name__ == "__main__":
    main()
