//
// Copyright (C) 2017 by the gint authors
//
// This file is part of gint.
//
// gint is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published
// by the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// gint is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with gint. If not, see <http://www.gnu.org/licenses/>.
//

#include <gint/IntegralLookup.hh>
#include <gint/IntegralUpdateKeys.hh>
#include <gint/Structure.hh>
#include <krims/GenMap.hh>
#include <lazyten/SmallVector.hh>
#include <lazyten/eigensystem.hh>

namespace rhf {
void restricted_hartree_fock(const krims::GenMap& intparams, const size_t n_alpha,
                             const size_t n_orbs = 1000, const size_t max_iter = 100) {
  using namespace lazyten;

  // Get the integrals for the appropriate integral parameters
  auto integrals = gint::IntegralLookup<SmallMatrix<double>>(intparams);
  auto Sbb       = integrals.lookup_integral("overlap");
  auto Tbb       = integrals.lookup_integral("kinetic");
  auto Vbb       = integrals.lookup_integral("nuclear_attraction");
  auto Jbb       = integrals.lookup_integral("coulomb");
  auto Kbb       = integrals.lookup_integral("exchange");

// Get an hcore guess
const auto hcorebb      = Tbb + Vbb;
const auto eigensolution = eigensystem_hermitian(hcorebb, Sbb, n_orbs);

// Current occupied coefficients in convenient data structure
const auto cocc = eigensolution.evectors().subview({0, n_alpha});

// Initialise two-electron terms with guess coefficients
Jbb.update({{"coefficients_occupied", cocc}});
Kbb.update({{"coefficients_occupied", cocc}});

double oldene = 0;
std::cout << "Iter      etot      echange" << std::endl;
for (size_t i = 0; i < max_iter; ++i) {
// Obtain new eigenpairs ...
const auto Fbb          = hcorebb + (2 * Jbb - Kbb);
const auto eigensolution = eigensystem_hermitian(Fbb, Sbb, n_orbs);

// ... and new occupied coefficients
const auto cocc = eigensolution.evectors().subview({0, n_alpha});

// Compute HF energies: E.g. Coulomb energy is tr(C^T J C)
double ene_one_elec = trace(outer_prod_sum(cocc, hcorebb * cocc));
double ene_coulomb  = 2 * trace(outer_prod_sum(cocc, Jbb * cocc));
double ene_exchge   = -trace(outer_prod_sum(cocc, Kbb * cocc));
double energy       = 2 * (ene_one_elec + .5 * ene_coulomb +
                                          .5 * ene_exchge);

// Display current iteration
double energy_diff = energy - oldene;
std::cout << i << " " << energy << " " << energy_diff << std::endl;
oldene = energy;

// Check for convergence
if (fabs(energy_diff) < 1e-6) break;

// Update the two-electron integrals,
// before coefficients go out of scope
Jbb.update({{"coefficients_occupied", cocc}});
Kbb.update({{"coefficients_occupied", cocc}});
}

  std::cout << "Doubly occupied orbitals: " << std::endl;
  for (size_t i = 0; i < n_alpha; ++i) {
    std::cout << "  " << eigensolution.evalues()[i] << std::endl;
  }
}
}  // namespace rhf

int main() {
  gint::Structure be{
        {"Be", {{0., 0., 0.}}},
  };
  const size_t n_alpha = 2;

  krims::GenMap params_gauss{
        {"basis_type", "gaussian/libint"},
        {"basis_set_name", "pc-2"},
        {"structure", be},
  };

  krims::GenMap params_sturm{
        {"basis_type", "sturmian/atomic/cs_dummy"},
        {"k_exponent", 1.988},
        {"n_max", 5},
        {"l_max", 1},
        {"m_max", 1},
        {"structure", be},
  };

  rhf::restricted_hartree_fock(params_gauss, n_alpha);
  return 0;
}
