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
#include <ql/math/integrals/kronrodintegral.hpp>
#include <ql/utilities/null.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_math::kronrodintegral(py::module_& m) {
    py::class_<GaussKronrodAdaptive, Integrator,
               ext::shared_ptr<GaussKronrodAdaptive>>(
        m, "GaussKronrodAdaptive",
        "Adaptive Gauss-Kronrod integration using 15-point rule.")
        .def(py::init([](Real tolerance, const py::object& maxFunctionEvaluations) {
            Size maxEvals = maxFunctionEvaluations.is_none()
                ? Null<Size>()
                : maxFunctionEvaluations.cast<Size>();
            return ext::make_shared<GaussKronrodAdaptive>(tolerance, maxEvals);
        }),
        py::arg("tolerance"),
        py::arg("maxFunctionEvaluations") = py::none(),
        "Constructs with tolerance and optional max function evaluations.");

    py::class_<GaussKronrodNonAdaptive, Integrator,
               ext::shared_ptr<GaussKronrodNonAdaptive>>(
        m, "GaussKronrodNonAdaptive",
        "Non-adaptive Gauss-Kronrod integration using 10/21/43/87-point rules.")
        .def(py::init<Real, Size, Real>(),
            py::arg("absoluteAccuracy"),
            py::arg("maxEvaluations"),
            py::arg("relativeAccuracy"),
            "Constructs with absolute accuracy, max evaluations, and relative accuracy.")
        .def("relativeAccuracy", &GaussKronrodNonAdaptive::relativeAccuracy,
            "Returns the relative accuracy.");
}
