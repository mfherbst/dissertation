from matplotlib import pyplot as plt
import molsturm
import molsturm.posthf
import numpy as np
from scipy.optimize import curve_fit


def compute_curve(atom, basis_args, conv_tol=1e-6,
                  zrange=(0.65, 7.15),
                  n_points=30):
  distances = np.linspace(zrange[1], zrange[0],
                          n_points)
  energies = np.empty_like(distances)
  previous_hf = None

  for i, z in enumerate(distances):
    system = molsturm.System(
      atoms=[atom, atom],
      coords=[(0, 0, 0), (0, 0, z)],
    )

    # Run a UHF and subsequent UMP2 calculation
    # using the basis parameters. If a previous
    # result exists (i.e. this is not the first
    # HF calculation we do along the curve)
    # use it as a guess.
    guess = "random" if not previous_hf \
      else previous_hf
    state = molsturm.hartree_fock(
      system, conv_tol=conv_tol, guess=guess,
      restricted=False, **basis_args
    )
    mp2 = molsturm.posthf.mp2(state)
    energies[i] = mp2["energy_ground_state"]
    previous_hf = state
  return distances, energies


def plot_morse_fit(dist, ene):
  # First fit Morse potential:
  def morse(x, de, a, xeq, off):
    return de * (1 - np.exp(-a * (x - xeq)))**2 + off
  popt, pcov = curve_fit(morse, dist, ene)

  # Plot data and Morse using 100 sampling points:
  x = np.linspace(np.min(dist), np.max(dist), 100)
  plt.plot(dist, ene, "+", label="UMP2")
  plt.plot(x, morse(x, *popt),
           label="Morse potential")

  plt.xlabel("Bond distance in Bohr")
  plt.ylabel("Energy in Hartree")
  plt.legend()


def main():
  # Compute the H2 dissociation using a particular
  # basis type, backend and basis set:
  basis_args = {
    "basis_type": "gaussian",
    "backend": "libint",
    "basis_set_name": "def2-svp"
  }
  distances, energies = compute_curve("H", basis_args)

  plot_morse_fit(distances, energies)
  plt.show()


if __name__ == "__main__":
  main()
