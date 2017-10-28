from matplotlib import pyplot as plt
import molsturm
import gint
import molsturm.posthf
import numpy as np
from scipy.optimize import curve_fit


def compute_curve(atom, basis_set_name, backend="libint", conv_tol=1e-6,
                  zrange=(0.65, 7.15), n_points=30):
    distances = np.linspace(zrange[1], zrange[0], n_points)
    energies = np.empty_like(distances)
    previous_hf = None

    for i, z in enumerate(distances):
        sys = molsturm.MolecularSystem(
            atoms=[atom, atom],
            coords=[(0, 0, 0), (0, 0, z)],
        )
        basis = gint.gaussian.Basis(sys, basis_set_name, backend)

        guess = "random" if not previous_hf else previous_hf
        state = molsturm.hartree_fock(sys, basis, conv_tol=conv_tol,
                                   guess=guess, restricted=False)
        mp2 = molsturm.posthf.mp2(state)
        energies[i] = mp2["energy_ground_state"]
        previous_hf = state

    return distances, energies


def plot_morse_fit(dist, ene):
    # Fit Morse potential
    def morse(x, de, a, xeq, off):
        return de * (1 - np.exp(-a * (x - xeq)))**2 + off
    popt, pcov = curve_fit(morse, dist, ene)

    # Plot data and Morse using 100 sampling points:
    x = np.linspace(np.min(dist), np.max(dist), 100)
    plt.plot(dist, ene, "+", label="MP2")
    plt.plot(x, morse(x, *popt), label="Morse potential")

    plt.xlabel("Bond distance in Bohr")
    plt.ylabel("Energy in Hartree")
    plt.legend()


if __name__ == "__main__":
    dist, ene = compute_curve("H", "def2-svp", "libint")
    plot_morse_fit(dist, ene)
    plt.show()
