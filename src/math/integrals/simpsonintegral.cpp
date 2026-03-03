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
#include <ql/math/integrals/simpsonintegral.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_math::simpsonintegral(py::module_& m) {
    py::class_<SimpsonIntegral, TrapezoidIntegral<Default>, Integrator,
               ext::shared_ptr<SimpsonIntegral>>(
        m, "SimpsonIntegral",
        "Integral of a 1-D function using the Simpson formula.")
        .def(py::init<Real, Size>(),
            py::arg("accuracy"), py::arg("maxIterations"),
            "Constructs with target accuracy and maximum iterations.");
}
