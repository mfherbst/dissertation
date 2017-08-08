#!/usr/bin/env python3

import re
import os

try:
    import xmp_cc_by_sa as xmp
except ImportError:
    raise SystemExit("Could not find xmp_cc_by_sa.py script. "
                     "Please add this file to the python path.")


def normalise_body(s):
    """Normalise the body of a \\newcommand definition"""
    s = re.sub(r"%?\n", " ", s)
    s = re.sub(r"  +", " ", s)
    return s


def all_commands(file):
    """Generator to retrieve all commands defined with \\newcommand of an
       input latex file"""
    # Regex to find newcommand definitions
    regnewc = re.compile(r"\\newcommand{\\(?P<command>\w+)}"
                         r"\s*{(?P<definition>[^}]*)}")

    with open(file, "r") as f:
        for command, definition in regnewc.findall(f.read()):
            yield command, normalise_body(definition)


def main():
    infile = "./commands.tex"
    outfile = "./metadata.xmp"

    if not os.path.exists(infile):
        raise SystemExit("Input file " + infile + " does not exist.")

    # Extract the command definitions we need
    commands = {cmd: definition for (cmd, definition) in all_commands(infile)}
    title = commands["thesistitle"]
    url = commands["thesisurl"]
    author = "Michael F. Herbst"
    # subtitle = commands["thesissubtitle"]

    with open(outfile, "w") as f:
        f.write(xmp.generate_xmp(title, author, url))


if __name__ == "__main__":
    main()
