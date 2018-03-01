#!/usr/bin/env python3
import h2_dissociation as lib
import yaml


if __name__ == "__main__":
    basis_args = {
      "basis_type": "gaussian",
      "backend": "libint",
      "basis_set_name": "def2-svp"
    }
    dist, ene = lib.compute_curve("H", basis_args)

    res = {
        "distances": dist.tolist(),
        "energies": ene.tolist(),
    }
    with open("H2_UMP2_dissociation.yaml", "w") as f:
        yaml.safe_dump(res, f)
