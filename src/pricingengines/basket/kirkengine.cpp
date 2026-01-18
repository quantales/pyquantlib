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
#include <ql/pricingengines/basket/kirkengine.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_pricingengines::kirkengine(py::module_& m) {
    py::class_<KirkEngine, ext::shared_ptr<KirkEngine>, SpreadBlackScholesVanillaEngine>(
        m, "KirkEngine", "Kirk engine for spread option pricing on two futures.")
        .def(py::init<ext::shared_ptr<GeneralizedBlackScholesProcess>,
                      ext::shared_ptr<GeneralizedBlackScholesProcess>,
                      Real>(),
            py::arg("process1"), py::arg("process2"), py::arg("correlation"),
            "Constructs with two Black-Scholes processes and correlation.");
}
