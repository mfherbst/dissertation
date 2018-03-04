#!/usr/bin/env python3

import molsturm
from molsturm import integrals
import numpy as np
import molsturm.posthf
import os
import argparse


def rotation_cpx_to_real(basis):
    """
    Rotation matrix to transform a CS basis in complex
    spherical harmonics into a basis with real spherical
    harmonics.
    """
    ret = np.zeros((basis.size, basis.size), dtype=np.complex128)

    # Factor for the ket and bra transformation cases
    fac = 1 / np.sqrt(2)
    for i, (n, l, m) in enumerate(basis.functions):
        if m == 0:
            ret[i, i] = 1
            continue

        mabs = np.abs(m)
        meven = 1 if m % 2 == 0 else -1
        if m < 0:
            ret[i, i] = - fac * 1j
            ret[i, i + 2 * mabs] = fac
        else:  # m > 0:
            ret[i, i - 2 * mabs] = meven * fac * 1j
            ret[i, i] = meven * fac
    return ret


def run_hf(k_exp, n_max, l_max):
    params = molsturm.ScfParameters()
    params.system = molsturm.System("Be")
    params.basis = molsturm.construct_basis("sturmian/atomic", params.system,
                                            k_exp=k_exp, n_max=n_max,
                                            l_max=l_max)
    params["guess/method"] = "random"
    params["scf/print_iterations"] = True

    # Run Beryllium HF calculation, not building the standard ERI tensor
    os.environ["MOLSTURM_SKIP_ERI_EXPORT"] = "on"
    res = molsturm.self_consistent_field(params)
    eri_bbbb = integrals.electron_repulsion_bbbb(params)

    # Extract some info
    coeff = res["orbcoeff_bf"]
    na = coeff.shape[0]
    norbs = res.fock.shape[0]
    nocca = res.input_parameters.system.n_alpha
    tol = res.input_parameters["scf/max_error_norm"]

    # Build bra and ket transformation matrices
    bra_trans = np.conj(rotation_cpx_to_real(params.basis))
    ket_trans = rotation_cpx_to_real(params.basis)

    # AO->MO transform using transformed coefficients
    bra_coeff = bra_trans @ coeff
    coeff = ket_trans @ coeff
    tmp = np.einsum("abcd,ai->ibcd", eri_bbbb, bra_coeff[:, :na])
    tmp = np.einsum("ibcd,bj->ijcd", tmp, coeff[:, :na])
    tmp = np.einsum("ijcd,ck->ijkd", tmp, bra_coeff[:, :na])
    tmp = np.einsum("ijkd,dl->ijkl", tmp, coeff[:, :na])

    # Check that the resulting block is real
    assert np.max(np.abs(tmp.imag)) < 1e-12

    # And replicate to the symmetry-equivalent places
    neweri = np.zeros((norbs, norbs, norbs, norbs))
    neweri[:na, :na, :na, :na] = tmp.real
    neweri[:na, :na, na:, na:] = tmp.real
    neweri[na:, na:, :na, :na] = tmp.real
    neweri[na:, na:, na:, na:] = tmp.real
    del tmp

    # Check eri has required symmetry
    assert np.allclose(neweri, neweri.transpose((1, 0, 2, 3)),
                       rtol=tol, atol=tol)

    # Transform fock matrix from complex basis functions
    # to real as well as the mo basis
    trans_fock = np.einsum("ab,ai,bj->ij", res["fock_bb"][:na, :na],
                           bra_coeff[:, :na], coeff[:, :na])
    assert np.allclose(trans_fock.diagonal(), res["orben_f"][:na],
                       rtol=tol, atol=tol)
    assert np.max(np.abs(trans_fock.imag))
    newfock = np.zeros_like(res["fock_ff"])
    newfock[:na, :na] = trans_fock.real
    newfock[na:, na:] = trans_fock.real

    # Check that transformed and rebuilt fock matrix agree
    hcore = integrals.kinetic_bb(params)
    hcore += integrals.nuclear_attraction_bb(params)
    hcore = np.einsum("ab,ai,bj->ij", hcore, bra_coeff[:, :na], coeff[:, :na])
    rebuild_fock = hcore + 2 * np.einsum("ccab->ab",
                                         neweri[:nocca, :nocca, :na, :na])
    rebuild_fock -= np.einsum("accb->ab", neweri[:na, :nocca, :nocca, :na])
    assert np.allclose(rebuild_fock, trans_fock, rtol=5e-7, atol=5e-7)

    # Replace the present values
    res["eri_ffff"] = neweri
    res["fock_ff"] = newfock

    return res


def main():
    parser = argparse.ArgumentParser(
        description="Run beryllium CS calculation and ADC(2) on top"
    )
    parser.add_argument("--kexp", type=float, default=2.0,
                        help="Sturmian exponent to use")
    parser.add_argument("--nmax", type=int, default=4,
                        help="Value for nmax to use")
    parser.add_argument("--lmax", type=int, default=1,
                        help="Value for nmax to use")
    args = parser.parse_args()
    print("Using kexp={}, nmax={}, lmax={}".format(
        args.kexp, args.nmax, args.lmax
    ), flush=True)

    # Run HF and print results
    res = run_hf(k_exp=args.kexp, n_max=args.nmax, l_max=args.lmax)
    molsturm.print_convergence_summary(res)
    molsturm.print_energies(res)
    molsturm.print_mo_occupation(res)

    print("", flush=True)

    # Run ADC
    GiB = 1024 * 1024 * 1024
    molsturm.posthf.adc2(res, verbosity=1,
                         max_memory=1 * GiB, singlets=15, triplets=0,
                         n_threads=2, n_cores=2)

    # Print final quote
    molsturm.print_quote(res)


if __name__ == "__main__":
    main()
