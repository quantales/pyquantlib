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
#include <ql/termstructures/volatility/optionlet/constantoptionletvol.hpp>
#include <ql/quote.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_termstructures::constantoptionletvolatility(py::module_& m) {
    py::class_<ConstantOptionletVolatility, OptionletVolatilityStructure,
               ext::shared_ptr<ConstantOptionletVolatility>>(
        m, "ConstantOptionletVolatility",
        "Constant optionlet volatility, no time-strike dependence.")
        // Settlement days + fixed volatility
        .def(py::init<Natural, const Calendar&, BusinessDayConvention,
                      Volatility, const DayCounter&, VolatilityType, Real>(),
            py::arg("settlementDays"), py::arg("calendar"),
            py::arg("businessDayConvention"), py::arg("volatility"),
            py::arg("dayCounter"),
            py::arg("type") = ShiftedLognormal, py::arg("displacement") = 0.0,
            "Constructs from settlement days and constant volatility.")
        // Reference date + fixed volatility
        .def(py::init<const Date&, const Calendar&, BusinessDayConvention,
                      Volatility, const DayCounter&, VolatilityType, Real>(),
            py::arg("referenceDate"), py::arg("calendar"),
            py::arg("businessDayConvention"), py::arg("volatility"),
            py::arg("dayCounter"),
            py::arg("type") = ShiftedLognormal, py::arg("displacement") = 0.0,
            "Constructs from reference date and constant volatility.")
        // Settlement days + quote handle
        .def(py::init<Natural, const Calendar&, BusinessDayConvention,
                      Handle<Quote>, const DayCounter&, VolatilityType, Real>(),
            py::arg("settlementDays"), py::arg("calendar"),
            py::arg("businessDayConvention"), py::arg("volatility"),
            py::arg("dayCounter"),
            py::arg("type") = ShiftedLognormal, py::arg("displacement") = 0.0,
            "Constructs from settlement days and quote handle.")
        // Reference date + quote handle
        .def(py::init<const Date&, const Calendar&, BusinessDayConvention,
                      Handle<Quote>, const DayCounter&, VolatilityType, Real>(),
            py::arg("referenceDate"), py::arg("calendar"),
            py::arg("businessDayConvention"), py::arg("volatility"),
            py::arg("dayCounter"),
            py::arg("type") = ShiftedLognormal, py::arg("displacement") = 0.0,
            "Constructs from reference date and quote handle.")
        // Settlement days + quote (hidden handle)
        .def(py::init([](Natural settlementDays, const Calendar& calendar,
                         BusinessDayConvention bdc,
                         const ext::shared_ptr<Quote>& volatility,
                         const DayCounter& dayCounter,
                         VolatilityType type, Real displacement) {
            return ext::make_shared<ConstantOptionletVolatility>(
                settlementDays, calendar, bdc,
                Handle<Quote>(volatility), dayCounter, type, displacement);
        }), py::arg("settlementDays"), py::arg("calendar"),
            py::arg("businessDayConvention"), py::arg("volatility"),
            py::arg("dayCounter"),
            py::arg("type") = ShiftedLognormal, py::arg("displacement") = 0.0,
            "Constructs from settlement days and quote (handle created internally).")
        // Reference date + quote (hidden handle)
        .def(py::init([](const Date& referenceDate, const Calendar& calendar,
                         BusinessDayConvention bdc,
                         const ext::shared_ptr<Quote>& volatility,
                         const DayCounter& dayCounter,
                         VolatilityType type, Real displacement) {
            return ext::make_shared<ConstantOptionletVolatility>(
                referenceDate, calendar, bdc,
                Handle<Quote>(volatility), dayCounter, type, displacement);
        }), py::arg("referenceDate"), py::arg("calendar"),
            py::arg("businessDayConvention"), py::arg("volatility"),
            py::arg("dayCounter"),
            py::arg("type") = ShiftedLognormal, py::arg("displacement") = 0.0,
            "Constructs from reference date and quote (handle created internally).");
}
