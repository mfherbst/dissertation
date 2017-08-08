import numpy as np


def compute_rms_qf(state, qnum="l"):
    """
    Computes the root mean square coefficient values
    with respect to some quantum number and per orbital f.

    If qnum == "l" the rms cofficient per angular momentum number l
    is computed.

    If qnum == "m" the rms coefficient per azimuthal quantum number m
    is computed.
    """
    coeff_bf = state["orbcoeff_bf"]

    basis = state.input_parameters.basis
    n_max, l_max, m_max = np.max(basis.functions, axis=0)

    if qnum == "l":
        rnge = list(range(l_max+1))

        def make_predicate(l):
            return lambda nlm: nlm[1] == l
    elif qnum == "m":
        rnge = list(range(m_max+1))

        def make_predicate(m):
            return lambda nlm: abs(nlm[2]) == m
    else:
        raise NotImplementedError("qnum value " + qnum)

    ret = np.empty((len(rnge), coeff_bf.shape[1]))
    for qnum in rnge:
        # Mask to filter all basis functions with the desired quantum number
        pred = make_predicate(qnum)
        mask = np.array([pred(nlm) for nlm in basis.functions])

        # Build the average sum of squares:
        ret[qnum, :] = np.average(np.square(coeff_bf[mask, :]), axis=0)

        # And take the square root
        ret[qnum, :] = np.sqrt(ret[qnum, :])
    return ret


def compute_rmsr_q(state, factor=10, qnum="l"):
    """
    Compute the root mean square coefficient value
    per quantum number.
    By default the angular momentum quantum number l
    is chosen.
    The average is over all the 'reachable' orbitals.

    Here we define a reachable orbital as one
    which has an energy at most
    `HOMO + factor * (LUMO-HOMO)`
    """
    noa = state["n_orbs_alpha"]
    na = state["n_alpha"]
    nb = state["n_beta"]

    rms_lf = compute_rms_qf(state, qnum=qnum)
    rmsa_lf = rms_lf[:, :noa]
    rmsb_lf = rms_lf[:, noa:]

    orbena_f = state["orben_f"][:noa]
    orbenb_f = state["orben_f"][noa:]

    e_homo = max(orbena_f[na-1], orbenb_f[nb-1])
    e_lumo = min(orbena_f[na], orbenb_f[nb])
    gap = e_lumo - e_homo

    # Build the masks of the alpha and beta orbitals
    # within the range of 'reachable' orbitals
    maska = orbena_f <= e_homo + factor * gap
    maskb = orbenb_f <= e_homo + factor * gap

    # Compute the sum of squares:
    tmp = np.average(np.square(rmsa_lf[:, maska]), axis=1)
    tmp += np.average(np.square(rmsb_lf[:, maskb]), axis=1)

    # Build the average, the square root and return
    return np.sqrt(tmp)


def compute_rmso_q(state, qnum="l"):
    """
    Computes the root mean square coefficient value
    per quantum number.

    By default the average is wrt the
    angular momentum quantum number l,
    but the azimuthal quantum number m can be chosen as well
    by setting qnum="m".

    The resulting values are rms-averaged over
    the occupied orbitals.
    """
    return compute_rmsr_q(state, factor=0, qnum=qnum)


def compute_rmsw_l(state, qnum="l"):
    """
    Compute the RMS coefficient value binned per some quantum
    number, by default the angular momentum quantum number l.

    The rms-average value in such a bin is computed, where
    the virtual orbitals are weighted by 1 over their
    orbital energy.

    Potential quantum numbers are "l" and "m".
       """
    noa = state["n_orbs_alpha"]

    rms_lf = compute_rms_qf(state, qnum=qnum)
    rmsa_lf = rms_lf[:, :noa]
    rmsb_lf = rms_lf[:, noa:]

    orbena_f = state["orben_f"][:noa]
    orbenb_f = state["orben_f"][noa:]

    weighta_f = 1 / orbena_f
    weightb_f = 1 / orbenb_f
    weighta_f[orbena_f <= 0] = 1
    weightb_f[orbenb_f <= 0] = 1

    rmsa_lf = rmsa_lf * weighta_f[np.newaxis, :]
    rmsb_lf = rmsb_lf * weightb_f[np.newaxis, :]
    tmp = np.average(np.square(rmsa_lf), axis=1)
    tmp += np.average(np.square(rmsb_lf), axis=1)
    return np.sqrt(tmp)
