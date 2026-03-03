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
#include <ql/math/integrals/tanhsinhintegral.hpp>
#include <pybind11/pybind11.h>
#include <cmath>
#include <limits>

namespace py = pybind11;
using namespace QuantLib;

void ql_math::tanhsinhintegral(py::module_& m) {
    py::class_<TanhSinhIntegral, Integrator,
               ext::shared_ptr<TanhSinhIntegral>>(
        m, "TanhSinhIntegral",
        "Tanh-sinh quadrature for rapidly convergent integration of smooth functions.")
        .def(py::init<Real, Size, Real>(),
            py::arg("relTolerance") = std::sqrt(std::numeric_limits<Real>::epsilon()),
            py::arg("maxRefinements") = 15,
            py::arg("minComplement") = std::numeric_limits<Real>::min() * 4,
            "Constructs with relative tolerance, max refinements, and min complement.");
}
