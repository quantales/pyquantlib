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
#include <ql/pricingengines/vanilla/cashdividendeuropeanengine.hpp>
#include <ql/processes/blackscholesprocess.hpp>
#include <ql/cashflows/dividend.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_pricingengines::cashdividendeuropeanengine(py::module_& m) {
    using Engine = CashDividendEuropeanEngine;

    // CashDividendModel enum (reused by FdBlackScholesVanillaEngine)
    py::enum_<Engine::CashDividendModel>(
        m, "CashDividendModel",
        "Cash dividend model type.")
        .value("Spot", Engine::Spot, "Spot dividend model.")
        .value("Escrowed", Engine::Escrowed, "Escrowed dividend model.")
        .export_values();

    py::class_<Engine, ext::shared_ptr<Engine>, PricingEngine>(
        m, "CashDividendEuropeanEngine",
        "Semi-analytic European engine with cash dividends (Healy, 2021).")
        .def(py::init<ext::shared_ptr<GeneralizedBlackScholesProcess>,
                      DividendSchedule,
                      Engine::CashDividendModel>(),
            py::arg("process"),
            py::arg("dividends"),
            py::arg("cashDividendModel") = Engine::Spot,
            "Constructs with process, dividend schedule, and model type.");
}
