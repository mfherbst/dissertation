#!/usr/bin/env python3

from molsturm import System
import molsturm
import yaml
import collections
import os
import multiprocessing


JobArguments = collections.namedtuple("JobArguments", ["system", "kexp"])


def run_job(args):
    atom = args.system.atoms[0].symbol
    if os.path.isfile(atom + "_results.yaml"):
        return

    params = molsturm.ScfParameters()
    params.system = args.system

    results = []
    if atom in ["F", "Ne", "N", "O"]:
        state = molsturm.load_hdf5(atom + "_n3-l2-m2.hdf5")
        nlms = [(3, 2, 2), (4, 3, 3), (5, 4, 4), (6, 5, 5)]
    else:
        state = molsturm.load_hdf5(atom + "_n2-l1-m1.hdf5")
        nlms = [(2, 1, 1), (3, 2, 2), (4, 3, 3), (5, 4, 4), (6, 5, 5)]

    for nlm in nlms:
        print("#")
        print("#-- " + atom + str(nlm))
        print("#")
        params = params.copy()
        params.basis = molsturm.construct_basis("sturmian/atomic", params.system,
                                                n_max=nlm[0], l_max=nlm[1],
                                                m_max=nlm[2], k_exp=args.kexp)

        params["scf/print_iterations"] = True
        params.set_guess_external(
            *molsturm.scf_guess.extrapolate_from_previous(state, params)
        )
        state = molsturm.self_consistent_field(params)

        results.append({
            "n": nlm[0],
            "l": nlm[1],
            "m": nlm[2],
            "n_bas": state["n_bas"],
            "ene": state["energy_ground_state"],
            "k": args.kexp,
        })

    molsturm.dump_hdf5(state, atom + "_n" + str(nlm[0]) + "-l" + str(nlm[1]) +
                       "-m" + str(nlm[2]) + ".hdf5")

    with open(atom + "_results.yaml", "w") as f:
        yaml.safe_dump(results, f)


def main():
    jobs = []
    jobs.append(JobArguments(System("Li", multiplicity=2), 1.533))
    jobs.append(JobArguments(System("Be"), 1.985))
    jobs.append(JobArguments(System("B", multiplicity=2), 2.409))
    jobs.append(JobArguments(System("C", multiplicity=3), 2.849))
    jobs.append(JobArguments(System("N", multiplicity=4), 3.287))
    jobs.append(JobArguments(System("O", multiplicity=3), 3.685))
    jobs.append(JobArguments(System("F", multiplicity=2), 4.099))
    jobs.append(JobArguments(System("Ne"), 4.512))

    nproc = multiprocessing.cpu_count()
    with multiprocessing.Pool(processes=nproc) as pool:
        list(pool.imap_unordered(run_job, jobs))


if __name__ == "__main__":
    main()
