#!/usr/bin/env python3

from matplotlib import pyplot as plt
import common
import molsturm
import os
import yaml
import shutil

#
# Plot how the Fock matrix structure changes during the SCF of a Gaussian
# and Sturmian basis.


def plot_convergence_progression(instate):
    # Store input state
    states = [instate]

    # Copy parameters:
    params = instate.input_parameters.copy()
    guess = molsturm.scf_guess.extrapolate_from_previous(instate, params)
    params.set_guess_external(*guess)
    del params["scf"]

    for error in [1e-2, 1e-6]:
        params["scf/conv_tol"] = error

        hfres = molsturm.self_consistent_field(params)
        states.append(hfres)

    # Plot them all:
    return common.plot_states(states)


def main():
    dir_of_this_file = os.path.dirname(__file__)
    common.setup()

    sturmian = molsturm.load_hdf5(dir_of_this_file + "/Be_sturmian_511.hdf5")
    props = plot_convergence_progression(sturmian)
    plt.savefig("fock_sturmian.pdf", bbox_inches="tight")
    with open("fock_sturmian_props.yaml", "w") as f:
        yaml.safe_dump(props, f)

    gaussian = molsturm.load_hdf5(dir_of_this_file + "/Be_gaussian_pc2.hdf5")
    props = plot_convergence_progression(gaussian)
    plt.savefig("fock_gaussian.pdf", bbox_inches="tight")
    with open("fock_gaussian_props.yaml", "w") as f:
        yaml.safe_dump(props, f)

    # Copy the FE stuff
    shutil.copy(dir_of_this_file + "/fock_fe.pdf", "fock_fe.pdf")
    shutil.copy(dir_of_this_file + "/fock_fe_props.yaml", "fock_fe_props.yaml")


if __name__ == "__main__":
    main()
