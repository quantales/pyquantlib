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
#include <ql/math/integrals/segmentintegral.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_math::segmentintegral(py::module_& m) {
    py::class_<SegmentIntegral, Integrator, ext::shared_ptr<SegmentIntegral>>(
        m, "SegmentIntegral",
        "Integral of a 1-D function using the segment (trapezoid) algorithm.")
        .def(py::init<Size>(),
            py::arg("intervals"),
            "Constructs with the given number of intervals.");
}
