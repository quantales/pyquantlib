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
#include <ql/math/integrals/integral.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/functional.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_math::integrator(py::module_& m) {
    py::class_<Integrator, ext::shared_ptr<Integrator>>(
        m, "Integrator",
        "Abstract base class for 1-D numerical integrators.")
        .def("__call__", &Integrator::operator(),
            py::arg("f"), py::arg("a"), py::arg("b"),
            "Integrates function f from a to b.")
        .def("absoluteAccuracy", &Integrator::absoluteAccuracy,
            "Returns the required absolute accuracy.")
        .def("maxEvaluations", &Integrator::maxEvaluations,
            "Returns the maximum number of function evaluations.")
        .def("absoluteError", &Integrator::absoluteError,
            "Returns the absolute error of the last integration.")
        .def("numberOfEvaluations", &Integrator::numberOfEvaluations,
            "Returns the number of evaluations of the last integration.")
        .def("integrationSuccess", &Integrator::integrationSuccess,
            "Returns whether the last integration was successful.")
        .def("setAbsoluteAccuracy", &Integrator::setAbsoluteAccuracy,
            py::arg("accuracy"),
            "Sets the required absolute accuracy.")
        .def("setMaxEvaluations", &Integrator::setMaxEvaluations,
            py::arg("maxEvaluations"),
            "Sets the maximum number of function evaluations.");
}
