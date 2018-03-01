#!/usr/bin/env python3

import numpy as np
import yaml
import matplotlib
from matplotlib import pyplot as plt
import scipy.optimize
import gint
import os


def Zeff_data():
    dir_of_this_file = os.path.dirname(__file__)
    with open(dir_of_this_file + "/Zeff.yaml", "r") as f:
        return yaml.safe_load(f)


def Zeffn_average(element, kind="Clementi"):
    """
    Compute the occupation-averaged Zeff/n* value
    for a particular element where n* is the n* value
    according to Slater 1930
    """
    names = ["1s", "2s", "2p", "3s", "3p", "4s"]
    nstar = [1, 2, 2, 3, 3, 3.7]
    maxelec = [2, 2, 6, 2, 6, 2]
    occupation = len(maxelec) * [0]

    elec = gint.element.find(element).atom_number
    for i in range(len(occupation)):
        occupation[i] = min(elec, maxelec[i])
        elec -= occupation[i]
        if elec == 0:
            break
    elec = gint.element.find(element).atom_number
    assert sum(occupation) == elec

    data = Zeff_data()
    eldata = data[element][kind]
    sum_Zeff = sum(occupation[i] * eldata.get(name, 0) / nstar[i]
                   for i, name in enumerate(names))
    return sum_Zeff / elec


def Zeff_HOMO(element, kind="Clementi"):
    data = Zeff_data()
    eldata = data[element][kind]
    homo = data[element]["HOMO"]
    return eldata[homo]


def load_kopts():
    dir_of_this_file = os.path.dirname(__file__)
    cachefile = dir_of_this_file + "/summary.yaml"
    with open(cachefile, "r") as f:
        return yaml.safe_load(f)


def period_of(at):
    if at < 3:
        return 1
    elif at < 11:
        return 2
    elif at < 19:
        return 3
    elif at < 37:
        return 4
    else:
        raise NotImplementedError()


def plot_zeffn_homo(data, kind="Clementi"):
    atnums = np.array([d["atom_number"] for d in data])
    HOMO_Zeffs = np.array([Zeff_HOMO(gint.element.by_atomic_number(at).symbol,
                                     kind=kind) / period_of(at)
                           for at in atnums])
    plt.plot(atnums, HOMO_Zeffs, "x", label=r"$\zeta_\text{Clementi}$ HO")


def plot_zeffn_average(data, kind="Clementi"):
    atnums = np.array([d["atom_number"] for d in data])
    avgs = np.array([Zeffn_average(gint.element.by_atomic_number(at).symbol,
                                   kind=kind)
                     for at in atnums])
    plt.plot(atnums, avgs, "x", label=r"$\zeta_\text{Clementi}$ average")


def plot_fit_kopt_vs_atnum(data):
    if len(data) == 0:
        return

    atnums = np.array([d["atom_number"] for d in data])
    ks = np.array([d["k_opt"] for d in data])
    n = data[0]["n_max"]
    l = data[0]["l_max"]
    m = data[0]["m_max"]

    p = plt.plot(atnums, ks, "x", label="(" + str(n) + "," + str(l) + "," +
                 str(m) + ") CS basis")

    if len(data) < 2:
        return

    def kopt_fun(x, a, b):
        return a*x + b
    popt, pcov = scipy.optimize.curve_fit(kopt_fun, atnums, ks)
    plt.plot(atnums, kopt_fun(atnums, *popt), color=p[0].get_color(),
             label="${0:8.3f}x + {1:8.3f}$".format(*popt))


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
    data = load_kopts()
    plt.figure(figsize=(5.5, 3.5))

    def is_period(d, p):
        return period_of(d["atom_number"]) == p

    def is_nlm(d, n, l, m):
        return (d["n_max"], d["l_max"], d["m_max"]) == (n, l, m)

    def is_charge(d, c):
        return d["charge"] == c

    data_period2 = [d for d in data
                    if is_period(d, 2) and is_nlm(d, 5, 2, 2) and
                    is_charge(d, 0)]
    data_period3 = [d for d in data
                    if is_period(d, 3) and is_nlm(d, 7, 2, 2) and
                    is_charge(d, 0)]
    data_period4 = [d for d in data
                    if is_period(d, 4) and is_nlm(d, 7, 2, 2) and
                    is_charge(d, 0)]

    plot_fit_kopt_vs_atnum(data_period2)
    plot_fit_kopt_vs_atnum(data_period3)
    plot_fit_kopt_vs_atnum(data_period4)
    plot_zeffn_homo(data_period2 + data_period3 + data_period4)
    plot_zeffn_average(data_period2 + data_period3 + data_period4)

    plt.ylim([0, 7])
    plt.legend(loc='upper left', fontsize=9)
    plt.xlabel(r"Atomic number")
    plt.savefig("kopt_vs_atnum.pdf", bbox_inches="tight")


if __name__ == "__main__":
    main()
