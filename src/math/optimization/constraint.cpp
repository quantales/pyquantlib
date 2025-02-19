/*
 * PyQuantLib: Python bindings for QuantLib
 * Copyright (c) 2025 Yassine Idyiahia
 * 
 * QuantLib is Copyright (c) 2000-2025 The QuantLib Authors
 * QuantLib is free software under a modified BSD license.
 * See http://quantlib.org/ for more information.
 * 
 * Source: https://github.com/quantales/pyquantlib
 * Licensed under the BSD 3-Clause License. See LICENSE file for details.
 */

#include "pyquantlib/pyquantlib.h"
#include <ql/math/optimization/constraint.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_math::constraint(py::module_& m) {
    py::class_<Constraint>(m, "Constraint",
        "Abstract constraint for optimization.")
        .def("test", &Constraint::test,
            py::arg("params"),
            "Tests if parameters satisfy the constraint.")
        .def("empty", &Constraint::empty,
            "Returns true if the constraint is empty.");
}

void ql_math::constraints(py::module_& m) {
    py::class_<NoConstraint, Constraint>(m, "NoConstraint",
        "No constraint (always satisfied).")
        .def(py::init<>());

    py::class_<PositiveConstraint, Constraint>(m, "PositiveConstraint",
        "Constraint enforcing positive values.")
        .def(py::init<>());

    py::class_<BoundaryConstraint, Constraint>(m, "BoundaryConstraint",
        "Constraint enforcing values within bounds.")
        .def(py::init<Real, Real>(),
            py::arg("low"), py::arg("high"));

    py::class_<CompositeConstraint, Constraint>(m, "CompositeConstraint",
        "Composite of two constraints.")
        .def(py::init<const Constraint&, const Constraint&>(),
            py::arg("c1"), py::arg("c2"));
}
