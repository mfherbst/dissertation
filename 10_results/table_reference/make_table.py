#!/usr/bin/env python3

import gint
import yaml
import os
import string


restricted = ["He", "Be", "Ne", "Mg", "Ar"]

next_letter_idx = 0
sources = {
    # TODO This is not actuall true ... for Na we use a different source
    # in reality, namely the "internal" basis set definitions by D. Feller.
    # and not the "official" ones by Prasher2011 and Dunning.
    "CBL3456": {
        "letter": None,
        "footnote": r"CBS extrapolation using cc-pVTZ to "
        "cc-pv6Z~\cite{Dunning1989,Woon1993,Wilson1996,VanMourik2000,"
        "Prascher2011}"
    },
    "CBL2345": {
        "letter": None,
        "footnote": r"CBS extrapolation using cc-pVDZ to "
        "cc-pv5Z~\cite{Dunning1989,Woon1993}"
    },
}

dir_of_this_script = os.path.dirname(__file__)
with open(dir_of_this_script + "/HF_reference.yaml", "r") as f:
    literature = yaml.safe_load(f)

headings = ["system", r"\multicolumn{2}{c}{$E_\text{HF}$}"]
rows = []
for i in range(1, 20):
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
    rows.append([symbol, "$" + str(lit["value"]) + "$" + mark])

cap = r"\HF reference values"
caption = r"Reference values used for comparison of the \CS-based results " + \
    r"and for estimating errors in the \CS values. " + \
    r"The CBS extrapolation was done with a builtin routine provided by " + \
    "\molsturm following \citet{Jensen2005}. " + \
    r"For more details regarding the extrapolation procedure see appendix " + \
    r"\vref{apx:CbsLimit}."

ret = []
ret.append(r"\ctable[")
ret.append(r"    cap=" + cap + ",")
ret.append(r"    caption=" + caption + ",")
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
off = (len(rows) + 1) // 2
for i in range(off):
    def make_row(row):
        value_split = row[1].split(".")
        return row[0] + " & " + value_split[0] + "$ & $" + value_split[1]

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
