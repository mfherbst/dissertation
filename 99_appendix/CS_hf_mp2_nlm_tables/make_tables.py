#!/usr/bin/env python3

import yaml
import numpy as np
import gint
import os


def generate_table(data):
    data.sort(key=lambda x: (x["n_max"], x["l_max"], x["m_max"]))

    atom = data[0]["symbol"]
    name = gint.element.by_symbol(atom).name
    k_exp = data[0]["k_exp"]

    # Columns to print
    columns = [[
        "",
        r"$\Nbas$",
        "HF",
        "MP2",
        "MP2 corr.",
        r"$\text{corr} / \Nbas$",
    ]]

    for entry in data:
        assert entry["symbol"] == atom
        assert entry["k_exp"] == k_exp

        n_bas = int(entry["n_bas"])
        Emp2 = float(entry["mp2"])
        Ecorr = float(Emp2 - entry["hf"])
        col = [
            "$(" + str(entry["n_max"]) + "," + str(entry["l_max"]) + "," +
            str(entry["m_max"]) + ")$",
            #
            str(n_bas),
            "{:9.5f}".format(float(entry["hf"])),
            "{:9.5f}".format(Emp2),
            "{:9.5f}".format(Ecorr),
            "{:9.5f}".format(Ecorr / n_bas),
        ]
        columns.append(col)

    ret = [
        r"\begin{table}",
        r"\smaller",
        r"   \begin{tabular}{l|" + (len(columns) - 1) * "c" + r"}",
    ]

    # Maxmal length in each column:
    maxlen = [max(map(len, l)) for l in columns]

    for i, col in enumerate(columns):
        for j, t in enumerate(col):
            col[j] = ("{0:>" + str(maxlen[i]) + "s}").format(t)

    # Transpose the table:
    columns = np.array(columns).transpose()

    for i, row in enumerate(columns):
        if i == 2:
            ret.append(r"\hline")
        ret.append(2*4*" " + " & ".join(row) + r" \\")

    ret += [
        r"   \end{tabular}",
        (r"   \caption{HF and MP2 energies of " + name + r" using $\kexp = " +
            "{0:5.3f}".format(k_exp) + r"$}"),
        r"\end{table}"
    ]
    return "\n".join(ret)


def main():
    dir_of_this_file = os.path.dirname(__file__)

    with open(dir_of_this_file + "/summary.yaml", "r") as f:
        table = yaml.safe_load(f)

        elements = np.array([e["atnum"] for e in table])
        elements = np.unique(elements)
        elements = [gint.element.find(e).symbol for e in elements]

        for e in elements:
            ret = generate_table([d for d in table if d["symbol"] == e])
            with open("CS_HF_MP2_" + e + "_table.tex", "w") as f:
                f.write(ret)


if __name__ == "__main__":
    main()
