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
#include <ql/models/equity/gjrgarchmodel.hpp>
#include <ql/processes/gjrgarchprocess.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_models::gjrgarchmodel(py::module_& m) {
    py::class_<GJRGARCHModel, CalibratedModel,
               ext::shared_ptr<GJRGARCHModel>>(
        m, "GJRGARCHModel",
        "GJR-GARCH(1,1) calibrated model.")
        .def(py::init<const ext::shared_ptr<GJRGARCHProcess>&>(),
             py::arg("process"))
        .def("omega", &GJRGARCHModel::omega,
             "Returns omega (variance mean reversion level).")
        .def("alpha", &GJRGARCHModel::alpha,
             "Returns alpha (impact of all innovations).")
        .def("beta", &GJRGARCHModel::beta,
             "Returns beta (impact of previous variance).")
        .def("gamma", &GJRGARCHModel::gamma,
             "Returns gamma (impact of negative innovations).")
        .def("lambda_", [](const GJRGARCHModel& m) { return m.lambda(); },
             "Returns lambda (market price of risk).")
        .def("v0", &GJRGARCHModel::v0,
             "Returns spot variance.")
        .def("process", &GJRGARCHModel::process,
             "Returns the underlying process.");
}
