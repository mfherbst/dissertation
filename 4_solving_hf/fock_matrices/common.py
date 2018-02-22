from matplotlib import pyplot as plt
import gint
import matplotlib
import matplotlib.gridspec as gridspec
from matplotlib.colors import LogNorm
import numpy as np


# Other potentially sensible vrange values
# (-12, 2), (-8, 2)
def plot_mtcs(mtcs, middle_labels=True, vrange=(-8, 2)):
    plt.close()

    cmap = matplotlib.cm.YlOrRd
    cmap.set_bad("white", 1.)
    cmap.set_over(cmap(cmap.N), 1.)
    cmap.set_under("white", 1.)
    norm = LogNorm(vmin=10**min(vrange), vmax=10**max(vrange))

    ticks = []
    for i in range(min(vrange), max(vrange)):
        ticks += list(np.linspace(10**i, 10*10**i, 5, endpoint=False))
    ticks += [10**max(vrange)]

    n_mtx = len(mtcs)
    if n_mtx == 1:
        size = 3
        adjust_right = 0.90
        cbar_axis = [0.92, 0.23, 0.03, 0.55]
    elif n_mtx == 2:
        size = 2.6
        adjust_right = 0.91
        cbar_axis = [0.93, 0.23, 0.015, 0.55]
    else:
        size = 2.4
        adjust_right = 0.91
        cbar_axis = [0.93, 0.23, 0.01, 0.55]

    fig = plt.figure(figsize=((size + 0.1) * n_mtx, size))
    gs = gridspec.GridSpec(1, n_mtx)

    if not middle_labels:
        gs.update(wspace=0.1)

    for i, mtx in enumerate(mtcs):
        ax = fig.add_subplot(gs[i])
        img = ax.matshow(np.abs(mtx), cmap=cmap, norm=norm)

        # Adjust ticks if requested
        if not middle_labels and i > 0:
            n_ticks = len(ax.get_yticklabels())
            ax.set_yticklabels(n_ticks * [""])
        if mtx.shape[0] > 1000:
            newlabels = [
                str(int(x)) if i == 1 or i % 2 == 0 else ""
                for i, x in enumerate(ax.get_xticks())
            ]
            ax.set_xticklabels(newlabels)

    fig.subplots_adjust(right=adjust_right)
    cbar_ax = fig.add_axes(cbar_axis)
    fig.colorbar(img, cax=cbar_ax, ticks=ticks)
    plt.draw()


def mtx_properties(mtx):
    props = dict()
    props["quadratic"] = bool(mtx.shape[0] == mtx.shape[1])
    props["symmetric"] = bool(np.max(np.abs(mtx - mtx.transpose())) < 1e-12)
    props["n_rows"] = mtx.shape[0]

    # Diagonal dominance:
    rowsum = np.sum(np.abs(mtx), axis=0)
    diff = rowsum - 2*np.abs(mtx.diagonal())
    props["n_diagdominant"] = np.where(diff <= 0)[0].size

    return props


def sturmian_change_order(basis, permutation):
    argsort = sorted(range(len(basis.functions)),
                     key=lambda i: permutation(basis.functions.__getitem__(i)))

    lenn = len(argsort)
    trans = np.zeros((lenn, lenn))
    for i, j in enumerate(argsort):
        trans[i, j] = 1
    return trans


def sturmian_nlm_to_mln_order(basis):
    def to_mln(nlm):
        return nlm[2], nlm[1], nlm[0]
    return sturmian_change_order(basis, to_mln)


def sturmian_nlm_to_lmn_order(basis):
    def to_lmn(nlm):
        return nlm[1], nlm[2], nlm[0]
    return sturmian_change_order(basis, to_lmn)


def plot_states(states):
    props = []
    mtcs = []
    for state in states:
        bas = state.input_parameters.basis
        n_orbs_alpha = state["n_orbs_alpha"]
        fa_bb = state["fock_bb"][:n_orbs_alpha, :n_orbs_alpha]

        order = "cartesian standard"
        if isinstance(bas, gint.sturmian.atomic.Basis):
            assert bas.order == "nlm"
            order = "mln"
            # order = "lmn"
            trans = globals()["sturmian_nlm_to_" + order + "_order"](bas)
            fa_bb = trans @ fa_bb @ trans.transpose()
        mtcs.append(fa_bb)

        props.append(mtx_properties(fa_bb))
        props[-1]["final_error_norm"] = state["final_error_norm"]
        props[-1]["order"] = order
    plot_mtcs(mtcs)
    return props


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
