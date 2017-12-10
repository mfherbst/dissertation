import numpy as np
import scipy.optimize
import molsturm
import scipy.constants


def optimize_h2o(rHO_guess, angHO_guess, conv_tol, **params):
    def geometry(r, theta):
        return molsturm.System(
            ["O", "H", "H"],
            [(0, 0, 0), (r, 0, 0), (r*np.cos(theta), r*np.sin(theta), 0)]
        )

    def objective_function(args):
        sys = geometry(*args)
        res = molsturm.hartree_fock(sys, conv_tol=conv_tol/10, **params)
        return res["energy_ground_state"]

    res = scipy.optimize.minimize(objective_function,
                                  (rHO_guess, angHO_guess),
                                  tol=conv_tol, method="Powell")
    return res.x[0], res.x[1]


if __name__ == "__main__":
    au = scipy.constants.physical_constants["atomic unit of length"][0]

    r = 1.6         # O-H    radius guess (in au)
    theta = 105     # H-O-H  angle guess

    # First a crude optimisation with sto-3g
    r, theta = optimize_h2o(r, theta, conv_tol=1e-4, basis_type="gaussian",
                            basis_set_name="sto-3g")

    # Then a more fine optimisation with def2-sv(p)
    r, theta = optimize_h2o(r, theta, conv_tol=1e-6, basis_type="gaussian",
                            basis_set_name="def2-sv(p)")

    print("optimal H-O bond length (au): ", r)
    print("optimal H-O bond length (A):  ", r * au * 10**10)
    print("optimal H-O-H bond angle:     ", theta)
