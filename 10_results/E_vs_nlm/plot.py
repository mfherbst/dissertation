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
        return list(yaml.safe_load(f).values())


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


def plot_orben_vs_bas(vals, alphas=True, selection=None):
    plt.close()
    plt.figure(figsize=(4.4, 2.8))

    if selection is None:
        selection = {i: str(i) for i in range(12)}
    orbenkey = "orben_a" if alphas else "orben_b"

    vals = sorted(vals, key=lambda x: (x["n_max"], x["l_max"]))
    ns = np.array([v["n_max"] for v in vals])
    orbens = np.array([v[orbenkey][:20] for v in vals])
    diff = np.diff(orbens, axis=0)
    error = np.abs(diff / orbens[1:, :])

    error = error.transpose()
    for i, v in enumerate(error):
        if i not in selection:
            continue
        plt.semilogy(ns[:-1], v, "x-", label=selection[i])

    plt.ylabel("relative difference of orbital energies")
    plt.legend()


def plot_EHF_vs_bas(values, full_O=False, ignore_regions=[]):
    plt.close()

    if full_O:
        plt.figure(figsize=(5.5, 2.9))
    else:
        plt.figure(figsize=(5.5, 3.5))

    litfile = dir_of_this_file + "/HF_reference.yaml"
    with open(litfile, "r") as f:
        literature = yaml.safe_load(f)

    colors = {}
    for vals in values:
        atom = vals[0]["atom"]
        vals = sorted(vals, key=lambda x: (x["n_max"], x["l_max"]))

        n_bas = np.array([v["n_bas"] for v in vals])
        ns = np.array([v["n_max"] for v in vals])
        hfs = np.array([v["energy_ground_state"] for v in vals])

        # Get literature for RHF (closed-shell) or UHF (open-shell)
        if atom in ["N", "O", "P", "C"]:
            litval = literature["unrestricted"][atom]["value"]
        else:
            litval = literature["restricted"][atom]["value"]

        if atom in ["N", "C"]:
            ls = [(1, 1, "-"), (2, 2, "--")]
        elif atom == "O":
            if full_O:
                ls = [(1, 1, "-"), (2, 2, "-"), (3, 3, "-")]
                # TODO OPTIONAL
                # ls = [(1, 1, "-"), (2, 2, "-"), (3, 1, "-"),
                #       (3, 2, "-"), (3, 3, "-")]
            else:
                ls = [(1, 1, "-"), (2, 2, "--")]
        elif atom == "Be":
            ls = [(1, 1, "-"), (0, 0, ":")]
        else:
            ls = [(1, 1, "-")]

        for l, m, style in ls:
            if not full_O:
                color = colors.get(atom)
            else:
                color = None

            mask = np.array([v["l_max"] == l and v["m_max"] == m
                             for v in vals])
            label = atom + r" ($n_\text{max}$," + str(l) + "," + str(m) + ") "

            hfdiff = (hfs - litval) / abs(litval)
            p = plt.semilogy(n_bas[mask], hfdiff[mask], "x" + style,
                             label=label, color=color)

            colors[atom] = p[0].get_color()

            # Plot value of n at first and last point
            for i, position in [(0, "above"), (-1, "right")]:
                xshift = 1.5 if position == "right" else -0.5
                yfac = 1.15 if full_O else 1.5
                yshift = yfac if position == "above" else 1
                x = n_bas[mask][i] + xshift
                y = hfdiff[mask][i] * yshift

                noplot = any(
                    np.abs(x - region[0]) < 0.4 and
                    np.abs(np.log(np.abs(y/region[1]))) < 0.4
                    for region in ignore_regions
                )
                if noplot:
                    continue

                plt.text(x, y, str(ns[mask][i]),
                         color=p[i].get_color(), size=8)

    plt.xlabel(r"Number of basis functions $N_\text{bas}$")
    plt.ylabel(r"Relative error in $E_\text{HF}$")
    plt.legend(ncol=2)


def main():
    setup()
    vals_be = load_data("Be")
    vals_n = load_data("N")
    vals_p = load_data("P")
    vals_o = load_data("O")
    vals_c = load_data("C")

    #
    # Plot orben convergence
    #
    orben_plot_n = [v for v in vals_n if v["l_max"] == 2]
    selection = {0: "1s", 1: "2s", 3: "2p", 5: "3s", 7: "3p", 11: "3d"}
    plot_orben_vs_bas(orben_plot_n, selection=selection)
    plt.xlabel(r"Coulomb Sturmian basis $(n_\text{max},2,2)$")
    plt.savefig("orben_vs_nlm_N.pdf", bbox_inches="tight")

    #
    # Plot energy convergence
    #
    ignore_regions = [(12.5, 0.011), (20.5, 1.4e-3), (40.5, 1.31e-3),
                      (46.5, 1e-4), (46.5, 2e-4)]

    plot_EHF_vs_bas([vals_be, vals_n, vals_p, vals_o, vals_c],
                    ignore_regions=ignore_regions)
    plt.text(12.5, 0.013, "4", size=8, color="tab:orange")
    plt.text(20.5, 1.4e-3, "6", size=8, color="tab:red")
    plt.text(40.5, 1.31e-3, "6", size=8, color="tab:red")
    plt.text(46.3, 1.0e-4, "12", size=8, color="tab:purple")

    plt.ylim([None, 3])
    plt.savefig("ehf_vs_nlm.pdf", bbox_inches="tight")

    plot_EHF_vs_bas([vals_o], full_O=True)
    plt.ylim([None, 1.4e-3])
    plt.savefig("ehf_vs_nlm_O.pdf", bbox_inches="tight")


if __name__ == "__main__":
    main()
