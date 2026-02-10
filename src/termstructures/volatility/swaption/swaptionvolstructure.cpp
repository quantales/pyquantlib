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
#include "pyquantlib/trampolines.h"
#include <ql/termstructures/volatility/swaption/swaptionvolstructure.hpp>
#include <ql/time/daycounters/actual365fixed.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_termstructures::swaptionvolstructure(py::module_& m) {
    py::class_<SwaptionVolatilityStructure, PySwaptionVolatilityStructure,
               ext::shared_ptr<SwaptionVolatilityStructure>, VolatilityTermStructure>(
        m, "SwaptionVolatilityStructure",
        "Abstract base class for swaption volatility structures.")
        // Constructors
        .def(py::init<BusinessDayConvention, const DayCounter&>(),
            py::arg("businessDayConvention"),
            py::arg("dayCounter") = Actual365Fixed(),
            "Constructs with business day convention.")
        .def(py::init<const Date&, const Calendar&, BusinessDayConvention,
                      const DayCounter&>(),
            py::arg("referenceDate"),
            py::arg("calendar"),
            py::arg("businessDayConvention"),
            py::arg("dayCounter") = Actual365Fixed(),
            "Constructs with reference date.")
        .def(py::init<Natural, const Calendar&, BusinessDayConvention,
                      const DayCounter&>(),
            py::arg("settlementDays"),
            py::arg("calendar"),
            py::arg("businessDayConvention"),
            py::arg("dayCounter") = Actual365Fixed(),
            "Constructs with settlement days.")
        // Volatility by Period/Period
        .def("volatility",
            py::overload_cast<const Period&, const Period&, Rate, bool>(
                &SwaptionVolatilityStructure::volatility, py::const_),
            py::arg("optionTenor"), py::arg("swapTenor"),
            py::arg("strike"), py::arg("extrapolate") = false,
            "Returns volatility for option tenor and swap tenor.")
        // Volatility by Date/Period
        .def("volatility",
            py::overload_cast<const Date&, const Period&, Rate, bool>(
                &SwaptionVolatilityStructure::volatility, py::const_),
            py::arg("optionDate"), py::arg("swapTenor"),
            py::arg("strike"), py::arg("extrapolate") = false,
            "Returns volatility for option date and swap tenor.")
        // Volatility by Time/Time
        .def("volatility",
            py::overload_cast<Time, Time, Rate, bool>(
                &SwaptionVolatilityStructure::volatility, py::const_),
            py::arg("optionTime"), py::arg("swapLength"),
            py::arg("strike"), py::arg("extrapolate") = false,
            "Returns volatility for option time and swap length.")
        // Black variance by Period/Period
        .def("blackVariance",
            py::overload_cast<const Period&, const Period&, Rate, bool>(
                &SwaptionVolatilityStructure::blackVariance, py::const_),
            py::arg("optionTenor"), py::arg("swapTenor"),
            py::arg("strike"), py::arg("extrapolate") = false,
            "Returns Black variance for option tenor and swap tenor.")
        // Black variance by Date/Period
        .def("blackVariance",
            py::overload_cast<const Date&, const Period&, Rate, bool>(
                &SwaptionVolatilityStructure::blackVariance, py::const_),
            py::arg("optionDate"), py::arg("swapTenor"),
            py::arg("strike"), py::arg("extrapolate") = false,
            "Returns Black variance for option date and swap tenor.")
        // Black variance by Time/Time
        .def("blackVariance",
            py::overload_cast<Time, Time, Rate, bool>(
                &SwaptionVolatilityStructure::blackVariance, py::const_),
            py::arg("optionTime"), py::arg("swapLength"),
            py::arg("strike"), py::arg("extrapolate") = false,
            "Returns Black variance for option time and swap length.")
        // Shift by Period/Period
        .def("shift",
            py::overload_cast<const Period&, const Period&, bool>(
                &SwaptionVolatilityStructure::shift, py::const_),
            py::arg("optionTenor"), py::arg("swapTenor"),
            py::arg("extrapolate") = false,
            "Returns shift for option tenor and swap tenor.")
        // Shift by Date/Period
        .def("shift",
            py::overload_cast<const Date&, const Period&, bool>(
                &SwaptionVolatilityStructure::shift, py::const_),
            py::arg("optionDate"), py::arg("swapTenor"),
            py::arg("extrapolate") = false,
            "Returns shift for option date and swap tenor.")
        // Shift by Time/Time
        .def("shift",
            py::overload_cast<Time, Time, bool>(
                &SwaptionVolatilityStructure::shift, py::const_),
            py::arg("optionTime"), py::arg("swapLength"),
            py::arg("extrapolate") = false,
            "Returns shift for option time and swap length.")
        // Smile section by Period/Period
        .def("smileSection",
            py::overload_cast<const Period&, const Period&, bool>(
                &SwaptionVolatilityStructure::smileSection, py::const_),
            py::arg("optionTenor"), py::arg("swapTenor"),
            py::arg("extrapolate") = false,
            "Returns smile section for option tenor and swap tenor.")
        // Smile section by Date/Period
        .def("smileSection",
            py::overload_cast<const Date&, const Period&, bool>(
                &SwaptionVolatilityStructure::smileSection, py::const_),
            py::arg("optionDate"), py::arg("swapTenor"),
            py::arg("extrapolate") = false,
            "Returns smile section for option date and swap tenor.")
        // Smile section by Time/Time
        .def("smileSection",
            py::overload_cast<Time, Time, bool>(
                &SwaptionVolatilityStructure::smileSection, py::const_),
            py::arg("optionTime"), py::arg("swapLength"),
            py::arg("extrapolate") = false,
            "Returns smile section for option time and swap length.")
        // Limits
        .def("maxSwapTenor", &SwaptionVolatilityStructure::maxSwapTenor,
            "Returns the largest swap tenor for which vols can be returned.")
        .def("maxSwapLength", &SwaptionVolatilityStructure::maxSwapLength,
            "Returns the largest swap length for which vols can be returned.")
        // Utilities
        .def("swapLength",
            py::overload_cast<const Period&>(
                &SwaptionVolatilityStructure::swapLength, py::const_),
            py::arg("swapTenor"),
            "Converts swap tenor to swap length.")
        .def("swapLength",
            py::overload_cast<const Date&, const Date&>(
                &SwaptionVolatilityStructure::swapLength, py::const_),
            py::arg("start"), py::arg("end"),
            "Converts swap dates to swap length.")
        .def("volatilityType", &SwaptionVolatilityStructure::volatilityType,
            "Returns the volatility type.");
}

void ql_termstructures::swaptionvolstructurehandle(py::module_& m) {
    bindHandle<SwaptionVolatilityStructure>(m, "SwaptionVolatilityStructureHandle",
        "Handle to SwaptionVolatilityStructure.");
}

void ql_termstructures::relinkableswaptionvolstructurehandle(py::module_& m) {
    bindRelinkableHandle<SwaptionVolatilityStructure>(m,
        "RelinkableSwaptionVolatilityStructureHandle",
        "Relinkable handle to SwaptionVolatilityStructure.");
}
