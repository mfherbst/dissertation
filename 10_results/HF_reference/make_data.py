#!/usr/bin/env python3

import yaml
import os
import molsturm

molsturm.yaml_utils.install_constructors()
molsturm.yaml_utils.install_representers()

dir_of_this_script = os.path.dirname(__file__)
with open(dir_of_this_script + "/literature.yaml") as f:
    data = yaml.safe_load(f)
with open(dir_of_this_script + "/summary.yaml") as f:
    cbsdata = yaml.safe_load(f)

CBS_atoms = ["Li", "B", "C", "N", "O", "F",
             "Na", "Al", "Si", "P", "S", "Cl"]

for cset in cbsdata:
    if cset.get("atom") not in CBS_atoms:
        continue

    atom = cset["atom"]
    value = cset["cbs"]
    source = "CBL" + "".join([str(c) for c in cset["orders"]])

    data["unrestricted"][atom] = {
        "value": cset["cbs"],
        "source": source,
    }

with open("data.yaml", "w") as f:
    yaml.safe_dump(data, f)
