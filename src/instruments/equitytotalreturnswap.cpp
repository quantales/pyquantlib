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
#include <ql/instruments/equitytotalreturnswap.hpp>
#include <ql/indexes/equityindex.hpp>
#include <ql/indexes/iborindex.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_instruments::equitytotalreturnswap(py::module_& m) {
    py::class_<EquityTotalReturnSwap, Swap, ext::shared_ptr<EquityTotalReturnSwap>>(
        m, "EquityTotalReturnSwap",
        "Equity total return swap.")
        // Constructor with IborIndex
        .def(py::init([](Swap::Type type, Real nominal, const Schedule& schedule,
                         const ext::shared_ptr<EquityIndex>& equityIndex,
                         const ext::shared_ptr<IborIndex>& interestRateIndex,
                         const DayCounter& dayCounter, Rate margin,
                         Real gearing, const py::object& paymentCalendar,
                         BusinessDayConvention paymentConvention,
                         Natural paymentDelay) {
            Calendar cal;
            if (!paymentCalendar.is_none())
                cal = paymentCalendar.cast<Calendar>();
            return ext::make_shared<EquityTotalReturnSwap>(
                type, nominal, schedule, equityIndex, interestRateIndex,
                dayCounter, margin, gearing, cal, paymentConvention, paymentDelay);
        }),
            py::arg("type"),
            py::arg("nominal"),
            py::arg("schedule"),
            py::arg("equityIndex"),
            py::arg("interestRateIndex"),
            py::arg("dayCounter"),
            py::arg("margin"),
            py::arg("gearing") = 1.0,
            py::arg("paymentCalendar") = py::none(),
            py::arg("paymentConvention") = Unadjusted,
            py::arg("paymentDelay") = 0,
            "Constructs an equity TRS with an IBOR interest rate leg.")
        // Constructor with OvernightIndex
        .def(py::init([](Swap::Type type, Real nominal, const Schedule& schedule,
                         const ext::shared_ptr<EquityIndex>& equityIndex,
                         const ext::shared_ptr<OvernightIndex>& interestRateIndex,
                         const DayCounter& dayCounter, Rate margin,
                         Real gearing, const py::object& paymentCalendar,
                         BusinessDayConvention paymentConvention,
                         Natural paymentDelay) {
            Calendar cal;
            if (!paymentCalendar.is_none())
                cal = paymentCalendar.cast<Calendar>();
            return ext::make_shared<EquityTotalReturnSwap>(
                type, nominal, schedule, equityIndex, interestRateIndex,
                dayCounter, margin, gearing, cal, paymentConvention, paymentDelay);
        }),
            py::arg("type"),
            py::arg("nominal"),
            py::arg("schedule"),
            py::arg("equityIndex"),
            py::arg("interestRateIndex"),
            py::arg("dayCounter"),
            py::arg("margin"),
            py::arg("gearing") = 1.0,
            py::arg("paymentCalendar") = py::none(),
            py::arg("paymentConvention") = Unadjusted,
            py::arg("paymentDelay") = 0,
            "Constructs an equity TRS with an overnight interest rate leg.")
        // Inspectors
        .def("type", &EquityTotalReturnSwap::type,
            "Returns the swap type (Payer or Receiver).")
        .def("nominal", &EquityTotalReturnSwap::nominal,
            "Returns the notional amount.")
        .def("equityIndex", &EquityTotalReturnSwap::equityIndex,
            "Returns the equity index.")
        .def("interestRateIndex", &EquityTotalReturnSwap::interestRateIndex,
            "Returns the interest rate index.")
        .def("schedule", &EquityTotalReturnSwap::schedule,
            py::return_value_policy::reference_internal,
            "Returns the payment schedule.")
        .def("dayCounter", &EquityTotalReturnSwap::dayCounter,
            py::return_value_policy::reference_internal,
            "Returns the day counter.")
        .def("margin", &EquityTotalReturnSwap::margin,
            "Returns the floating leg margin.")
        .def("gearing", &EquityTotalReturnSwap::gearing,
            "Returns the gearing factor.")
        .def("paymentCalendar", &EquityTotalReturnSwap::paymentCalendar,
            py::return_value_policy::reference_internal,
            "Returns the payment calendar.")
        .def("paymentConvention", &EquityTotalReturnSwap::paymentConvention,
            "Returns the payment business day convention.")
        .def("paymentDelay", &EquityTotalReturnSwap::paymentDelay,
            "Returns the payment delay in days.")
        // Legs
        .def("equityLeg", &EquityTotalReturnSwap::equityLeg,
            py::return_value_policy::reference_internal,
            "Returns the equity leg.")
        .def("interestRateLeg", &EquityTotalReturnSwap::interestRateLeg,
            py::return_value_policy::reference_internal,
            "Returns the interest rate leg.")
        // Results
        .def("equityLegNPV", &EquityTotalReturnSwap::equityLegNPV,
            "Returns the NPV of the equity leg.")
        .def("interestRateLegNPV", &EquityTotalReturnSwap::interestRateLegNPV,
            "Returns the NPV of the interest rate leg.")
        .def("fairMargin", &EquityTotalReturnSwap::fairMargin,
            "Returns the fair margin.");
}
