#!/usr/bin/env python3

import yaml
import gint
import os


def make_element_rows(elementdata, basis_sets):
    # Generate correlation energy column
    for data in elementdata:
        data["cc"] = data["mp2"] - data["hf"]

    if data["symbol"] in ["Be", "Ne", "Mg", "Ar"]:
        restr = "R"
        mrestr = ""
    else:
        restr = "U"
        mrestr = "U"

    rows = [
        ["", restr + r"HF"],
        [data["symbol"], mrestr + r"MP2"],
        [r"\textit{" + "{:.3f}".format(data["k_exp"]) + "}",
         mrestr + "MP2 corr."],
    ]
    for i, method in enumerate(["hf", "mp2", "cc"]):
        row = rows[i]
        for basis in basis_sets:
            values = [d[method] for d in elementdata
                      if (d["n_max"], d["l_max"], d["m_max"]) == basis]
            if len(values) == 0:
                row.append(r"\multicolumn{2}{c}{}")
            else:
                value = "{:.5f}".format(values[0])
                value = ["$" + v + "$" for v in value.split(".")]
                row.extend(value)

    rows[-1][-1] += r" \ML"
    return rows


def prepare_rows(data):
    elements = set(e["atnum"] for e in data)
    elements = sorted(elements)
    elements = [gint.element.find(e).symbol for e in elements]
    basis_sets = set((d["n_max"], d["l_max"], d["m_max"]) for d in data)
    basis_sets = sorted(basis_sets)
    n_bass = len(basis_sets)

    headings = [
        [
            "atom", "",
            r"\multicolumn{" + str(2 * n_bass) + r"}{c}{Coulomb-Sturmian basis set}",
        ], [
            r"\textit{$\kexp$}", "",
        ] + [
            r"\multicolumn{2}{c}{$" + "({0:},{1:},{2:})".format(*nlm) + "$}"
            for nlm in basis_sets
        ],
        # TODO \Nbas
    ]
    colstring = r"ll @{\hspace{20pt}} *{" + str(n_bass) + "}{r@{.}l}"

    rows = []
    for e in elements:
        elementdata = [d for d in data if d["symbol"] == e]
        rows.extend(make_element_rows(elementdata, basis_sets))
    return headings, colstring, rows


def make_table(data, period, label, continued=False, sideways=False):
    headings, colstring, rows = prepare_rows(data)

    caption = "Hartree-Fock and MP2 ground state energies " + \
        "as well as MP2 correlation energies~(MP2 corr.) for the atoms " + \
        "of the " + period + " period and a range of \CS basis sets."

    shortcap = "CS-based HF and MP2 ground state energies for atoms of the " + \
        period + " period"

    ret = []
    ret.append(r"\ctable[")
    ret.append(r"    cap=HF and MP2 energies for the " + period +
               " period.,")
    ret.append(r"    mincapwidth=0.98\textwidth,")
    ret.append(r"    caption=" + caption + ",")
    ret.append(r"    pos=tbph,")
    ret.append(r"    botcap,")
    ret.append(r"    cap=" + shortcap + ",")
    if continued:
        ret.append(r"    continued,")
    else:
        ret.append(r"    label=tab:" + label + ",")
    if sideways:
        ret.append(r"    sideways,")
    ret.append(r"]{" + colstring + "}{}{")

    # Add headings
    ret.append(r"    \FL")
    for i, head in enumerate(headings):
        if i + 1 >= len(headings):
            ending = r" \ML"
        else:
            ending = r" \NN"
        ret.append(r"    " + " & ".join(head) + ending)

    for i, row in enumerate(rows):
        ending = r" \NN"
        if row[-1].endswith(r" \ML"):
            # Strip ending off last column if there is any
            ending = row[-1][-4:]
            row[-1] = row[-1][:-4]
        if i + 1 >= len(rows):
            ending = r" \LL"
        ret.append("    " + " & ".join(row) + ending)
    ret.append(r"}")

    return ret


def is_period(dataset, n):
    atnum = dataset["atnum"]
    if n == 1:
        return atnum < 3
    if n == 2:
        return atnum > 2 and atnum < 11
    if n == 3:
        return atnum > 10 and atnum < 19
    if n == 4:
        return atnum > 18 and atnum < 37


def main():
    dir_of_this_file = os.path.dirname(__file__)

    with open(dir_of_this_file + "/summary.yaml", "r") as f:
        data = yaml.safe_load(f)

    # TODO One could make this table alternatively a continuing table,
    #      i.e. refer to all periods by the same table name.
    for p in range(1, 6):
        chunk = [d for d in data if is_period(d, p)]
        if len(chunk) <= 0:
            continue

        data_parts = [chunk]
        sidw = [False]
        if p == 1:
            period = "1st"
        elif p == 2:
            period = "2nd"
            chunk1 = [d for d in chunk if d["m_max"] < 2]
            chunk2 = [d for d in chunk if d["m_max"] >= 2]
            data_parts = [chunk1, chunk2]
            sidw = [False, True]
            del chunk1
            del chunk2
        elif p == 3:
            period = "3rd"
            sidw = [True]
        else:
            period = str(p) + "th"

        label = "CSCorrConv" + str(p)
        for i, chunk in enumerate(data_parts):
            contd = i > 0
            tble = make_table(chunk, period=period, label=label,
                              continued=contd, sideways=sidw[i])

            extra = ""
            if contd:
                extra = "." + str(i)
            filename = "table_cs_corr_conv_" + str(p) + extra + ".tex"
            with open(filename, "w") as f:
                f.write("\n".join(tble))


if __name__ == "__main__":
    main()
