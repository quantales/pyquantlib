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
#include "pyquantlib/binding_manager.h"
#include <ql/models/equity/hestonmodel.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_models::hestonmodel(py::module_& m) {
    py::class_<HestonModel, CalibratedModel, ext::shared_ptr<HestonModel>>(
        m, "HestonModel",
        "Heston stochastic volatility model.")
        .def(py::init<const ext::shared_ptr<HestonProcess>&>(),
             py::arg("process"),
            "Constructs Heston model from process.")
        .def("theta", &HestonModel::theta,
            "Returns long-term variance.")
        .def("kappa", &HestonModel::kappa,
            "Returns mean-reversion speed.")
        .def("sigma", &HestonModel::sigma,
            "Returns volatility of volatility.")
        .def("rho", &HestonModel::rho,
            "Returns correlation.")
        .def("v0", &HestonModel::v0,
            "Returns initial variance.");
}

void ql_models::hestonmodelhandle(py::module_& m) {
    bindHandle<HestonModel>(m, "HestonModelHandle",
        "Handle to HestonModel objects.");
}
