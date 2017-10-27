#!/usr/bin/env python3

import gint
import yaml
import os
import string


restricted = ["He", "Be", "Ne", "Mg", "Ar"]

# TODO Cite basis sets
# The Orca calculations use the newer Dunning versions!
next_letter_idx = 0
sources = {
    "CBL3456": {
        "letter": None,
        "footnote": "CBS extrapolation using cc-pVTZ to cc-pv6Z on molsturm"
    },
    "CBL2345": {
        "letter": None,
        "footnote": "CBS extrapolation using cc-pVDZ to cc-pv5Z on molsturm"
    },
    "ccpv5z": {
        "letter": None,
        "footnote": "cc-pV5Z calculation on molsturm"
    },
    "ccpv6z": {
        "letter": None,
        "footnote": "cc-pV6Z calculation on molsturm"
    },
}

dir_of_this_script = os.path.dirname(__file__)
with open(dir_of_this_script + "/HF_reference.yaml", "r") as f:
    literature = yaml.safe_load(f)

headings = ["system", r"\multicolumn{2}{c}{$E_\text{HF}$}"]
rows = []
for i in range(1, 100):
    symbol = gint.element.find(i).symbol

    if symbol in restricted:
        lit = literature["restricted"]
        hfmark = "R"
    else:
        lit = literature["unrestricted"]
        hfmark = "U"

    if symbol not in lit:
        continue

    lit = lit[symbol]
    src = lit["source"]
    if src not in sources:
        sources[src] = {"footnote": r"\citet{" + src + "}", "letter": None}

    if sources[src]["letter"] is None:
        sources[src]["letter"] = string.ascii_lowercase[next_letter_idx]
        next_letter_idx += 1

    mark = r"\tmark[" + sources[src]["letter"] + "," + hfmark + "]"
    rows.append([symbol, str(lit["value"]) + mark])


ret = []
ret.append(r"\ctable[")
ret.append(r"    cap=\HF reference values,")
ret.append(r"    caption=Reference values used in chapter \ref{CSQChem}")
ret.append(r"       to compare to obtained results and estimate errors ")
ret.append(r"       in the \CS calculations,")
ret.append(r"    botcap,")
ret.append(r"     label=tab:HFReference,")
ret.append(r"]{lr@{.}l@{\hspace{40pt}}lr@{.}l}{")

# Add footnotes
ret.append(r"    \tnote[U]{unrestricted HF}")
ret.append(r"    \tnote[R]{restricted HF}")
for s in sorted(sources.values(), key=lambda x: str(x["letter"])):
    if not s["letter"]:
        continue
    ret.append(r"    \tnote[" + s["letter"] + "]{" + s["footnote"] + "}")
ret.append(r"}{")

# Add heading
ret.append(r"    \FL")
ret.append(r"    " + " & ".join(2 * headings) + r" \ML")

# Add content (in two columns)
off = len(rows) // 2
for i in range(len(rows) - off):
    def make_row(row):
        return row[0] + " & " + " & ".join(row[1].split("."))

    app = make_row(rows[i]) + " & "
    if i + off < len(rows):
        app += make_row(rows[i + off])
    else:
        app += "&&"

    if i + off + 1 >= len(rows):
        app += r" \LL"
    else:
        app += r" \NN"
    ret.append("    " + app)
ret.append(r"}")


with open("table_reference.tex", "w") as f:
    f.write("\n".join(ret))
