from matplotlib import pyplot as plt
import gint
import matplotlib
import numpy as np


# Other potentially sensible vrange values
# (-12, 2), (-8, 2)
def plot_mtcs(mtcs, vrange=(-7, 1)):
    plt.close()

    cmap = matplotlib.cm.YlOrRd
    cmap.set_bad("white", 1.)
    vrange = min(vrange), max(vrange)

    n_mtx = len(mtcs)
    size = 2.4
    if n_mtx < 3:
        size = 3

    fig = plt.figure(figsize=((size + 0.1) * n_mtx, size))
    for i, mtx in enumerate(mtcs):
        # Compute logabs, but enforce a numerical zero:
        mtxabs = np.abs(mtx)
        logabs = np.log10(mtxabs)

        ax = fig.add_subplot(1, n_mtx, i+1)
        # norm=common.LogNorm()
        img = ax.matshow(logabs, cmap=cmap, vmin=vrange[0], vmax=vrange[1])

    if n_mtx < 3:
        fig.subplots_adjust(right=0.90)
        cbar_ax = fig.add_axes([0.92, 0.23, 0.03, 0.55])
    else:
        fig.subplots_adjust(right=0.91)
        cbar_ax = fig.add_axes([0.93, 0.23, 0.01, 0.55])

    cbar = fig.colorbar(img, cax=cbar_ax)
    cbar.set_clim(vrange[0], vrange[1])

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
