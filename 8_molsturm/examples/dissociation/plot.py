#!/usr/bin/env python3
from matplotlib import pyplot as plt
import h2_dissociation as lib
import matplotlib
import numpy as np
import os
import yaml


def load_data():
    dir_of_this_file = os.path.dirname(__file__)
    with open(dir_of_this_file + "/H2_UMP2_dissociation.yaml", "r") as f:
        data = yaml.safe_load(f)
    return np.array(data["distances"]), np.array(data["energies"])


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


if __name__ == "__main__":
    setup()
    plt.figure(figsize=(5.5, 3.5))
    lib.plot_morse_fit(*load_data())
    plt.savefig("h2_dissociation.pdf", bbox_inches="tight")
