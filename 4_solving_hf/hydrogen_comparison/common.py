#!/usr/bin/env python3

import molsturm
import matplotlib
import numpy as np
from molsturm import integrals
from scipy import linalg

XLABEL = r"relative distance in Bohr"
ELLABEL = r"$E_L(\underline{\boldsymbol{r}})$ in Hartree"
RELABEL = r"relative error"


def hydrogen_local_energy(basis, coefficients,
                          r=np.linspace(0, 10, 1000), dr=5e-6,
                          mirror=True):
    """
    params:
        basis         The basis object from molsturm describing the basis
                      to use
        coefficients  The coefficients forming the ground state 1s orbitals
                      of hydrogen from the basis functions
        dr            The difference parameter for numerical differentiation
        r             The points on which to compute the local energy
    """
    def orbital_1s(r):
        """Return the function value of the 1s orbital on the radial axis"""
        zero = np.linspace(0, 0, 1)
        x, y, z = np.meshgrid(r, zero, zero)
        raw = basis.evaluate_at(x, y, z)[:, 0, :, 0]
        return np.einsum("b,br->r", coefficients, raw)

    # Finite differences first and second derivative.
    # We need f(r-2h) up to f(r+2h)
    fm2 = orbital_1s(r - 2*dr)
    fm1 = orbital_1s(r - dr)
    f = orbital_1s(r)
    fp1 = orbital_1s(r + dr)
    fp2 = orbital_1s(r + 2*dr)

    df = (-fp2 + 8*fp1 - 8*fm1 + fm2) / (12*dr)
    ddf = (-fp2 + 16*fp1 - 30*f + 16*fm1 - fm2) / (12*dr*dr)

    # Make functional values symmetric (because they have to)
    if mirror:
        r = np.concatenate((-r[::-1], r))
        f = np.concatenate((f[::-1], f))
        df = np.concatenate((df[::-1], df))
        ddf = np.concatenate((ddf[::-1], ddf))

    # Notice: Radial laplacian is d2f/dr2 + 2/r * df/dr
    kin_part = - 1/2 * (ddf + 2*df/np.abs(r))
    locen = kin_part / f - 1/np.abs(r)
    return r, locen


def hydrogen_relative_error(basis, coefficients, r=np.linspace(0, 10, 1000),
                            mirror=True):
    def exact_1s(r):
        """Return the exact function value of the 1s orbital"""
        return np.sqrt(1./np.pi) * np.exp(-r)

    def orbital_1s(r):
        """Return the function value of the 1s orbital on the radial axis"""
        zero = np.linspace(0, 0, 1)
        x, y, z = np.meshgrid(r, zero, zero)
        raw = basis.evaluate_at(x, y, z)[:, 0, :, 0]
        return np.einsum("b,br->r", coefficients, raw)

    rel_err = (orbital_1s(r) - exact_1s(r)) / exact_1s(r)

    if mirror:
        r = np.concatenate((-r[::-1], r))
        rel_err = np.concatenate((rel_err[::-1], rel_err))
    return r, rel_err


def do_hydrogen_scf(basis):
    params = molsturm.ScfParameters()
    params.system = molsturm.System("H")
    params.basis = basis

    t_bb = integrals.kinetic_bb(params)
    v_bb = integrals.nuclear_attraction_bb(params)
    s_bb = integrals.overlap_bb(params)

    ene, coeff = linalg.eigh(t_bb + v_bb, s_bb, eigvals=(0, 0))

    coeff = coeff[:, 0]
    if coeff.sum() < 0:
        return -1 * coeff
    else:
        return coeff


def setup():
    # Setup matplotlib
    tex_premable = [
        r"\usepackage[T1]{fontenc}",
        r"\usepackage[utf8]{inputenc}",
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
