#!/usr/bin/env python3
import molsturm
import molsturm.posthf

params = molsturm.ScfParameters()
params.system = molsturm.System("Be")
params["scf/print_iterations"] = True

params.basis = molsturm.construct_basis("gaussian", params.system,
                                        basis_set_name="cc-pvtz")
res = molsturm.self_consistent_field(params)

molsturm.print_convergence_summary(res)
molsturm.print_energies(res)
molsturm.print_mo_occupation(res)
print("", flush=True)

molsturm.posthf.adc2(res, verbosity=1,
                     max_memory=500 * 1024 * 1024, singlets=5,
                     n_threads=2, n_cores=2)

molsturm.print_quote(res)
