#!/usr/bin/env python3

from matplotlib import pyplot as plt
import molsturm
import numpy as np
import yaml
import os
import matplotlib


def load_data():
    dir_of_this_file = os.path.dirname(__file__)
    molsturm.yaml_utils.install_constructors()

    with open(dir_of_this_file + "/Be_fci_summary.yaml", "r") as f:
        data = yaml.safe_load(f)

    with open(dir_of_this_file + "/Be_fci_high_accuracy.yaml", "r") as f:
        data.append(yaml.safe_load(f))
    return data


def setup():
    # Setup matplotlib
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


def plot_cc_vs_nbas(data, reference):
    plt.close()
    fig = plt.figure(figsize=(4.8, 2.8))
    ax1 = fig.add_subplot(111)
    ax2 = ax1.twiny()

    ref_fci = reference["fci"][0]
    ref_hf = reference["hf"]
    ref_cc = ref_fci - ref_hf
    data = sorted(data, key=lambda d: d["n_bas"])

    hf = np.array([d["hf"] for d in data])
    mp2 = np.array([d["mp2"] for d in data])
    fci = np.array([d["fci"][0] for d in data])
    n_bas = np.array([d["n_bas"] for d in data])
    nlms = [(d["n_max"], d["l_max"], d["m_max"]) for d in data]
    relmp2cc = (mp2 - hf) / ref_cc
    relfcicc = (fci - hf) / ref_cc

    ax1.plot(n_bas, relmp2cc, "x:", label="MP2 correlation", linewidth=0.2)
    ax1.plot(n_bas, relfcicc, "x:", label="FCI correlation", linewidth=0.2)
    ax1.legend()
    ax1.set_xlabel(r"Number of basis functions $N_\text{bas}$")
    ax1.set_ylabel("Fraction of correlation energy")

    ax2.set_xlim(ax1.get_xlim())
    ax2.set_xticks(n_bas)
    ax2.set_xticklabels([
        r"$({0:},{1:},{2:})$".format(*nlm) for nlm in nlms
    ], fontdict={"fontsize": 7})
    ax2.set_xlabel(r"Coulomb-Sturmian basis set "
                   r"$(n_\text{max},l_\text{max},m_\text{max})$")


def main():
    setup()

    data = load_data()
    reference = [d for d in data if d["n_max"] == 10][0]

    data = [d for d in data if d["n_max"] == 6]
    plot_cc_vs_nbas(data, reference)
    plt.savefig("Be_fci_cc_vs_nbas.pdf", bbox_inches="tight")


if __name__ == "__main__":
    main()
