/*
 * PyQuantLib: Python bindings for QuantLib
 * https://github.com/quantales/pyquantlib
 *
 * Copyright (c) 2025 Yassine Idyiahia
 * SPDX-License-Identifier: BSD-3-Clause
 * See LICENSE for details.
 *
 * ---
 * QuantLib is Copyright (c) 2000-2025 The QuantLib Authors
 * https://www.quantlib.org/
 */

#include "pyquantlib/pyquantlib.h"
#include <ql/methods/montecarlo/lsmbasissystem.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_methods::lsmbasissystem(py::module_& m) {
    py::enum_<LsmBasisSystem::PolynomialType>(m, "PolynomialType",
        "Polynomial basis types for Longstaff-Schwartz regression.")
        .value("Monomial", LsmBasisSystem::Monomial)
        .value("Laguerre", LsmBasisSystem::Laguerre)
        .value("Hermite", LsmBasisSystem::Hermite)
        .value("Hyperbolic", LsmBasisSystem::Hyperbolic)
        .value("Legendre", LsmBasisSystem::Legendre)
        .value("Chebyshev", LsmBasisSystem::Chebyshev)
        .value("Chebyshev2nd", LsmBasisSystem::Chebyshev2nd)
        .export_values();
}
