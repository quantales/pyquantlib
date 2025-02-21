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
#include "pyquantlib/trampolines.h"
#include <ql/math/optimization/costfunction.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_math::costfunction(py::module_& m) {
    py::class_<CostFunction, PyCostFunction, ext::shared_ptr<CostFunction>>(
        m, "CostFunction",
        "Abstract cost function for optimization.")
        .def(py::init_alias<>())
        .def("value", &CostFunction::value,
            py::arg("x"),
            "Returns the cost for the given parameters.")
        .def("values", &CostFunction::values,
            py::arg("x"),
            "Returns the cost values for the given parameters.");
}
