import numpy as np
import scipy.optimize
import molsturm


def optimize_h2o(rHO_guess, angHO_guess, conv_tol,
                 **params):
  # Function which computes the cartesian geometry
  # from r and theta.
  def geometry(r, theta):
    rad = theta / 180 * np.pi
    pos = (r * np.cos(rad), r * np.sin(rad), 0)
    return molsturm.System(["O", "H", "H"],
                           [(0, 0, 0), (r, 0, 0), pos])

  def objective_function(args):
    system = geometry(*args)
    ret = molsturm.hartree_fock(
        system, conv_tol=conv_tol/100, **params,
    )
    return ret["energy_ground_state"]

  guess = (rHO_guess, angHO_guess)
  res = scipy.optimize.minimize(
      objective_function, guess, tol=conv_tol,
      method="Powell"
  )
  return res.x[0], res.x[1]

def main():
  r = 2.0         # O-H    radius guess (in au)
  theta = 120     # H-O-H  angle guess

  # First a crude optimisation with sto-3g
  r, theta = optimize_h2o(r, theta, conv_tol=5e-4,
                          basis_type="gaussian",
                          basis_set_name="sto-3g")

  # Then a more fine optimisation with def2-sv(p)
  r, theta = optimize_h2o(r, theta, conv_tol=1e-5,
                          basis_type="gaussian",
                          basis_set_name="def2-sv(p)")
  print("optimal H-O bond length (au): ", r)
  print("optimal H-O-H bond angle:     ", theta)

if __name__ == "__main__":
  main()
