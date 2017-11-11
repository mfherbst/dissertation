#!/usr/bin/env python3

import molsturm
import numpy as np
import yaml
import os
import multiprocessing


dir_of_this_file = os.path.dirname(__file__)


def filename(atom):
    return dir_of_this_file + "/" + atom + "_plot_data.yaml"


def run_calculation(args):
    atom, nlm, k_exp = args

    outdir = dir_of_this_file + "/outstates"
    os.makedirs(outdir, exist_ok=True)

    n = nlm[0]
    l = nlm[1]
    m = nlm[2]
    outfile = outdir + "/" + atom + "_n" + str(n) + "-l" + str(l) + \
        "-m" + str(m) + ".hdf5"

    print("#")
    print("#-- " + atom + " (n,l,m)=" + str(nlm))
    print("#")

    if not os.path.isfile(outfile):
        def find_file():
            for sn in range(n, -1, -1):
                for sl in range(l, -1, -1):
                    sn_file = dir_of_this_file + "/" + atom + "_n" + \
                        str(sn) + "-l" + str(sl) + "-m" + str(m) + ".hdf5"
                    if os.path.isfile(sn_file):
                        old = molsturm.load_hdf5(sn_file)
                        print("using " + sn_file)
                        return old
        old = find_file()

        if old is None:
            raise ValueError("No guess found for " + atom + " " + str(n))

        k_exp = k_exp

        params = molsturm.ScfParameters()
        params.system = old.input_parameters.system
        params.basis = molsturm.construct_basis("sturmian/atomic",
                                                params.system, n_max=n,
                                                l_max=l, m_max=m,
                                                k_exp=k_exp)
        params["scf/print_iterations"] = True
        guess = molsturm.scf_guess.extrapolate_from_previous(old, params)
        params.set_guess_external(*guess)

        res = molsturm.self_consistent_field(params)
        molsturm.dump_hdf5(res, outfile)
    else:
        res = molsturm.load_hdf5(outfile)

    nea = res["n_alpha"]
    noa = res["n_orbs_alpha"]
    return {
        "atom": atom,
        "energy_ground_state": res["energy_ground_state"],
        "k_exp": res.input_parameters.basis.k_exp,
        "n_max": n,
        "l_max": l,
        "m_max": m,
        "n_bas": res["n_bas"],
        "orben_a": list(np.sort(res["orben_f"][:noa])),
        "orben_b": list(np.sort(res["orben_f"][noa:])),
        "orben_occ_a": list(np.sort(
            res.fock.block("oo").diagonal()[:nea])),
        "orben_occ_b": list(np.sort(
            res.fock.block("oo").diagonal()[nea:])),
    }


def dump_data(atom, nlms, k_exp):
    molsturm.yaml_utils.install_representers()
    nproc = multiprocessing.cpu_count()

    arguments = [(atom, nlm, k_exp) for nlm in nlms]
    with multiprocessing.Pool(processes=nproc) as pool:
        result = {str(r["n_max"]) + "_" + str(r["l_max"]) + "_" + str(r["m_max"]):
                  r for r in pool.imap_unordered(run_calculation, arguments)}

    with open(filename(atom), "w") as f:
        yaml.safe_dump(result, f)


def main():
    nlms_p = [(n, 1, 1) for n in range(5, 13)]
    nlms_n = [(n, l, l) for n in range(4, 13) for l in range(1, 3)]
    nlms_be = [(n, l, l) for n in range(4, 13) for l in range(0, 2)]
    nlms_c = [(n, l, l) for n in range(6, 13) for l in range(1, 3)]
    nlms_o = [(n, l, l) for n in range(6, 13) for l in range(1, 4)] + \
             [(n, 3, m) for n in range(6, 13) for m in range(1, 3)]

    dump_data("Be", nlms=nlms_be, k_exp=1.988)
    dump_data("N", nlms=nlms_n, k_exp=3.287)
    dump_data("P", nlms=nlms_p, k_exp=5.186)
    dump_data("O", nlms=nlms_o, k_exp=3.7)
    dump_data("C", nlms=nlms_c, k_exp=2.85)


if __name__ == "__main__":
    main()
