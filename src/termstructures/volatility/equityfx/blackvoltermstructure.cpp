/*
 * PyQuantLib: Python bindings for QuantLib
 * Copyright (c) 2025 Yassine Idyiahia
 *
 * QuantLib is Copyright (c) 2000-2025 The QuantLib Authors
 * QuantLib is free software under a modified BSD license.
 * See http://quantlib.org/ for more information.
 *
 * Source: https://github.com/quantales/pyquantlib
 * Licensed under the BSD 3-Clause License. See LICENSE file for details.
 */

#include "pyquantlib/pyquantlib.h"
#include "pyquantlib/trampolines.h"
#include <ql/termstructures/volatility/equityfx/blackvoltermstructure.hpp>
#include <ql/time/daycounters/actual365fixed.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_termstructures::blackvoltermstructure(py::module_& m) {
    // BlackVolTermStructure - base class for Black volatility term structures
    py::class_<BlackVolTermStructure, PyBlackVolTermStructure,
               ext::shared_ptr<BlackVolTermStructure>, VolatilityTermStructure>(
        m, "BlackVolTermStructure",
        "Abstract base class for Black volatility term structures.")
        // Constructors
        .def(py::init<const Date&, const Calendar&, BusinessDayConvention,
                      const DayCounter&>(),
            py::arg("referenceDate"),
            py::arg("calendar") = Calendar(),
            py::arg("businessDayConvention") = Following,
            py::arg("dayCounter") = Actual365Fixed(),
            "Constructs with reference date.")
        .def(py::init<Natural, const Calendar&, BusinessDayConvention,
                      const DayCounter&>(),
            py::arg("settlementDays"),
            py::arg("calendar"),
            py::arg("businessDayConvention") = Following,
            py::arg("dayCounter") = Actual365Fixed(),
            "Constructs with settlement days.")
        // Black volatility by date
        .def("blackVol",
            py::overload_cast<const Date&, Real, bool>(
                &BlackVolTermStructure::blackVol, py::const_),
            py::arg("date"), py::arg("strike"), py::arg("extrapolate") = false,
            "Returns the Black volatility for the given date and strike.")
        // Black volatility by time
        .def("blackVol",
            py::overload_cast<Time, Real, bool>(
                &BlackVolTermStructure::blackVol, py::const_),
            py::arg("time"), py::arg("strike"), py::arg("extrapolate") = false,
            "Returns the Black volatility for the given time and strike.")
        // Black variance by date
        .def("blackVariance",
            py::overload_cast<const Date&, Real, bool>(
                &BlackVolTermStructure::blackVariance, py::const_),
            py::arg("date"), py::arg("strike"), py::arg("extrapolate") = false,
            "Returns the Black variance for the given date and strike.")
        // Black variance by time
        .def("blackVariance",
            py::overload_cast<Time, Real, bool>(
                &BlackVolTermStructure::blackVariance, py::const_),
            py::arg("time"), py::arg("strike"), py::arg("extrapolate") = false,
            "Returns the Black variance for the given time and strike.")
        // Forward variance
        .def("blackForwardVol",
            py::overload_cast<const Date&, const Date&, Real, bool>(
                &BlackVolTermStructure::blackForwardVol, py::const_),
            py::arg("date1"), py::arg("date2"), py::arg("strike"),
            py::arg("extrapolate") = false,
            "Returns the Black forward volatility between two dates.")
        .def("blackForwardVol",
            py::overload_cast<Time, Time, Real, bool>(
                &BlackVolTermStructure::blackForwardVol, py::const_),
            py::arg("time1"), py::arg("time2"), py::arg("strike"),
            py::arg("extrapolate") = false,
            "Returns the Black forward volatility between two times.")
        .def("blackForwardVariance",
            py::overload_cast<const Date&, const Date&, Real, bool>(
                &BlackVolTermStructure::blackForwardVariance, py::const_),
            py::arg("date1"), py::arg("date2"), py::arg("strike"),
            py::arg("extrapolate") = false,
            "Returns the Black forward variance between two dates.")
        .def("blackForwardVariance",
            py::overload_cast<Time, Time, Real, bool>(
                &BlackVolTermStructure::blackForwardVariance, py::const_),
            py::arg("time1"), py::arg("time2"), py::arg("strike"),
            py::arg("extrapolate") = false,
            "Returns the Black forward variance between two times.");

    // BlackVolatilityTermStructure - adapter for volatility-based implementations
    py::class_<BlackVolatilityTermStructure, PyBlackVolatilityTermStructure,
               ext::shared_ptr<BlackVolatilityTermStructure>, BlackVolTermStructure>(
        m, "BlackVolatilityTermStructure",
        "Abstract adapter for Black volatility term structures (volatility-based).")
        .def(py::init<const Date&, const Calendar&, BusinessDayConvention,
                      const DayCounter&>(),
            py::arg("referenceDate"),
            py::arg("calendar") = Calendar(),
            py::arg("businessDayConvention") = Following,
            py::arg("dayCounter") = Actual365Fixed(),
            "Constructs with reference date.")
        .def(py::init<Natural, const Calendar&, BusinessDayConvention,
                      const DayCounter&>(),
            py::arg("settlementDays"),
            py::arg("calendar"),
            py::arg("businessDayConvention") = Following,
            py::arg("dayCounter") = Actual365Fixed(),
            "Constructs with settlement days.");

    // BlackVarianceTermStructure - adapter for variance-based implementations
    py::class_<BlackVarianceTermStructure, PyBlackVarianceTermStructure,
               ext::shared_ptr<BlackVarianceTermStructure>, BlackVolTermStructure>(
        m, "BlackVarianceTermStructure",
        "Abstract adapter for Black volatility term structures (variance-based).")
        .def(py::init<const Date&, const Calendar&, BusinessDayConvention,
                      const DayCounter&>(),
            py::arg("referenceDate"),
            py::arg("calendar") = Calendar(),
            py::arg("businessDayConvention") = Following,
            py::arg("dayCounter") = Actual365Fixed(),
            "Constructs with reference date.")
        .def(py::init<Natural, const Calendar&, BusinessDayConvention,
                      const DayCounter&>(),
            py::arg("settlementDays"),
            py::arg("calendar"),
            py::arg("businessDayConvention") = Following,
            py::arg("dayCounter") = Actual365Fixed(),
            "Constructs with settlement days.");
}

void ql_termstructures::blackvoltermstructurehandle(py::module_& m) {
    bindHandle<BlackVolTermStructure>(m, "BlackVolTermStructureHandle",
        "Handle to BlackVolTermStructure.");
}

void ql_termstructures::relinkableblackvoltermstructurehandle(py::module_& m) {
    bindRelinkableHandle<BlackVolTermStructure>(m, "RelinkableBlackVolTermStructureHandle",
        "Relinkable handle to BlackVolTermStructure.");
}
