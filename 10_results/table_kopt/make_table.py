#!/usr/bin/env python3

import re
import yaml
import os
import gint
import molsturm

dir_of_this_script = os.path.dirname(__file__)
with open(dir_of_this_script + "/HF_reference.yaml", "r") as f:
    literature = yaml.safe_load(f)


def prepare_rows(data):
    headings = ["system", r"\CS basis", r"\multicolumn{2}{c}{$\kopt$}",
                r"$\Nbas$", r"\multicolumn{3}{c}{$E_\text{HF}$}",
                r"\multicolumn{2}{c}{relative error}"]
    colstring = r"lc r@{.}l c r@{.}l@{}c r@{.}l"

    def atnumchargenlm(d):
        return (d["atom_number"], d["charge"], d["n_max"],
                d["l_max"], d["m_max"])

    rows = []
    for dset in sorted(data, key=atnumchargenlm):
        charge = ""
        if dset["charge"] == 1:
            charge = "+"
        elif dset["charge"] == -1:
            charge = "-"
        atom = gint.element.find(dset["atom_number"]).symbol
        system = atom + charge

        # TODO
        # Temporary until multiplicity key is available
        anum = dset["atom_number"] - dset["charge"]
        if "multiplicity" not in dset:
            if anum in [3, 5, 9, 11, 13, 17, 19]:
                dset["multiplicity"] = 2
            elif anum in [6, 8, 14, 16]:
                dset["multiplicity"] = 3
            elif anum in [7, 15]:
                dset["multiplicity"] = 4
            else:
                dset["multiplicity"] = 1

        sys = molsturm.System(atom)
        sys.adjust_electrons(charge=dset["charge"],
                             multiplicity=dset["multiplicity"])

        if sys.multiplicity == 1:
            lit = literature["restricted"]
            mark = r"\tmark[R]"
        else:
            lit = literature["unrestricted"]
            mark = r"\tmark[U]"

        hf = dset["ground_state_energy"]
        if abs(hf) < 10:
            hfstr = "{:.5f}".format(hf)
        elif abs(hf) < 100:
            hfstr = "{:.5f}".format(hf)
        elif abs(hf) < 1000:
            hfstr = "{:.4f}".format(hf)
        else:
            raise NotImplementedError()
        hfstr = ["$" + v + "$" for v in hfstr.split(".")]

        n_bas = str(dset["n_bas"])
        basis = r"$(" + str(dset["n_max"]) + ", " + str(dset["l_max"]) + \
                ", " + str(dset["m_max"]) + r")$"
        kopt = "{:.3f}".format(dset["k_opt"])
        kopt = ["$" + v + "$" for v in kopt.split(".")]

        if system in lit:
            error = (hf - lit[system]["value"]) / abs(lit[system]["value"])
            error = "{:.1e}".format(error)
            error = re.sub("e(-?[0-9]+)", r"\\E{\1}", error)
            error = ["$" + v + "$" for v in error.split(".")]
        else:
            error = "", ""
        system = r"\ce{" + system + "}"

        rows.append([system, basis, kopt[0], kopt[1], n_bas,
                     hfstr[0], hfstr[1], mark, error[0], error[1]])
    return headings, colstring, rows


def make_table(data, period, label):
    headings, colstring, rows = prepare_rows(data)

    ret = []
    ret.append(r"\ctable[")
    ret.append(r"    cap=Optimal \CS exponent for the " + period +
               " period at Hartree-Fock level,")
    ret.append(r"    caption=Optimal \CS exponent for the " + period +
               r" period of the periodic table at \HF level. "
               r"Relative errors are given with respect to the "
               r"reference energies of table \vref{tab:HFReference}.,")
    ret.append(r"    botcap,")
    ret.append(r"    mincapwidth=0.98\textwidth,")
    ret.append(r"    footerwidth,")
    ret.append(r"     label=tab:" + label + ",")
    ret.append(r"]{" + colstring + "}{")
    ret.append(r"    \tnote[U]{unrestricted HF}")
    ret.append(r"    \tnote[R]{restricted HF}")
    ret.append(r"}{")

    # Add heading
    ret.append(r"    \FL")
    ret.append(r"    " + " & ".join(headings) + r" \ML")

    for i, row in enumerate(rows):
        ending = r" \LL" if i + 1 >= len(rows) else r" \NN"
        ret.append("    " + " & ".join(row) + ending)
    ret.append(r"}")

    return ret


def is_period(dataset, n):
    atnum = dataset["atom_number"]
    if n == 1:
        return atnum < 3
    if n == 2:
        return atnum > 2 and atnum < 11
    if n == 3:
        return atnum > 10 and atnum < 19
    if n == 4:
        return atnum > 18 and atnum < 37


def main():
    with open(dir_of_this_script + "/summary.yaml", "r") as f:
        data = yaml.safe_load(f)

    def filtered(d):
        n, l, m = d["n_max"], d["l_max"], d["m_max"]

        # Skip invalid ones
        if not d["valid"]:
            return False

        # On Li, Be, N, Ne and  Na, Mg, P, Ar
        # l == 2 makes no difference since RMSO_l is pretty small for l >= 2
        skipl2_elems = ["Li", "Be", "N", "Ne", "Na", "Mg", "P", "Ar"]
        if gint.element.find(d["atom_number"]).symbol in skipl2_elems:
            if l > 1:
                return False

        # TODO OPTIONAL
        # Skip charged  ones
        if d["charge"] != 0:
            return False

        # By default return true
        return True
    data = [d for d in data if filtered(d)]

    # TODO One could make this table alternatively a continuing table,
    #      i.e. refer to all periods by the same table name.
    tble = []
    for p in range(2, 5):
        data_part = [d for d in data if is_period(d, p)]

        if len(data_part) <= 0:
            continue

        if p == 1:
            period = "1st"
        elif p == 2:
            period = "2nd"
        elif p == 3:
            period = "3rd"
        else:
            period = str(p) + "th"
        label = "Kopt" + str(p)

        tble.extend(make_table(data_part, period=period, label=label))
        tble.append("")

    with open("table_kopt.tex", "w") as f:
        f.write("\n".join(tble))


if __name__ == "__main__":
    main()
