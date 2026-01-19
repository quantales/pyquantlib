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
#include <ql/models/equity/batesmodel.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_models::batesmodel(py::module_& m) {
    py::class_<BatesModel, HestonModel, ext::shared_ptr<BatesModel>>(
        m, "BatesModel",
        "Bates stochastic volatility model with jumps.")
        .def(py::init<const ext::shared_ptr<BatesProcess>&>(),
            py::arg("process"),
            "Constructs from a Bates process.")
        .def("nu", &BatesModel::nu, "Returns mean jump size.")
        .def("delta", &BatesModel::delta, "Returns jump size volatility.")
        .def("lambda_", &BatesModel::lambda, "Returns jump intensity.");
}
