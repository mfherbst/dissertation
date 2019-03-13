#!/usr/bin/env python3
from matplotlib import pyplot as plt
import matplotlib
import numpy as np
import os
import yaml


def load_data():
    dir_of_this_file = os.path.dirname(__file__)
    with open(dir_of_this_file + "/data.yaml", "r") as f:
        data = yaml.safe_load(f)
    years = np.array([d[0] for d in data])
    mems = np.array([d[1] for d in data])
    cpus = np.array([d[2] for d in data])
    return {"years": years, "mems": mems, "cpus": cpus, }


def plot_mem_cpu(data):
    plt.close()
    plt.figure(figsize=(5.5, 3.5))

    years = data["years"]
    mems = data["mems"]
    cpus = data["cpus"]

    plt.semilogy(years, cpus, "xC0", label="CPU clock speed")
    plt.semilogy(years, mems, "xC1", label="Memory bus speed")
    plt.ylabel("Scale-up relative to 1980")

    color = "C3"
    plt.arrow(x=2010, y=5015, dx=0, dy=7000,
              color=color,
              head_width=0.3, head_length=2000)
    plt.arrow(x=2010, y=5015, dx=0, dy=-5000,
              color=color,
              head_width=0.3, head_length=2.5)

    tpos = (2001.5, 280)
    plt.text(tpos[0] + 1.4, 2 * tpos[1], "Processor vs.", color=color)
    plt.text(tpos[0] + 2.5, tpos[1], "Memory", color=color)
    plt.text(tpos[0] + 0.0, tpos[1] // 2, "performance gap", color=color)
    plt.legend()


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


if __name__ == "__main__":
    setup()
    data = load_data()
    plot_mem_cpu(data)
    plt.savefig("mem_cpu_years.pdf", bbox_inches="tight")
