#!/usr/bin/python3

import sys
import os


_latex_documentclass = r"\documentclass[crop]{standalone}"
_latex_open = r"\begin{document}" + "\n" + r"\begin{tikzpicture}"
_latex_close = r"\end{tikzpicture}" + "\n" + r"\end{document}"


def find_common(f, prefix="", relto=os.getcwd()):
    fulldir = os.path.realpath(prefix)
    full = os.path.join(fulldir, f)

    if os.path.exists(full):
        return os.path.relpath(full, relto)
    elif fulldir == "/":
        raise SystemExit("Common file not found: " + f)
    else:
        return find_common(f, prefix=os.path.join(fulldir, ".."), relto=relto)


def build_tex_document(tikz, includes):
    string = _latex_documentclass + "\n"

    for pack in includes:
        string += r"\input{" + pack + "}\n"

    string += _latex_open + "\n"
    string += tikz + "\n"
    string += _latex_close

    return string


def main():
    fn = sys.argv[1]
    out = sys.argv[2]

    if not os.path.exists(fn):
        raise SystemExit("Input file does not exist")

    base = os.path.dirname(out)
    tikz = None
    with open(fn, "r") as f:
        tikz = f.read()

    includes = [
        find_common("common_" + pack + ".tex", prefix=base, relto=base)
        for pack in ["packages", "configure", "commands"]
    ]

    with open(out, "w") as f:
        f.write(build_tex_document(tikz, includes))


if __name__ == "__main__":
    main()
