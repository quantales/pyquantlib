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
#include <ql/math/integrals/trapezoidintegral.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_math::trapezoidintegral(py::module_& m) {
    py::class_<TrapezoidIntegral<Default>, Integrator,
               ext::shared_ptr<TrapezoidIntegral<Default>>>(
        m, "TrapezoidIntegral",
        "Integral of a 1-D function using the trapezoid formula.")
        .def(py::init<Real, Size>(),
            py::arg("accuracy"), py::arg("maxIterations"),
            "Constructs with target accuracy and maximum iterations.");

    py::class_<TrapezoidIntegral<MidPoint>, Integrator,
               ext::shared_ptr<TrapezoidIntegral<MidPoint>>>(
        m, "MidPointTrapezoidIntegral",
        "Integral of a 1-D function using the mid-point trapezoid formula.")
        .def(py::init<Real, Size>(),
            py::arg("accuracy"), py::arg("maxIterations"),
            "Constructs with target accuracy and maximum iterations.");
}
