#!/usr/bin/env python3

from matplotlib import pyplot as plt
import matplotlib
import numpy as np
import os
import yaml


dir_of_this_file = os.path.dirname(__file__)


def plot_EHF_vs_shell(systems):
    plt.close()
    fig = plt.figure(figsize=(5.5, 3.5))
    ax1 = fig.add_subplot(111)
    ax2 = ax1.twiny()

    litfile = dir_of_this_file + "/HF_literature.yaml"
    with open(litfile, "r") as f:
        literature = yaml.safe_load(f)

    for atom in systems:
        with open(dir_of_this_file + "/" + atom + "_results.yaml", "r") as f:
            results = yaml.safe_load(f)

        nbas = np.array([res["n_bas"] for res in results])
        hfs = np.array([res["ene"] for res in results])

        if atom in ["Li", "B", "C", "N", "O", "F"]:
            lit = literature["unrestricted"][atom]["value"]
        else:
            lit = literature["restricted"][atom]["value"]
        ax1.semilogy(nbas, hfs - lit, "x-", label=atom)

    ax1.set_ylabel(r"Error $\Delta E_\text{HF}$")
    ax1.set_xlabel(r"Number of basis functions $N_\text{bas}$")
    ax1.legend()

    # Setup second axis
    with open(dir_of_this_file + "/Be_results.yaml", "r") as f:
        results = yaml.safe_load(f)
    ns = np.array([res["n"] for res in results])
    nbas = np.array([res["n_bas"] for res in results])

    ax2.set_xlim(ax1.get_xlim())
    ax2.set_xticks(nbas)
    ax2.set_xticklabels([str(v) for v in ns])
    ax2.set_xlabel(r"Number of shells $n$")


def setup():
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


def main():
    setup()
    systems = ["Li", "Be", "B", "C", "N", "O", "F", "Ne"]

    plot_EHF_vs_shell(systems)
    plt.savefig("Delta_EHF_vs_shell.pdf", bbox_inches="tight")


if __name__ == "__main__":
    main()
