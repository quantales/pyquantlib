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
#include "pyquantlib/trampolines.h"
#include "pyquantlib/binding_manager.h"
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

    // ShortRateModel ABC
    py::class_<ShortRateModel, CalibratedModel, ext::shared_ptr<ShortRateModel>>(
        base, "ShortRateModel",
        "Abstract base class for short-rate models.")
        .def("tree", &ShortRateModel::tree,
            py::arg("grid"),
            "Returns a lattice for the given time grid.");

    // Handle<ShortRateModel>
    bindHandle<ShortRateModel>(m, "ShortRateModelHandle",
        "Handle to a short-rate model.");

    // RelinkableHandle<ShortRateModel>
    bindRelinkableHandle<ShortRateModel>(m, "RelinkableShortRateModelHandle",
        "Relinkable handle to a short-rate model.");            
}
