#!/usr/bin/env python3

import molsturm
import yaml
from matplotlib import pyplot as plt
import numpy as np
import matplotlib
import os


def load_data():
    molsturm.yaml_utils.install_constructors()
    dir_of_this_file = os.path.dirname(__file__)
    with open(dir_of_this_file + "/summary.yaml", "r") as f:
        return yaml.safe_load(f)


def plot_hf(data, orben=False):
    ks = np.array([d["k"] for d in data])
    hfs = np.array([d["energy_hf"] for d in data])

    p = plt.plot(ks, hfs, label="HF")
    min_idx = np.argmin(hfs)
    plt.plot(ks[min_idx], hfs[min_idx], "x", color=p[0].get_color())

    if orben:
        label = {0: "1s", 1: "2s", 2: "2p", 5: "3s", 6: "3p"}
        for i in [0, 1, 2, 5, 6]:
            orben = np.array([d["orben"][i] for d in data])
            plt.plot(ks, orben, label="HF " + label[i] + " energy")


def plot_mp2(data):
    ks = np.array([d["k"] for d in data])
    mp2s = np.array([d["energy_mp2"] for d in data])

    p = plt.plot(ks, mp2s, label="MP2")
    min_idx = np.argmin(mp2s)
    plt.plot(ks[min_idx], mp2s[min_idx], "x", color=p[0].get_color())


def plot_fci(data):
    ks = np.array([d["k"] for d in data])
    s1 = np.array([d["states"][0]["energy"] for d in data])
    t1 = np.array([d["states"][1]["energy"] for d in data])

    # TODO OPTIONAL
    # p = plt.plot(ks, s1, label="FCI S1")
    p = plt.plot(ks, s1, label="FCI")
    min_idx = np.argmin(s1)
    plt.plot(ks[min_idx], s1[min_idx], "x", color=p[0].get_color())

    # TODO OPTIONAL
    # p = plt.plot(ks, t1, label="FCI T1")
    # min_idx = np.argmin(t1)
    # plt.plot(ks[min_idx], t1[min_idx], "x", color=p[0].get_color())


def plot_methods_vs_k(data):
    plt.figure(figsize=(5.5, 3.5))

    plot_hf(data)
    plot_mp2(data)
    plot_fci(data)

    plt.xlabel(r"Coulomb-Sturmian exponent $k_\text{exp}$")
    plt.ylabel("Energy in Hartree")
    plt.ylim([-14.75, -13.5])
    plt.xlim([1.0, 4.5])
    plt.legend()


def plot_hf_energies_vs_k(data):
    plt.figure(figsize=(5.5, 3.0))

    ks = np.array([d["k"] for d in data])
    Eatr = np.array([d["energy_nuclear_attraction"] for d in data])
    Ekin = np.array([d["energy_kinetic"] for d in data])
    Ecoul = np.array([d["energy_coulomb"] for d in data])
    Eexch = np.array([d["energy_exchange"] for d in data])

    plt.plot(ks, Eatr, "--", label="Nuclear attraction energy")
    plt.plot(ks, Ekin, ":", label="Electronic kinetic energy")
    plt.plot(ks, Ecoul + Eexch, "-", label="Electron-electron interaction energy")

    plt.xlabel(r"Coulomb-Sturmian exponent $k_\text{exp}$")
    plt.ylabel("Energy in Hartree")
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


def main():
    setup()
    data = load_data()

    plot_methods_vs_k(data)
    plt.savefig("Efci_vs_k.pdf", bbox_inches="tight")

    plot_hf_energies_vs_k(data)
    plt.savefig("EHF_terms_vs_k.pdf", bbox_inches="tight")


if __name__ == "__main__":
    main()
