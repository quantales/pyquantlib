/*
 * PyQuantLib: Python bindings for QuantLib
 * https://github.com/quantales/pyquantlib
 *
 * Copyright (c) 2025 Yassine Idyiahia
 * SPDX-License-Identifier: BSD-3-Clause
 * See LICENSE for details.
 *
 * ---
 * QuantLib is free software distributed under its own modified BSD license,
 * and is copyright of its respective contributors.
 * https://www.quantlib.org/
 */

#include "pyquantlib/pyquantlib.h"
#include <ql/termstructures/volatility/capfloor/capfloortermvolcurve.hpp>
#include <ql/quote.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_termstructures::capfloortermvolcurve(py::module_& m) {
    // Diamond: LazyObject + CapFloorTermVolatilityStructure (both through Observable)
    py::classh<CapFloorTermVolCurve,
               LazyObject, CapFloorTermVolatilityStructure>(
        m, "CapFloorTermVolCurve",
        "Cap/floor at-the-money term volatility curve.")
        // Floating reference date, quoted volatilities
        .def(py::init<Natural, const Calendar&, BusinessDayConvention,
                      const std::vector<Period>&,
                      const std::vector<Handle<Quote>>&, const DayCounter&>(),
            py::arg("settlementDays"), py::arg("calendar"),
            py::arg("businessDayConvention"),
            py::arg("optionTenors"), py::arg("volatilities"),
            py::arg("dayCounter") = Actual365Fixed(),
            "Constructs from settlement days and quoted volatilities.")
        // Fixed reference date, quoted volatilities
        .def(py::init<const Date&, const Calendar&, BusinessDayConvention,
                      const std::vector<Period>&,
                      const std::vector<Handle<Quote>>&, const DayCounter&>(),
            py::arg("settlementDate"), py::arg("calendar"),
            py::arg("businessDayConvention"),
            py::arg("optionTenors"), py::arg("volatilities"),
            py::arg("dayCounter") = Actual365Fixed(),
            "Constructs from settlement date and quoted volatilities.")
        // Fixed reference date, fixed volatilities
        .def(py::init<const Date&, const Calendar&, BusinessDayConvention,
                      const std::vector<Period>&,
                      const std::vector<Volatility>&, const DayCounter&>(),
            py::arg("settlementDate"), py::arg("calendar"),
            py::arg("businessDayConvention"),
            py::arg("optionTenors"), py::arg("volatilities"),
            py::arg("dayCounter") = Actual365Fixed(),
            "Constructs from settlement date and fixed volatilities.")
        // Floating reference date, fixed volatilities
        .def(py::init<Natural, const Calendar&, BusinessDayConvention,
                      const std::vector<Period>&,
                      const std::vector<Volatility>&, const DayCounter&>(),
            py::arg("settlementDays"), py::arg("calendar"),
            py::arg("businessDayConvention"),
            py::arg("optionTenors"), py::arg("volatilities"),
            py::arg("dayCounter") = Actual365Fixed(),
            "Constructs from settlement days and fixed volatilities.")
        .def("optionTenors", &CapFloorTermVolCurve::optionTenors,
            py::return_value_policy::reference_internal,
            "Returns the option tenors.")
        .def("optionDates", &CapFloorTermVolCurve::optionDates,
            py::return_value_policy::reference_internal,
            "Returns the option dates.")
        .def("optionTimes", &CapFloorTermVolCurve::optionTimes,
            py::return_value_policy::reference_internal,
            "Returns the option times.")
        .def("maxDate", &CapFloorTermVolCurve::maxDate,
            "Returns the maximum date.")
        .def("minStrike", &CapFloorTermVolCurve::minStrike,
            "Returns the minimum strike.")
        .def("maxStrike", &CapFloorTermVolCurve::maxStrike,
            "Returns the maximum strike.");
}
