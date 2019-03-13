#!/usr/bin/env python3

import matplotlib
from matplotlib import pyplot as plt
import numpy as np


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


def get_cells():
    # labels at cell boundaries
    # position of grid cell boundary
    cells = {
        0: r"$a = x_0$",
        10: r"$x_1$",
        21: r"$x_{j-1}$",
        29: r"$x_j$",
        52: r"$x_{j+1}$",
        69: r"$x_{j+2}$",
        85: r"$x_{N_\text{cell}-1}$",
        100: r"$x_{N_\text{cell}} = b$",
    }
    x = np.linspace(min(cells.keys()), max(cells.keys()), 100*100)
    return x, cells


def make_cell_label(cells, i):
    lals = ["", "$c_0$", "$\cdots$", "$c_{j-1}$", "$c_j$", "$c_{j+1}$",
            "$\cdots$", r"$c_{N_\text{cell}}$"]
    return lals[i]


def plot_grid(cells):
    keys = sorted(list(cells.keys()))
    for i, k in enumerate(keys):
        if i > 0:
            half = keys[i-1] + (keys[i] - keys[i-1]) / 2
            plt.text(half, 0.9, make_cell_label(cells, i),
                     ha="center", va="center",
                     color="DarkGrey", fontsize=8)
        plt.axvline(x=k, color="DarkGray", linewidth=0.4, linestyle="--")


def plot_ticks(ax, cells, subticks=0):
    keys = sorted(list(cells.keys()))
    keys_minor = []

    for i, k in enumerate(keys):
        if i > 0:
            extra = np.linspace(keys[i-1], keys[i], subticks + 1, endpoint=False)
            keys_minor += extra[1:].tolist()
    plt.xticks(list(cells.keys()), list(cells.values()))
    ax.set_xticks(keys_minor, minor=True)
    ax.set_xticklabels(len(keys_minor) * [""], minor=True)
    plt.yticks([0.0, 0.5, 1.0])


def linear_element(cells, n, x):
    keys = sorted(list(cells.keys()))
    center = keys[n]
    lower = keys[n-1] if n > 0 else keys[0]
    upper = keys[n+1] if n < len(cells) - 1 else keys[-1]

    ret = np.zeros_like(x)
    lpart = (x >= lower) & (x <= center)
    rpart = (x <= upper) & (x > center)

    ret[lpart] = (x[lpart] - lower) / (center - lower)
    ret[rpart] = (upper - x[rpart]) / (upper - center)
    return ret


def quadratic_element(cells, n, k, x):
    keys = sorted(list(cells.keys()))

    ret = np.zeros_like(x)
    if k == 2:
        center = keys[n]
        lower = keys[n-1] if n > 0 else keys[0]
        upper = keys[n+1] if n < len(cells) - 1 else keys[-1]

        l_middle = lower + (center - lower) / 2
        r_middle = center + (upper - center) / 2

        lpart = (x >= lower) & (x <= center)
        rpart = (x <= upper) & (x > center)

        ret[lpart] = (x[lpart] - lower) * (x[lpart] - l_middle)
        ret[lpart] = ret[lpart] / (center - lower) / (center - l_middle)
        ret[rpart] = (x[rpart] - upper) * (x[rpart] - r_middle)
        ret[rpart] = ret[rpart] / (center - upper) / (center - r_middle)
    elif k == 1:
        lower = keys[n]
        upper = keys[n + 1]
        center = lower + (upper - lower) / 2

        part = (x >= lower) & (x <= upper)
        ret[part] = (x[part] - upper) * (x[part] - lower)
        ret[part] = ret[part] / (center - upper) / (center - lower)

    return ret


def plot_linear_grid():
    plt.close()
    fig = plt.figure(figsize=(5.5, 1.5))
    ax = fig.add_subplot(111)

    x, cells = get_cells()
    plot_grid(cells)

    plt.plot(x, linear_element(cells, 3, x))
    plt.plot(x, linear_element(cells, 4, x))
    plt.plot(x, linear_element(cells, len(cells) - 1, x))

    plot_ticks(ax, cells)


def plot_quadratic_grid():
    plt.close()
    fig = plt.figure(figsize=(5.5, 1.5))
    ax = fig.add_subplot(111)

    x, cells = get_cells()
    plot_grid(cells)

    plt.plot(x, quadratic_element(cells, 3, 2, x))
    plt.plot(x, quadratic_element(cells, 4, 1, x))
    plt.plot(x, quadratic_element(cells, len(cells) - 1, 2, x))

    plot_ticks(ax, cells, subticks=1)


def main():
    setup()
    plot_linear_grid()
    plt.savefig("fe_grid_linear.pdf", bbox_inches="tight")

    plot_quadratic_grid()
    plt.savefig("fe_grid_quadratic.pdf", bbox_inches="tight")


if __name__ == "__main__":
    main()
