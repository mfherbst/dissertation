#!/usr/bin/env python3

from matplotlib import pyplot as plt
import molsturm
import numpy as np
import yaml
import os
import matplotlib


dir_of_this_file = os.path.dirname(__file__)


def filename(atom):
    return dir_of_this_file + "/" + atom + "_plot_data.yaml"


def load_data(atom):
    if not os.path.isfile(filename(atom)):
        raise ValueError("Atom not computed: " + atom)

    molsturm.yaml_utils.install_constructors()
    with open(filename(atom), "r") as f:
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


def plot_orben_vs_bas(vals, n_alpha=12, n_beta=0, lmax=1):
    plt.close()
    plt.figure(figsize=(5.5, 3.5))

    atom = vals["7_1_1"]["atom"]
    vals = sorted(vals.values(), key=lambda x: (x["n_max"], x["l_max"]))
    ns = np.array([v["n_max"] for v in vals if v["l_max"] == lmax])
    alphas = np.array([v["orben_a"][:n_alpha] for v in vals
                       if v["l_max"] == lmax])
    betas = np.array([v["orben_b"][:n_beta] for v in vals
                      if v["l_max"] == lmax])

    alphas = alphas.transpose()
    betas = betas.transpose()

    for i, v in enumerate(alphas):
        plt.plot(ns, v, label=str(i) + "a " + atom)

    for i, v in enumerate(betas):
        plt.plot(ns, v, label=str(i) + "b " + atom)

    plt.xlabel("Sturmian basis $(n,1,1)$")
    plt.ylabel("$i$th orbital energy")

    plt.legend()


def plot_EHF_vs_bas(values):
    plt.close()
    plt.figure(figsize=(5.5, 3.5))

    litfile = dir_of_this_file + "/HF_reference.yaml"
    with open(litfile, "r") as f:
        literature = yaml.safe_load(f)

    for vals in values:
        atom = vals["7_1_1"]["atom"]
        vals = sorted(vals.values(), key=lambda x: (x["n_max"], x["l_max"]))

        n_bas = np.array([
            molsturm.construct_basis("sturmian/atomic", atom, k_exp=1.0,
                                     n_max=v["n_max"], l_max=v["l_max"],
                                     m_max=v["m_max"]).size
            for v in vals
        ])
        ns = np.array([v["n_max"] for v in vals])
        hfs = np.array([v["energy_ground_state"] for v in vals])

        # Get literature for RHF (closed-shell) or UHF (open-shell)
        if atom in ["N", "O", "P", "C"]:
            litval = literature["unrestricted"][atom]["value"]
            kind = "UHF"
        else:
            litval = literature["restricted"][atom]["value"]
            kind = "RHF"

        if atom in ["N", "C"]:
            ls = [(1, 1), (2, 2)]
        elif atom == "O":
            ls = [(1, 1), (2, 2), (3, 3), (3, 2), (3, 1)]
        elif atom == "Be":
            ls = [(1, 1), (0, 0)]
        else:
            ls = [(1, 1)]

        for l, m in ls:
            mask = np.array([v["l_max"] == l and v["m_max"] == m
                             for v in vals])
            label = atom + " (n," + str(l) + "," + str(m) + ") " + kind

            hfdiff = (hfs - litval) / abs(litval)
            p = plt.semilogy(n_bas[mask], hfdiff[mask], "x-",
                             label=label)

            # Plot value of n at first and last point
            for i, position in [(0, "left"), (-1, "right")]:
                shift = -3 if position == "left" else 1
                plt.text(n_bas[mask][i] + shift, hfdiff[mask][i],
                         str(ns[mask][i]),
                         color=p[i].get_color(), size=8)

    plt.xlabel(r"Number of basis functions $N_\text{bas}$")
    plt.ylabel(r"relative error in $E_\text{HF}$ compared to reference "
               r"value in $E_\text{H}$")

    plt.legend(ncol=2)


def main():
    setup()
    vals_be = load_data("Be")
    vals_n = load_data("N")
    vals_p = load_data("P")
    vals_o = load_data("O")
    vals_c = load_data("C")

    # plot_orben_vs_bas(vals_be, lmax=1)
    # plt.savefig("orben_vs_nlm_Be.pdf", bbox_inches="tight")

    plot_orben_vs_bas(vals_n, lmax=2)
    plt.savefig("orben_vs_nlm_N.pdf", bbox_inches="tight")

    # plot_orben_vs_bas(vals_p, lmax=1)
    # plt.savefig("orben_vs_nlm_P.pdf", bbox_inches="tight")

    # plot_orben_vs_bas(vals_o, lmax=3)
    # plt.savefig("orben_vs_nlm_O.pdf", bbox_inches="tight")

    plot_EHF_vs_bas([vals_be, vals_n, vals_p, vals_o, vals_c])
    plt.savefig("ehf_vs_nlm.pdf", bbox_inches="tight")


if __name__ == "__main__":
    main()
