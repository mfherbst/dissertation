#!/usr/bin/env python3

import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import random
from matplotlib import cm
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


def shapefun(order, index):
    INNER = {
        (1, 0): lambda x: x,
        (1, 1): lambda x: 1 - x,
        #
        (2, 0): lambda x: 2 * x * (x - 0.5),
        (2, 1): lambda x: 2 * (x - 1) * (x - 0.5),
        (2, 2): lambda x: -4 * x * (x - 1),
        #
        (3, 0): lambda x: 4.5 * x * (x - 1./3) * (x - 2./3),
        (3, 1): lambda x: -4.5 * (x - 1./3) * (x - 2./3) * (x - 1),
        (3, 2): lambda x: -13.5 * x * (x - 1./3) * (x - 1),
        (3, 3): lambda x: 13.5 * x * (x - 2./3) * (x - 1),
    }
    return INNER[(order, index)]


def plot_1d(ax, order, ylabels=True):
    x = np.linspace(0, 1, 10000)
    ax.plot(x, np.zeros_like(x), "--", color="DarkGray")
    for i in range(order+1):
        plt.plot(x, shapefun(order, i)(x))

    ticks = [0]
    labels = ["0"]
    for i in range(1, order):
        ticks.append(i / order)
        labels.append(str(i) + "/" + str(order))
    ticks.append(1)
    labels.append("1")

    ax.set_xticks(ticks)
    ax.set_xticklabels(labels)
    ax.set_ylim(-0.35, 1.1)

    if not ylabels:
        n_ticks = len(ax.get_yticklabels())
        ax.set_yticklabels(n_ticks * [""])


def plot_shape_1d():
    plt.close()
    fig = plt.figure(figsize=(6, 2))

    ax = fig.add_subplot(131)
    plot_1d(ax, 1)

    ax = fig.add_subplot(132)
    plot_1d(ax, 2, ylabels=False)

    ax = fig.add_subplot(133)
    plot_1d(ax, 3, ylabels=False)


def plot_2d(ax, order, xidx, yidx):
    x = y = np.linspace(0, 1, 100)
    X, Y = np.meshgrid(x, y)
    Z = shapefun(order, xidx)(X) * shapefun(order, yidx)(Y)
    ax.plot_surface(X, Y, Z, cmap=cm.RdBu, vmin=-0.3, vmax=1)
    ax.contour(X, Y, Z, 12, cmap=cm.RdBu, offset=-0.3, vmin=-0.3, vmax=1)

    ticks = [0]
    labels = ["0"]
    for i in range(1, order):
        ticks.append(i / order)
        labels.append(str(i) + "/" + str(order))
    ticks.append(1)
    labels.append("1")


    ax.view_init(10, 75)
    ax.set_yticks(ticks)
    ax.set_yticklabels(labels)
    ax.set_xticks(ticks)
    ax.set_xticklabels(labels)
    ax.set_zlim(-0.35, 1.1)

def plot_shape_2d():
    plt.close()
    fig = plt.figure(figsize=(6, 5))

    ax = fig.add_subplot(221, projection='3d')
    plot_2d(ax, 1, 1, 0)

    ax = fig.add_subplot(222, projection='3d')
    plot_2d(ax, 2, 2, 2)

    ax = fig.add_subplot(223, projection='3d')
    plot_2d(ax, 2, 1, 2)

    ax = fig.add_subplot(224, projection='3d')
    plot_2d(ax, 2, 2, 1)


def main():
    setup()

    plot_shape_1d()
    plt.savefig("shape_functions_1d.pdf", bbox_inches="tight")

    plot_shape_2d()
    plt.savefig("shape_functions_2d.pdf", bbox_inches="tight")


if __name__ == "__main__":
    main()
