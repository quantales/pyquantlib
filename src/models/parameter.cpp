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
#include <ql/models/parameter.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_models::parameter(py::module_& m) {
    py::class_<Parameter, ext::shared_ptr<Parameter>>(
        m, "Parameter",
        "Model parameter with constraint.")
        .def(py::init<>())
        .def("params", &Parameter::params,
            "Returns parameter values.")
        .def("setParam", &Parameter::setParam,
            py::arg("i"), py::arg("x"),
            "Sets the i-th parameter value.")
        .def("testParams", &Parameter::testParams,
            py::arg("params"),
            "Tests if parameters satisfy constraint.")
        .def("constraint", &Parameter::constraint,
            "Returns the parameter constraint.")
        .def("size", &Parameter::size,
            "Returns number of parameters.")
        .def("__call__", &Parameter::operator(),
            py::arg("t"),
            "Returns parameter value at time t.");

    py::class_<ConstantParameter, Parameter, ext::shared_ptr<ConstantParameter>>(
        m, "ConstantParameter",
        "Time-constant parameter.")
        .def(py::init<const Constraint&>(),
             py::arg("constraint"))
        .def(py::init<Real, const Constraint&>(),
             py::arg("value"), py::arg("constraint"));
}
