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
#include <ql/math/interpolations/extrapolation.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_math::extrapolation(py::module_& m) {
    py::class_<Extrapolator, ext::shared_ptr<Extrapolator>>(m, "Extrapolator",
        "Base class for term structures supporting extrapolation.")
        .def("enableExtrapolation", &Extrapolator::enableExtrapolation,
            py::arg("b") = true,
            "Enables or disables extrapolation.")
        .def("disableExtrapolation", &Extrapolator::disableExtrapolation,
            py::arg("b") = true,
            "Disables or enables extrapolation.")
        .def("allowsExtrapolation", &Extrapolator::allowsExtrapolation,
            "Returns true if extrapolation is enabled.");
}
