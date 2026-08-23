/*
 * PyQuantLib: Python bindings for QuantLib
 * https://github.com/quantales/pyquantlib
 *
 * Copyright (c) 2026 Yassine Idyiahia
 * SPDX-License-Identifier: BSD-3-Clause
 * See LICENSE for details.
 *
 * ---
 * QuantLib is free software distributed under its own modified BSD license,
 * and is copyright of its respective contributors.
 * https://www.quantlib.org/
 */

#include "pyquantlib/pyquantlib.h"
#include <ql/currency.hpp>
#include <ql/optional.hpp>
#include <ql/pricingengines/swap/discountingconstnotionalcrosscurrencyswapengine.hpp>
#include <ql/quote.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_pricingengines::discountingconstnotionalcrosscurrencyswapengine(
        py::module_& m) {
    using CcySwapEngine = DiscountingConstNotionalCrossCurrencySwapEngine;

    py::class_<CcySwapEngine, PricingEngine, ext::shared_ptr<CcySwapEngine>>(
        m, "DiscountingConstNotionalCrossCurrencySwapEngine",
        "Prices a cross-currency swap by discounting each leg on its own "
        "currency curve. The NPV is expressed in the domestic currency.")
        // Explicit handles
        .def(py::init([](const Currency& domesticCcy,
                         const Handle<YieldTermStructure>& domesticCurve,
                         const Currency& foreignCcy,
                         const Handle<YieldTermStructure>& foreignCurve,
                         const Handle<Quote>& spotFX,
                         const py::object& includeSettlementDateFlows,
                         const Date& settlementDate, const Date& npvDate,
                         const Date& spotFXSettleDate) {
            ext::optional<bool> include;
            if (!includeSettlementDateFlows.is_none())
                include = includeSettlementDateFlows.cast<bool>();
            return ext::make_shared<CcySwapEngine>(
                domesticCcy, domesticCurve, foreignCcy, foreignCurve, spotFX,
                include, settlementDate, npvDate, spotFXSettleDate);
        }),
            py::arg("domesticCurrency"),
            py::arg("domesticCurrencyDiscountCurve"),
            py::arg("foreignCurrency"),
            py::arg("foreignCurrencyDiscountCurve"),
            py::arg("spotFX"),
            py::arg("includeSettlementDateFlows") = py::none(),
            py::arg("settlementDate") = Date(),
            py::arg("npvDate") = Date(),
            py::arg("spotFXSettleDate") = Date(),
            "Constructs from the two discount curves and the spot FX quote "
            "(domestic units per unit of foreign).")
        // Hidden handles
        .def(py::init([](const Currency& domesticCcy,
                         const ext::shared_ptr<YieldTermStructure>& domesticCurve,
                         const Currency& foreignCcy,
                         const ext::shared_ptr<YieldTermStructure>& foreignCurve,
                         const ext::shared_ptr<Quote>& spotFX,
                         const py::object& includeSettlementDateFlows,
                         const Date& settlementDate, const Date& npvDate,
                         const Date& spotFXSettleDate) {
            ext::optional<bool> include;
            if (!includeSettlementDateFlows.is_none())
                include = includeSettlementDateFlows.cast<bool>();
            return ext::make_shared<CcySwapEngine>(
                domesticCcy, Handle<YieldTermStructure>(domesticCurve),
                foreignCcy, Handle<YieldTermStructure>(foreignCurve),
                Handle<Quote>(spotFX), include, settlementDate, npvDate,
                spotFXSettleDate);
        }),
            py::arg("domesticCurrency"),
            py::arg("domesticCurrencyDiscountCurve"),
            py::arg("foreignCurrency"),
            py::arg("foreignCurrencyDiscountCurve"),
            py::arg("spotFX"),
            py::arg("includeSettlementDateFlows") = py::none(),
            py::arg("settlementDate") = Date(),
            py::arg("npvDate") = Date(),
            py::arg("spotFXSettleDate") = Date(),
            "Constructs from curves and spot quote (handles created internally).")
        // Inspectors
        .def("domesticCurrency", &CcySwapEngine::domesticCurrency,
            "Returns the domestic currency.")
        .def("foreignCurrency", &CcySwapEngine::foreignCurrency,
            "Returns the foreign currency.")
        .def("domesticCcyDiscountCurve", &CcySwapEngine::domesticCcyDiscountCurve,
            "Returns the domestic-currency discount curve handle.")
        .def("foreignCcyDiscountCurve", &CcySwapEngine::foreignCcyDiscountCurve,
            "Returns the foreign-currency discount curve handle.")
        .def("spotFX", &CcySwapEngine::spotFX,
            "Returns the spot FX quote handle.");
}
