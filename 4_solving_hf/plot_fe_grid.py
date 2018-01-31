#!/usr/bin/env python3

import matplotlib
from matplotlib import pyplot as plt
import numpy as np


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


def get_cells():
    # labels at cell boundaries
    # position of grid cell boundary
    return {
        0: r"$a = x_0$",
        10: r"",
        17: r"$x_{j-1}$",
        28: r"$x_j$",
        45: r"$x_{j+1}$",
        63: r"$x_{j+2}$",
        89: r"",
        100: r"$x_{\text{N}_\text{cell}} = b$",
    }


def linear_element(cells, n, x):
    keys = list(cells.keys())
    center = keys[n]
    lower = keys[n-1] if n > 0 else keys[0]
    upper = keys[n+1] if n < len(cells) - 1 else keys[-1]

    ret = np.zeros_like(x)
    lpart = (x >= lower) & (x <= center)
    rpart = (x <= upper) & (x > center)

    ret[lpart] = (x[lpart] - lower) / (center - lower)
    ret[rpart] = (upper - x[rpart]) / (upper - center)
    return ret


def plot_linear_grid():
    plt.close()
    plt.figure(figsize=(5.5, 1.5))

    cells = get_cells()
    x = np.linspace(min(cells.keys()), max(cells.keys()), 100*100)
    for k in cells.keys():
        plt.axvline(x=k, color="DarkGray", linewidth=0.4, linestyle="--")

    plt.plot(x, linear_element(cells, 3, x))
    plt.plot(x, linear_element(cells, 4, x))
    plt.plot(x, linear_element(cells, len(cells) - 1, x))
    plt.xticks(list(cells.keys()), list(cells.values()))


def quadratic_element(cells, n, k, x):
    keys = list(cells.keys())

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


def plot_quadratic_grid():
    plt.close()
    fig = plt.figure(figsize=(5.5, 1.5))
    ax = fig.add_subplot(111)

    cells = get_cells()
    x = np.linspace(min(cells.keys()), max(cells.keys()), 100*100)
    for k in cells.keys():
        plt.axvline(x=k, color="DarkGray", linewidth=0.4, linestyle="--")

    plt.plot(x, quadratic_element(cells, 3, 2, x))
    plt.plot(x, quadratic_element(cells, 4, 1, x))
    plt.plot(x, quadratic_element(cells, len(cells) - 1, 2, x))

    keys = list(cells.keys())
    keys_minor = []
    for i, k in enumerate(keys):
        if i > 0:
            keys_minor.append(keys[i-1] + (keys[i] - keys[i-1]) / 2)
    plt.xticks(keys, list(cells.values()))
    ax.set_xticks(keys_minor, minor=True)
    ax.set_xticklabels(len(keys_minor) * [""], minor=True)


def main():
    setup()
    plot_linear_grid()
    plt.savefig("fe_grid_linear.pdf", bbox_inches="tight")

    plot_quadratic_grid()
    plt.savefig("fe_grid_quadratic.pdf", bbox_inches="tight")


if __name__ == "__main__":
    main()
