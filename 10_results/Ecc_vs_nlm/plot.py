#!/usr/bin/env python3

from matplotlib import pyplot as plt
import molsturm
import numpy as np
import yaml
import os
import matplotlib
import gint


def load_data():
    dir_of_this_file = os.path.dirname(__file__)
    filename = dir_of_this_file + "/summary.yaml"

    molsturm.yaml_utils.install_constructors()
    with open(filename, "r") as f:
        return yaml.safe_load(f)


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


def build_atom_chunks(data):
    data = sorted(data, key=lambda d: (d["atnum"], d["n_bas"]))

    atoms = np.array([d["symbol"] for d in data])
    atoms = np.lib.arraysetops.unique(atoms)
    atoms = sorted(atoms, key=lambda at: gint.element.find(at).atom_number)

    ret = []
    for at in atoms:
        atdata = [d for d in data if d["symbol"] == at]
        nlm = [(d["n_max"], d["l_max"], d["m_max"]) for d in atdata]
        nbas = np.array([d["n_bas"] for d in atdata])
        Egs = np.array([d["mp2"] for d in atdata])
        Ecc = Egs - np.array([d["hf"] for d in atdata])

        ret.append({
            "symbol": at,
            "nlm": nlm,
            "n_bas": nbas,
            "Egs": Egs,
            "Ecc": Ecc,
        })
    return ret


def plot_y_vs_nbas(data, ykey):
    plt.close()
    fig = plt.figure(figsize=(4.8, 2.8))
    ax1 = fig.add_subplot(111)
    ax2 = ax1.twiny()

    all_nlms = set()
    for chk in build_atom_chunks(data):
        relative = chk[ykey] / chk[ykey][-1]
        ax1.plot(chk["n_bas"], relative, "x:", label=chk["symbol"],
                 linewidth=0.2)
        for nlm in chk["nlm"]:
            all_nlms.add(nlm)

    def find_nbas(nlm):
        for d in data:
            if (d["n_max"], d["l_max"], d["m_max"]) == nlm:
                return d["n_bas"]
        raise ValueError("Not found")

    all_nlms = list(all_nlms)
    all_nbas = [find_nbas(nlm) for nlm in all_nlms]

    ax1.legend()
    ax1.set_xlabel(r"Number of basis functions $N_\text{bas}$")

    ax2.set_xlim(ax1.get_xlim())
    ax2.set_xticks(all_nbas)
    ax2.set_xticklabels([
        r"$({0:},{1:},{2:})$".format(*nlm) for nlm in all_nlms
    ], fontdict={"fontsize": 7})
    ax2.set_xlabel(r"Coulomb-Sturmian basis set $(n,l,m)$")
    return ax1


def plot_total_vs_bas(data):
    ax = plot_y_vs_nbas(data, ykey="Egs")
    ax.set_ylabel(r"Fraction of total energy")


def plot_cc_vs_bas(data):
    ax = plot_y_vs_nbas(data, ykey="Ecc")
    ax.set_ylabel(r"Fraction of MP2 correlation energy")


def main():
    setup()
    data = load_data()

    easy_atnums = [3, 4, 7, 10, 11, 12, 15, 18]
    easy = [d for d in data if d["atnum"] in easy_atnums]
    hard = [d for d in data if d["atnum"] not in easy_atnums]

    plot_total_vs_bas(easy)
    plt.savefig("Etot_vs_bas_easy.pdf", bbox_inches="tight")

    plot_total_vs_bas(hard)
    plt.savefig("Etot_vs_bas_hard.pdf", bbox_inches="tight")

    plot_cc_vs_bas(hard)
    plt.savefig("Ecc_vs_bas_hard.pdf", bbox_inches="tight")

    plot_cc_vs_bas(easy)
    plt.savefig("Ecc_vs_bas_easy.pdf", bbox_inches="tight")


if __name__ == "__main__":
    main()
