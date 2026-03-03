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
#include "pyquantlib/interpolation_helper.h"
#include <ql/math/interpolations/lagrangeinterpolation.hpp>

namespace py = pybind11;
using namespace QuantLib;

void ql_math::lagrangeinterpolation(py::module_& m) {
    py::class_<LagrangeInterpolation, Interpolation,
               ext::shared_ptr<LagrangeInterpolation>>(
        m, "LagrangeInterpolation",
        "Lagrange interpolation through discrete points.")
        .def(py::init([](std::vector<Real> x, std::vector<Real> y) {
            return pyquantlib::make_safe_interpolation<LagrangeInterpolation>(
                std::move(x), std::move(y), 2);
        }),
        py::arg("x"), py::arg("y"),
        "Constructs interpolation from x and y arrays.")
        .def("value", &LagrangeInterpolation::value,
            py::arg("y"), py::arg("x"),
            "Evaluates at x using alternative y values.");
}
