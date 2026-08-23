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
#include <ql/instruments/constnotionalcrosscurrencyfixedvsfloatingswap.hpp>
#include <ql/instruments/swap.hpp>
#include <ql/time/calendar.hpp>
#include <ql/time/schedule.hpp>
#include <ql/utilities/null.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_instruments::constnotionalcrosscurrencyfixedvsfloatingswap(py::module_& m) {
    using CcyFixFloatSwap = ConstNotionalCrossCurrencyFixedVsFloatingSwap;

    py::class_<CcyFixFloatSwap::arguments,
               ConstNotionalCrossCurrencySwap::arguments,
               ext::shared_ptr<CcyFixFloatSwap::arguments>>(
        m, "ConstNotionalCrossCurrencyFixedVsFloatingSwapArguments",
        "Arguments for cross-currency fixed-vs-floating swap pricing.")
        .def(py::init<>())
        .def_readwrite("fixedRate", &CcyFixFloatSwap::arguments::fixedRate)
        .def_readwrite("spread", &CcyFixFloatSwap::arguments::spread)
        .def("validate", &CcyFixFloatSwap::arguments::validate);

    py::class_<CcyFixFloatSwap::results,
               ConstNotionalCrossCurrencySwap::results,
               ext::shared_ptr<CcyFixFloatSwap::results>>(
        m, "ConstNotionalCrossCurrencyFixedVsFloatingSwapResults",
        "Results from cross-currency fixed-vs-floating swap pricing.")
        .def(py::init<>())
        .def_readwrite("fairFixedRate", &CcyFixFloatSwap::results::fairFixedRate)
        .def_readwrite("fairSpread", &CcyFixFloatSwap::results::fairSpread)
        .def("reset", &CcyFixFloatSwap::results::reset);

    py::class_<CcyFixFloatSwap, ConstNotionalCrossCurrencySwap,
               ext::shared_ptr<CcyFixFloatSwap>>(
        m, "ConstNotionalCrossCurrencyFixedVsFloatingSwap",
        "Cross-currency swap paying a fixed rate in one currency against a "
        "floating rate in another.")
        .def(py::init([](Swap::Type type,
                         Real fixedNominal, const Currency& fixedCurrency,
                         const Schedule& fixedSchedule, Rate fixedRate,
                         const DayCounter& fixedDayCount,
                         BusinessDayConvention fixedPaymentBdc,
                         Natural fixedPaymentLag,
                         const Calendar& fixedPaymentCalendar,
                         Real floatNominal, const Currency& floatCurrency,
                         const Schedule& floatSchedule,
                         const ext::shared_ptr<IborIndex>& floatIndex,
                         Spread floatSpread,
                         BusinessDayConvention floatPaymentBdc,
                         Natural floatPaymentLag,
                         const Calendar& floatPaymentCalendar,
                         bool telescopicValueDates, bool floatCompoundSpread,
                         const py::object& floatLookbackDays,
                         bool floatObservationShift, Natural floatLockoutDays,
                         RateAveraging::Type floatAveragingMethod) {
            Natural lb = Null<Natural>();
            if (!floatLookbackDays.is_none())
                lb = floatLookbackDays.cast<Natural>();
            return ext::make_shared<CcyFixFloatSwap>(
                type, fixedNominal, fixedCurrency, fixedSchedule, fixedRate,
                fixedDayCount, fixedPaymentBdc, fixedPaymentLag,
                fixedPaymentCalendar, floatNominal, floatCurrency,
                floatSchedule, floatIndex, floatSpread, floatPaymentBdc,
                floatPaymentLag, floatPaymentCalendar, telescopicValueDates,
                floatCompoundSpread, lb, floatObservationShift,
                floatLockoutDays, floatAveragingMethod);
        }),
            py::arg("type"),
            py::arg("fixedNominal"), py::arg("fixedCurrency"),
            py::arg("fixedSchedule"), py::arg("fixedRate"),
            py::arg("fixedDayCount"), py::arg("fixedPaymentBdc"),
            py::arg("fixedPaymentLag"), py::arg("fixedPaymentCalendar"),
            py::arg("floatNominal"), py::arg("floatCurrency"),
            py::arg("floatSchedule"), py::arg("floatIndex"),
            py::arg("floatSpread"), py::arg("floatPaymentBdc"),
            py::arg("floatPaymentLag"), py::arg("floatPaymentCalendar"),
            py::arg("telescopicValueDates") = false,
            py::arg("floatCompoundSpread") = false,
            py::arg("floatLookbackDays") = py::none(),
            py::arg("floatObservationShift") = false,
            py::arg("floatLockoutDays") = 0,
            py::arg("floatAveragingMethod") = RateAveraging::Compound,
            "Constructs the swap. Arguments after the floating payment "
            "calendar apply only to overnight floating legs.")
        .def("type", &CcyFixFloatSwap::type,
            "Returns the swap type (Payer or Receiver).")
        .def("fixedNominal", &CcyFixFloatSwap::fixedNominal,
            "Returns the fixed-leg notional.")
        .def("fixedCurrency", &CcyFixFloatSwap::fixedCurrency,
            "Returns the fixed-leg currency.")
        .def("fixedSchedule", &CcyFixFloatSwap::fixedSchedule,
            "Returns the fixed-leg schedule.")
        .def("fixedRate", &CcyFixFloatSwap::fixedRate,
            "Returns the fixed rate.")
        .def("fixedDayCount", &CcyFixFloatSwap::fixedDayCount,
            "Returns the fixed-leg day counter.")
        .def("fixedPaymentBdc", &CcyFixFloatSwap::fixedPaymentBdc,
            "Returns the fixed-leg payment business day convention.")
        .def("fixedPaymentLag", &CcyFixFloatSwap::fixedPaymentLag,
            "Returns the fixed-leg payment lag.")
        .def("fixedPaymentCalendar", &CcyFixFloatSwap::fixedPaymentCalendar,
            "Returns the fixed-leg payment calendar.")
        .def("floatNominal", &CcyFixFloatSwap::floatNominal,
            "Returns the floating-leg notional.")
        .def("floatCurrency", &CcyFixFloatSwap::floatCurrency,
            "Returns the floating-leg currency.")
        .def("floatSchedule", &CcyFixFloatSwap::floatSchedule,
            "Returns the floating-leg schedule.")
        .def("floatIndex", &CcyFixFloatSwap::floatIndex,
            "Returns the floating-leg index.")
        .def("floatSpread", &CcyFixFloatSwap::floatSpread,
            "Returns the floating-leg spread.")
        .def("floatPaymentBdc", &CcyFixFloatSwap::floatPaymentBdc,
            "Returns the floating-leg payment business day convention.")
        .def("floatPaymentLag", &CcyFixFloatSwap::floatPaymentLag,
            "Returns the floating-leg payment lag.")
        .def("floatPaymentCalendar", &CcyFixFloatSwap::floatPaymentCalendar,
            "Returns the floating-leg payment calendar.")
        .def("floatCompoundSpread", &CcyFixFloatSwap::floatCompoundSpread,
            "Returns True if the spread is compounded daily.")
        .def("floatLookbackDays", &CcyFixFloatSwap::floatLookbackDays,
            "Returns the floating-leg lookback days.")
        .def("floatLockoutDays", &CcyFixFloatSwap::floatLockoutDays,
            "Returns the floating-leg lockout days.")
        .def("floatAveragingMethod", &CcyFixFloatSwap::floatAveragingMethod,
            "Returns the floating-leg averaging method.")
        .def("fairRate", &CcyFixFloatSwap::fairRate,
            "Returns the fixed rate that makes the swap fair.")
        .def("fairSpread", &CcyFixFloatSwap::fairSpread,
            "Returns the floating spread that makes the swap fair.");
}
