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
#include <ql/pricingengines/basket/spreadblackscholesvanillaengine.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_pricingengines::spreadblackscholesvanillaengine(py::module_& m) {
    py::module_ base = m.def_submodule("base", "Abstract base classes");

    py::class_<SpreadBlackScholesVanillaEngine, PySpreadBlackScholesVanillaEngine,
        ext::shared_ptr<SpreadBlackScholesVanillaEngine>, BasketOption::engine>(
        base, "SpreadBlackScholesVanillaEngine",
        "Abstract base class for spread option pricing engines.")
        .def(py::init<ext::shared_ptr<GeneralizedBlackScholesProcess>,
                      ext::shared_ptr<GeneralizedBlackScholesProcess>,
                      Real>(),
            py::arg("process1"), py::arg("process2"), py::arg("correlation"),
            "Constructs with two Black-Scholes processes and correlation.");
}
