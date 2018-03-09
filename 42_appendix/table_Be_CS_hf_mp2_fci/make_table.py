#!/usr/bin/env python3

import yaml
import numpy as np
import os


dir_of_this_file = os.path.dirname(__file__)
with open(dir_of_this_file + "/Be_fci_summary.yaml", "r") as f:
    table = yaml.safe_load(f)

table = [t for t in table if t["n_max"] in [5, 6]]
table.sort(key=lambda x: (x["n_max"], x["l_max"], x["m_max"]))


# Text column by column:
text = [[
    "",
    r"$\Nbas$",
    "HF",
    "MP2",
    "MP2 corr.",
    "FCI",
    "FCI corr.",
]]

for entry in table:
    col = [
        "$(" + str(entry["n_max"]) + "," + str(entry["l_max"]) + "," +
        str(entry["m_max"]) + ")$",
        #
        str(entry["n_bas"]),
        "{:9.5f}".format(float(entry["hf"])),
        "{:9.5f}".format(float(entry["mp2"])),
        "{:9.5f}".format(float(entry["mp2"] - entry["hf"])),
        "{:9.5f}".format(float(entry["fci"][0])),
        "{:9.5f}".format(float(entry["fci"][0] - entry["hf"])),
    ]
    text.append(col)

filename = "Be_hf_mp2_fci_nlm_table.tex"
with open(filename, "w") as f:
    f.write(r"\begin{tabular}{l|" + (len(text) - 1) * "c" + "}\n")

    # Maxmal length in each column:
    maxlen = [max(map(len, l)) for l in text]

    for i, col in enumerate(text):
        for j, t in enumerate(col):
            col[j] = ("{0:>" + str(maxlen[i]) + "s}").format(t)

    # Transpose the table:
    text = np.array(text).transpose()

    for i, row in enumerate(text):
        f.write("    " + " & ".join(row) + r" \\" + "\n")
        if i == 1:
            f.write(r"\hline" + "\n")

    f.write(r"\end{tabular}")
