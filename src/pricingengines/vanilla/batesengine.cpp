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
#include <ql/pricingengines/vanilla/batesengine.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_pricingengines::batesengine(py::module_& m) {
    py::class_<BatesEngine, AnalyticHestonEngine, ext::shared_ptr<BatesEngine>>(
        m, "BatesEngine",
        "Analytic pricing engine for the Bates model.")
        .def(py::init<const ext::shared_ptr<BatesModel>&, Size>(),
            py::arg("model"),
            py::arg("integrationOrder") = 144,
            "Constructs with Bates model and integration order.")
        .def(py::init<const ext::shared_ptr<BatesModel>&, Real, Size>(),
            py::arg("model"),
            py::arg("relTolerance"),
            py::arg("maxEvaluations"),
            "Constructs with Bates model, relative tolerance, and max evaluations.");
}
