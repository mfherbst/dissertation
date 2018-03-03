#!/usr/bin/env python3

from matplotlib import pyplot as plt
import numpy as np
import yaml
import os
import matplotlib


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
    dir_of_this_file = os.path.dirname(__file__)
    with open(dir_of_this_file + "/data_adc2.yaml", "r") as f:
        return yaml.safe_load(f)


def load_literature():
    dir_of_this_file = os.path.dirname(__file__)
    with open(dir_of_this_file + "/literature.yaml", "r") as f:
        lit = yaml.safe_load(f)
    # Convert Rydberg to Hartree
    return {k: v / 2 for k, v in lit.items()}


def load_ccpvtz():
    dir_of_this_file = os.path.dirname(__file__)
    with open(dir_of_this_file + "/ccpdtz.yaml", "r") as f:
        return yaml.safe_load(f)


def plot_error_vs_n(data,
                    selection=["s2s2p", "s2s3s", "s2s3p", "s2s4s", "s2s4p"]):
    plt.close()
    plt.figure(figsize=(5.5, 3.5))

    ns = np.array([d["nmax"] for d in data])
    ground_state = np.array([d["ground_state"] for d in data])

    ex_states = {
        k: np.array([
            np.NaN if d["selected"][k] == "None"
            else d["singlets"][d["selected"][k]]
            for d in data
        ])
        for k in selection
    }

    excitation_energies = {
        k: ex_states[k] - ground_state
        for k in selection
    }

    ccpvtz_raw = load_ccpvtz()
    ccpvtz = {}
    for k in selection:
        if ccpvtz_raw["selected"][k] == "None":
            ccpvtz[k] = np.NaN
        else:
            ccpvtz[k] = ccpvtz_raw["singlets"][ccpvtz_raw["selected"][k]]
            ccpvtz[k] -= ccpvtz_raw["ground_state"]

    literature = load_literature()
    for k in selection:
        label = "$" + k[1:] + "$"
        p = plt.plot(ns, excitation_energies[k], "x-", label=label)
        plt.plot([11], ccpvtz[k], "+", color=p[0].get_color())
        plt.plot([12], literature[k], "+", color=p[0].get_color())

    xticks = ["$({},1,1)$".format(n) for n in ns] + ["cc-pVTZ", "Exp."]
    plt.xticks(range(ns[0], 13), xticks, size="small")
    # plt.xlabel(r"$n_\text{max}$")
    plt.ylabel(r"Excitation energy in Hartree")
    plt.ylim([0, None])
    plt.legend()


def main():
    setup()
    data = load_data()

    plot_error_vs_n(data)
    plt.savefig("be_adc2_vs_n.pdf", bbox_inches="tight")


if __name__ == "__main__":
    main()
