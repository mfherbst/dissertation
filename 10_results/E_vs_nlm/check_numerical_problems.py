#!/usr/bin/env python3

import molsturm
import os
import yaml


dir_of_this_file = os.path.dirname(__file__)


def compute(atom, nlm, k_exp):
    n, l, m = nlm

    s_file = dir_of_this_file + "/" + atom + "_n" + \
        str(n) + "-l" + str(l) + "-m" + str(m) + ".hdf5"

    if os.path.isfile(s_file):
        return molsturm.load_hdf5(s_file)

    old = None
    for sn, sl, sm in [(7, 1, 1), (6, 1, 1)]:
        sn_file = dir_of_this_file + "/" + atom + "_n" + \
            str(sn) + "-l" + str(sl) + "-m1.hdf5"
        if not os.path.isfile(sn_file):
            continue
        old = molsturm.load_hdf5(sn_file)

    if old is None:
        raise ValueError("No guess found for " + atom + " " + str(n))

    params = molsturm.ScfParameters()
    params.system = old.input_parameters.system
    params.basis = molsturm.construct_basis("sturmian/atomic/cs_dummy",
                                            params.system, n_max=nlm[0],
                                            l_max=nlm[1], m_max=nlm[2],
                                            k_exp=k_exp, backend="cs_dummy")

    if atom == "P":
        params["scf/conv_tol"] = 5e-6

    params["scf/print_iterations"] = True
    guess = molsturm.scf_guess.extrapolate_from_previous(old, params)
    params.set_guess_external(*guess)

    res = molsturm.self_consistent_field(params)
    molsturm.dump_hdf5(res, s_file)
    return res


def main():
    nlm = (10, 1, 1)

    vals = [
        compute("Be", nlm=nlm, k_exp=1.98),
        compute("N", nlm=nlm,  k_exp=3.28),
        compute("P", nlm=nlm, k_exp=5.05),
        compute("O", nlm=nlm, k_exp=3.7),
    ]

    with open("./HF_literature.yaml", "r") as f:
        lit = yaml.safe_load(f)
        literature_rhf = lit["restricted"]
        literature_uhf = lit["unrestricted"]

    print("atom      computed          literature(RHF)    diff    lit(UHF)    diff")
    for v in vals:
        atom = v.input_parameters.system.atoms[0].symbol
        if atom in ["N", "P", "O"]:
            uhf = literature_uhf[atom]["value"]
            diff = v["energy_ground_state"] - uhf
        else:
            uhf = 0
            diff = 0

        print(atom, "  ", v["energy_ground_state"], "  ", literature_rhf[atom]["value"],
              "  ", abs(v["energy_ground_state"] - literature_rhf[atom]["value"]), "  ",
              uhf, "  ", diff)
    print()
    print("Note here that UHF is not variational")


if __name__ == "__main__":
    main()
