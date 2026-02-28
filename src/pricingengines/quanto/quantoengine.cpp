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
#include <ql/exercise.hpp>
#include <ql/pricingengines/quanto/quantoengine.hpp>
#include <ql/pricingengines/vanilla/analyticeuropeanengine.hpp>
#include <ql/pricingengines/forward/forwardengine.hpp>
#include <ql/instruments/vanillaoption.hpp>
#include <ql/instruments/forwardvanillaoption.hpp>
#include <ql/processes/blackscholesprocess.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <ql/termstructures/volatility/equityfx/blackvoltermstructure.hpp>
#include <ql/quote.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_pricingengines::quantoengine(py::module_& m) {
    using QuantoVanillaEngine =
        QuantoEngine<VanillaOption, AnalyticEuropeanEngine>;

    py::class_<QuantoVanillaEngine, PricingEngine,
               ext::shared_ptr<QuantoVanillaEngine>>(
        m, "QuantoVanillaEngine",
        "Quanto European option engine (currency-adjusted Black-Scholes).")
        .def(py::init<ext::shared_ptr<GeneralizedBlackScholesProcess>,
                      Handle<YieldTermStructure>,
                      Handle<BlackVolTermStructure>,
                      Handle<Quote>>(),
             py::arg("process"),
             py::arg("foreignRiskFreeRate"),
             py::arg("exchangeRateVolatility"),
             py::arg("correlation"))
        // Hidden handle constructors
        .def(py::init([](const ext::shared_ptr<GeneralizedBlackScholesProcess>& process,
                         const ext::shared_ptr<YieldTermStructure>& foreignRate,
                         const ext::shared_ptr<BlackVolTermStructure>& fxVol,
                         const ext::shared_ptr<Quote>& correlation) {
                 return ext::make_shared<QuantoVanillaEngine>(
                     process,
                     Handle<YieldTermStructure>(foreignRate),
                     Handle<BlackVolTermStructure>(fxVol),
                     Handle<Quote>(correlation));
             }),
             py::arg("process"),
             py::arg("foreignRiskFreeRate"),
             py::arg("exchangeRateVolatility"),
             py::arg("correlation"),
             "Constructs from shared_ptr objects (handles created internally).");

    using QuantoForwardVanillaEngine =
        QuantoEngine<ForwardVanillaOption,
                     ForwardVanillaEngine<AnalyticEuropeanEngine>>;

    py::class_<QuantoForwardVanillaEngine, PricingEngine,
               ext::shared_ptr<QuantoForwardVanillaEngine>>(
        m, "QuantoForwardVanillaEngine",
        "Quanto forward-start European option engine.")
        .def(py::init<ext::shared_ptr<GeneralizedBlackScholesProcess>,
                      Handle<YieldTermStructure>,
                      Handle<BlackVolTermStructure>,
                      Handle<Quote>>(),
             py::arg("process"),
             py::arg("foreignRiskFreeRate"),
             py::arg("exchangeRateVolatility"),
             py::arg("correlation"))
        // Hidden handle constructor
        .def(py::init([](const ext::shared_ptr<GeneralizedBlackScholesProcess>& process,
                         const ext::shared_ptr<YieldTermStructure>& foreignRate,
                         const ext::shared_ptr<BlackVolTermStructure>& fxVol,
                         const ext::shared_ptr<Quote>& correlation) {
                 return ext::make_shared<QuantoForwardVanillaEngine>(
                     process,
                     Handle<YieldTermStructure>(foreignRate),
                     Handle<BlackVolTermStructure>(fxVol),
                     Handle<Quote>(correlation));
             }),
             py::arg("process"),
             py::arg("foreignRiskFreeRate"),
             py::arg("exchangeRateVolatility"),
             py::arg("correlation"),
             "Constructs from shared_ptr objects (handles created internally).");
}
