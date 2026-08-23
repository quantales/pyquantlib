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
#include <ql/cashflows/rateaveraging.hpp>
#include <ql/currency.hpp>
#include <ql/indexes/iborindex.hpp>
#include <ql/instruments/constnotionalcrosscurrencybasisswap.hpp>
#include <ql/time/schedule.hpp>
#include <ql/utilities/null.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_instruments::constnotionalcrosscurrencybasisswap(py::module_& m) {
    using CcyBasisSwap = ConstNotionalCrossCurrencyBasisSwap;

    py::class_<CcyBasisSwap::arguments, ConstNotionalCrossCurrencySwap::arguments,
               ext::shared_ptr<CcyBasisSwap::arguments>>(
        m, "ConstNotionalCrossCurrencyBasisSwapArguments",
        "Arguments for cross-currency basis swap pricing.")
        .def(py::init<>())
        .def_readwrite("paySpread", &CcyBasisSwap::arguments::paySpread)
        .def_readwrite("recSpread", &CcyBasisSwap::arguments::recSpread)
        .def("validate", &CcyBasisSwap::arguments::validate);

    py::class_<CcyBasisSwap::results, ConstNotionalCrossCurrencySwap::results,
               ext::shared_ptr<CcyBasisSwap::results>>(
        m, "ConstNotionalCrossCurrencyBasisSwapResults",
        "Results from cross-currency basis swap pricing.")
        .def(py::init<>())
        .def_readwrite("fairPaySpread", &CcyBasisSwap::results::fairPaySpread)
        .def_readwrite("fairRecSpread", &CcyBasisSwap::results::fairRecSpread)
        .def("reset", &CcyBasisSwap::results::reset);

    py::class_<CcyBasisSwap, ConstNotionalCrossCurrencySwap, ext::shared_ptr<CcyBasisSwap>>(
        m, "ConstNotionalCrossCurrencyBasisSwap",
        "Cross-currency basis swap: floating vs floating in two currencies.")
        .def(py::init([](Real payNominal, const Currency& payCurrency,
                         const Schedule& paySchedule,
                         const ext::shared_ptr<IborIndex>& payIndex,
                         Spread paySpread, Real payGearing,
                         Real recNominal, const Currency& recCurrency,
                         const Schedule& recSchedule,
                         const ext::shared_ptr<IborIndex>& recIndex,
                         Spread recSpread, Real recGearing,
                         Integer payPaymentLag, Integer recPaymentLag,
                         bool payCompoundSpread,
                         const py::object& payLookbackDays,
                         bool payObservationShift, Natural payLockoutDays,
                         RateAveraging::Type payAveragingMethod,
                         bool recCompoundSpread,
                         const py::object& recLookbackDays,
                         bool recObservationShift, Natural recLockoutDays,
                         RateAveraging::Type recAveragingMethod,
                         bool telescopicValueDates) {
            Natural payLb = Null<Natural>();
            if (!payLookbackDays.is_none())
                payLb = payLookbackDays.cast<Natural>();
            Natural recLb = Null<Natural>();
            if (!recLookbackDays.is_none())
                recLb = recLookbackDays.cast<Natural>();
            return ext::make_shared<CcyBasisSwap>(
                payNominal, payCurrency, paySchedule, payIndex, paySpread,
                payGearing, recNominal, recCurrency, recSchedule, recIndex,
                recSpread, recGearing, payPaymentLag, recPaymentLag,
                payCompoundSpread, payLb, payObservationShift, payLockoutDays,
                payAveragingMethod, recCompoundSpread, recLb,
                recObservationShift, recLockoutDays, recAveragingMethod,
                telescopicValueDates);
        }),
            py::arg("payNominal"), py::arg("payCurrency"),
            py::arg("paySchedule"), py::arg("payIndex"),
            py::arg("paySpread"), py::arg("payGearing"),
            py::arg("recNominal"), py::arg("recCurrency"),
            py::arg("recSchedule"), py::arg("recIndex"),
            py::arg("recSpread"), py::arg("recGearing"),
            py::arg("payPaymentLag") = 0,
            py::arg("recPaymentLag") = 0,
            py::arg("payCompoundSpread") = false,
            py::arg("payLookbackDays") = py::none(),
            py::arg("payObservationShift") = false,
            py::arg("payLockoutDays") = 0,
            py::arg("payAveragingMethod") = RateAveraging::Compound,
            py::arg("recCompoundSpread") = false,
            py::arg("recLookbackDays") = py::none(),
            py::arg("recObservationShift") = false,
            py::arg("recLockoutDays") = 0,
            py::arg("recAveragingMethod") = RateAveraging::Compound,
            py::arg("telescopicValueDates") = false,
            "Constructs a basis swap. Arguments after the gearings apply only "
            "to overnight legs.")
        // Pay leg inspectors
        .def("payNominal", &CcyBasisSwap::payNominal, "Returns the pay-leg notional.")
        .def("payCurrency", &CcyBasisSwap::payCurrency, "Returns the pay-leg currency.")
        .def("paySchedule", &CcyBasisSwap::paySchedule, "Returns the pay-leg schedule.")
        .def("payIndex", &CcyBasisSwap::payIndex, "Returns the pay-leg index.")
        .def("paySpread", &CcyBasisSwap::paySpread, "Returns the pay-leg spread.")
        .def("payGearing", &CcyBasisSwap::payGearing, "Returns the pay-leg gearing.")
        // Receive leg inspectors
        .def("recNominal", &CcyBasisSwap::recNominal, "Returns the receive-leg notional.")
        .def("recCurrency", &CcyBasisSwap::recCurrency, "Returns the receive-leg currency.")
        .def("recSchedule", &CcyBasisSwap::recSchedule, "Returns the receive-leg schedule.")
        .def("recIndex", &CcyBasisSwap::recIndex, "Returns the receive-leg index.")
        .def("recSpread", &CcyBasisSwap::recSpread, "Returns the receive-leg spread.")
        .def("recGearing", &CcyBasisSwap::recGearing, "Returns the receive-leg gearing.")
        // Engine-computed results
        .def("fairPaySpread", &CcyBasisSwap::fairPaySpread,
            "Returns the spread that makes the pay leg fair.")
        .def("fairRecSpread", &CcyBasisSwap::fairRecSpread,
            "Returns the spread that makes the receive leg fair.");
}
