#!/usr/bin/env python3

import os
import yaml


HARTREE_TO_EV = 27.21138602


def load_data():
    dir_of_this_file = os.path.dirname(__file__)
    with open(dir_of_this_file + "/data_adc2.yaml", "r") as f:
        return yaml.safe_load(f)


def load_literature():
    dir_of_this_file = os.path.dirname(__file__)
    with open(dir_of_this_file + "/literature.yaml", "r") as f:
        lit = yaml.safe_load(f)
    # Convert Rydberg to Hartree
    return {k: v / 2 for k, v in lit.items()}


def load_cgto():
    dir_of_this_file = os.path.dirname(__file__)
    with open(dir_of_this_file + "/ccpdtz.yaml", "r") as f:
        return yaml.safe_load(f)


def main():
    cgto = load_cgto()
    data = load_data()
    literature = load_literature()

    print("stte", "error cgto (eV)   ", "   error cs (eV)")
    for k in ["s2s2p", "s2s3s", "s2s3p"]:
        g_cgto = cgto["ground_state"]
        v_cgto = cgto["singlets"][cgto["selected"][k]]
        e_cgto = v_cgto - g_cgto
        err_cgto = (e_cgto - literature[k]) * HARTREE_TO_EV

        cs = [d for d in data if d["nmax"] == 7][0]
        g_cs = cs["ground_state"]
        v_cs = cs["singlets"][cs["selected"][k]]
        e_cs = v_cs - g_cs
        err_cs = (e_cs - literature[k]) * HARTREE_TO_EV

        which = "<" if err_cgto < err_cs else ">"
        print(k, "{:.4e}".format(err_cgto), which, "{:.4e}".format(err_cs))


if __name__ == "__main__":
    main()
