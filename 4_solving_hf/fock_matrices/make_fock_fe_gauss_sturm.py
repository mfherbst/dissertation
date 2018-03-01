#!/usr/bin/env python3

from matplotlib import pyplot as plt
import common
import scipy.io
import molsturm


def main():
    common.setup()

    fe_mat = scipy.io.mmread("./Be.fe.stiff.mtx.gz").todense()
    sturmian = molsturm.load_hdf5("./Be_sturmian_511.hdf5")
    gaussian = molsturm.load_hdf5("./Be_gaussian_pc2.hdf5")

    n_orbs_alpha = gaussian["n_orbs_alpha"]
    gaussian_mat = gaussian["fock_bb"][:n_orbs_alpha, :n_orbs_alpha]

    n_orbs_alpha = sturmian["n_orbs_alpha"]
    bas = sturmian.input_parameters.basis
    sturmian_mat = sturmian["fock_bb"][:n_orbs_alpha, :n_orbs_alpha]
    trans = common.sturmian_nlm_to_mln_order(bas)
    sturmian_mat = trans @ sturmian_mat @ trans.transpose()

    common.plot_mtcs([fe_mat, gaussian_mat, sturmian_mat], middle_labels=True,
                     vrange=(-10, 1))
    plt.savefig("fock_fe_gauss_sturm.pdf", bbox_inches="tight", dpi=300)


if __name__ == "__main__":
    main()
