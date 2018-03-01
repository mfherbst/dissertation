#!/usr/bin/env python3

import molsturm
import numpy as np
import os
import yaml

molsturm.yaml_utils.install_constructors()
molsturm.yaml_utils.install_representers()

dir_of_this_script = os.path.dirname(__file__)
with open(dir_of_this_script + "/literature.yaml") as f:
    data = yaml.safe_load(f)
with open(dir_of_this_script + "/summary.yaml") as f:
    cbsdata = yaml.safe_load(f)

CBS_systems = ["Li", "B", "C", "N", "O", "F",
               "Na", "Al", "Si", "P", "S", "Cl",
               "B+", "C-", "O+", "F-",
               "Al+", "Si-", "S+", "Cl-"]

for cset in cbsdata:
    system_key = "system"
    if system_key not in cset:
        system_key = "atom"

    system = cset[system_key]
    if system not in CBS_systems:
        continue

    source = "CBL" + "".join([str(c) for c in cset["orders"]])
    value = cset["cbs"]

    # The calculations have run with a conv_tol of 5e-7 tops,
    # so we do not accept more than 7 digits.
    # Other than that we use the stddev as an estimate for the
    # number of trustworthy digits.
    digits = min(7, int(-np.log(cset["stddev"])))
    dfmt = "{:." + str(digits) + "f}"

    # First round using numpy, then format as a string with
    # the said nuber of digits, then convert back to float.
    value = float(dfmt.format(value, digits))

    data["unrestricted"][system] = {
        "value": value,
        "source": source,
    }

with open("data.yaml", "w") as f:
    yaml.safe_dump(data, f)
