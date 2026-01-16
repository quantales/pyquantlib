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
#include <ql/math/optimization/problem.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_math::problem(py::module_& m) {
    py::class_<Problem, ext::shared_ptr<Problem>>(m, "Problem",
        "Constrained optimization problem.")
        .def(py::init<CostFunction&, Constraint&, const Array&>(),
            py::arg("costFunction"),
            py::arg("constraint"),
            py::arg("initialValue"),
            py::keep_alive<1, 2>(),  // CostFunction must outlive Problem
            py::keep_alive<1, 3>(),  // Constraint must outlive Problem
            "Creates an optimization problem.")
        .def("currentValue", &Problem::currentValue,
            py::return_value_policy::reference_internal,
            "Returns the current parameter values.")
        .def("functionValue", &Problem::functionValue,
            "Returns the current function value.")
        .def("value", &Problem::value,
            py::arg("x"),
            "Evaluates the cost function at the given point.")
        .def("values", &Problem::values,
            py::arg("x"),
            "Evaluates the cost function values at the given point.")
        .def("constraint", &Problem::constraint,
            py::return_value_policy::reference_internal,
            "Returns the constraint.")
        .def("costFunction", &Problem::costFunction,
            py::return_value_policy::reference_internal,
            "Returns the cost function.");
}
