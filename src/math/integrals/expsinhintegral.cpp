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
#include <ql/math/integrals/expsinhintegral.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <cmath>
#include <limits>

namespace py = pybind11;
using namespace QuantLib;

void ql_math::expsinhintegral(py::module_& m) {
    using HalfInfiniteIntegrate =
        Real (ExpSinhIntegral::*)(const std::function<Real(Real)>&) const;

    py::class_<ExpSinhIntegral, Integrator,
               ext::shared_ptr<ExpSinhIntegral>>(
        m, "ExpSinhIntegral",
        "Exp-sinh quadrature for rapidly convergent integration of smooth functions.")
        .def(py::init<Real, Size>(),
            py::arg("relTolerance") = std::sqrt(std::numeric_limits<Real>::epsilon()),
            py::arg("maxRefinements") = 9,
            "Constructs with relative tolerance and max refinements.")
        .def("integrateHalfInfinite",
            static_cast<HalfInfiniteIntegrate>(&ExpSinhIntegral::integrate),
            py::arg("f"),
            "Integrates f(x) over the half-infinite interval [0, inf).");
}
