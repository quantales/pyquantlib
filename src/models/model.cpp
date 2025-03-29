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
#include <ql/models/model.hpp>
#include <ql/math/optimization/constraint.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_models::model(py::module_& m) {
    py::module_ base = m.def_submodule("base", "Abstract base classes");

    py::class_<CalibratedModel, PyCalibratedModel, ext::shared_ptr<CalibratedModel>,
               Observer, Observable>(
        base, "CalibratedModel",
        "Abstract base class for calibrated models.")
        .def("calibrate", &CalibratedModel::calibrate,
            py::arg("instruments"),
            py::arg("method"),
            py::arg("endCriteria"),
            py::arg("constraint") = NoConstraint(),
            py::arg("weights") = std::vector<Real>(),
            py::arg("fixParameters") = std::vector<bool>(),
            "Calibrate model to market instruments.")
        .def("params", &CalibratedModel::params,
            "Returns model parameters.")
        .def("setParams", &CalibratedModel::setParams,
            py::arg("params"),
            "Sets model parameters.")
        .def("value", &CalibratedModel::value,
            py::arg("params"), py::arg("instruments"),
            "Returns objective function value.")
        .def("constraint", &CalibratedModel::constraint,
            "Returns parameter constraint.")
        .def("endCriteria", &CalibratedModel::endCriteria,
            "Returns end criteria from last calibration.")
        .def("problemValues", &CalibratedModel::problemValues,
            "Returns problem values from last calibration.")
        .def("functionEvaluation", &CalibratedModel::functionEvaluation,
            "Returns number of function evaluations.");
}
