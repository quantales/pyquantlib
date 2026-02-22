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
#include <ql/experimental/callablebonds/callablebondconstantvol.hpp>
#include <ql/quote.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_experimental::callablebondconstantvol(py::module_& m) {
    py::class_<CallableBondConstantVolatility, CallableBondVolatilityStructure,
               ext::shared_ptr<CallableBondConstantVolatility>>(
        m, "CallableBondConstantVolatility",
        "Constant callable-bond volatility.")
        // Constructor: reference date + scalar vol
        .def(py::init<const Date&, Volatility, DayCounter>(),
            py::arg("referenceDate"),
            py::arg("volatility"),
            py::arg("dayCounter"),
            "Constructs with reference date and scalar volatility.")
        // Constructor: reference date + Handle<Quote> vol
        .def(py::init<const Date&, Handle<Quote>, DayCounter>(),
            py::arg("referenceDate"),
            py::arg("volatility"),
            py::arg("dayCounter"),
            "Constructs with reference date and quoted volatility.")
        // Constructor: settlement days + scalar vol
        .def(py::init<Natural, const Calendar&, Volatility, DayCounter>(),
            py::arg("settlementDays"),
            py::arg("calendar"),
            py::arg("volatility"),
            py::arg("dayCounter"),
            "Constructs with settlement days and scalar volatility.")
        // Constructor: settlement days + Handle<Quote> vol
        .def(py::init<Natural, const Calendar&, Handle<Quote>, DayCounter>(),
            py::arg("settlementDays"),
            py::arg("calendar"),
            py::arg("volatility"),
            py::arg("dayCounter"),
            "Constructs with settlement days and quoted volatility.")
        // Hidden handle constructors
        .def(py::init([](const Date& referenceDate,
                         const ext::shared_ptr<Quote>& volatility,
                         const DayCounter& dayCounter) {
            return ext::make_shared<CallableBondConstantVolatility>(
                referenceDate, Handle<Quote>(volatility), dayCounter);
        }),
            py::arg("referenceDate"),
            py::arg("volatility"),
            py::arg("dayCounter"),
            "Constructs with reference date and quote (handle created internally).")
        .def(py::init([](Natural settlementDays, const Calendar& calendar,
                         const ext::shared_ptr<Quote>& volatility,
                         const DayCounter& dayCounter) {
            return ext::make_shared<CallableBondConstantVolatility>(
                settlementDays, calendar, Handle<Quote>(volatility), dayCounter);
        }),
            py::arg("settlementDays"),
            py::arg("calendar"),
            py::arg("volatility"),
            py::arg("dayCounter"),
            "Constructs with settlement days and quote (handle created internally).");
}
