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
#include <ql/pricingengines/vanilla/hestonexpansionengine.hpp>
#include <ql/models/equity/hestonmodel.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_pricingengines::hestonexpansionengine(py::module_& m) {
    py::enum_<HestonExpansionEngine::HestonExpansionFormula>(
        m, "HestonExpansionFormula",
        "Formula type for Heston expansion engine.")
        .value("LPP2", HestonExpansionEngine::LPP2)
        .value("LPP3", HestonExpansionEngine::LPP3)
        .value("Forde", HestonExpansionEngine::Forde);

    py::class_<HestonExpansionEngine,
               ext::shared_ptr<HestonExpansionEngine>,
               PricingEngine>(
        m, "HestonExpansionEngine",
        "Heston engine based on analytic expansions (LPP2, LPP3, Forde).")
        .def(py::init<const ext::shared_ptr<HestonModel>&,
                      HestonExpansionEngine::HestonExpansionFormula>(),
            py::arg("model"),
            py::arg("formula"),
            "Constructs Heston expansion engine.");
}
