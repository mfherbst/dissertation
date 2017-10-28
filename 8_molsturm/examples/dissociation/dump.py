#!/usr/bin/env python3
import h2_dissociation as lib
import yaml


if __name__ == "__main__":
    dist, ene = lib.compute_curve("H", "def2-svp", "libint")
    res = {
        "distances": dist.tolist(),
        "energies": ene.tolist(),
    }
    with open("H2_UMP2_dissociation.yaml", "w") as f:
        yaml.safe_dump(res, f)
