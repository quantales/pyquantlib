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
#include <ql/termstructures/volatility/optionlet/optionletvolatilitystructure.hpp>
#include <ql/time/daycounters/actual365fixed.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_termstructures::optionletvolatilitystructure(py::module_& m) {
    py::class_<OptionletVolatilityStructure, PyOptionletVolatilityStructure,
               ext::shared_ptr<OptionletVolatilityStructure>, VolatilityTermStructure>(
        m, "OptionletVolatilityStructure",
        "Abstract base class for optionlet (caplet/floorlet) volatility structures.")
        // Constructors
        .def(py::init<BusinessDayConvention, const DayCounter&>(),
            py::arg("businessDayConvention") = Following,
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
        // Volatility by Period
        .def("volatility",
            py::overload_cast<const Period&, Rate, bool>(
                &OptionletVolatilityStructure::volatility, py::const_),
            py::arg("optionTenor"), py::arg("strike"),
            py::arg("extrapolate") = false,
            "Returns volatility for option tenor and strike.")
        // Volatility by Date
        .def("volatility",
            py::overload_cast<const Date&, Rate, bool>(
                &OptionletVolatilityStructure::volatility, py::const_),
            py::arg("optionDate"), py::arg("strike"),
            py::arg("extrapolate") = false,
            "Returns volatility for option date and strike.")
        // Volatility by Time
        .def("volatility",
            py::overload_cast<Time, Rate, bool>(
                &OptionletVolatilityStructure::volatility, py::const_),
            py::arg("optionTime"), py::arg("strike"),
            py::arg("extrapolate") = false,
            "Returns volatility for option time and strike.")
        // Black variance by Period
        .def("blackVariance",
            py::overload_cast<const Period&, Rate, bool>(
                &OptionletVolatilityStructure::blackVariance, py::const_),
            py::arg("optionTenor"), py::arg("strike"),
            py::arg("extrapolate") = false,
            "Returns Black variance for option tenor and strike.")
        // Black variance by Date
        .def("blackVariance",
            py::overload_cast<const Date&, Rate, bool>(
                &OptionletVolatilityStructure::blackVariance, py::const_),
            py::arg("optionDate"), py::arg("strike"),
            py::arg("extrapolate") = false,
            "Returns Black variance for option date and strike.")
        // Black variance by Time
        .def("blackVariance",
            py::overload_cast<Time, Rate, bool>(
                &OptionletVolatilityStructure::blackVariance, py::const_),
            py::arg("optionTime"), py::arg("strike"),
            py::arg("extrapolate") = false,
            "Returns Black variance for option time and strike.")
        // Smile section by Period
        .def("smileSection",
            py::overload_cast<const Period&, bool>(
                &OptionletVolatilityStructure::smileSection, py::const_),
            py::arg("optionTenor"), py::arg("extrapolate") = false,
            "Returns smile section for option tenor.")
        // Smile section by Date
        .def("smileSection",
            py::overload_cast<const Date&, bool>(
                &OptionletVolatilityStructure::smileSection, py::const_),
            py::arg("optionDate"), py::arg("extrapolate") = false,
            "Returns smile section for option date.")
        // Smile section by Time
        .def("smileSection",
            py::overload_cast<Time, bool>(
                &OptionletVolatilityStructure::smileSection, py::const_),
            py::arg("optionTime"), py::arg("extrapolate") = false,
            "Returns smile section for option time.")
        .def("volatilityType", &OptionletVolatilityStructure::volatilityType,
            "Returns the volatility type.")
        .def("displacement", &OptionletVolatilityStructure::displacement,
            "Returns the displacement for shifted lognormal volatilities.");
}

void ql_termstructures::optionletvolatilitystructurehandle(py::module_& m) {
    bindHandle<OptionletVolatilityStructure>(m,
        "OptionletVolatilityStructureHandle",
        "Handle to OptionletVolatilityStructure.");
}

void ql_termstructures::relinkableoptionletvolatilitystructurehandle(py::module_& m) {
    bindRelinkableHandle<OptionletVolatilityStructure>(m,
        "RelinkableOptionletVolatilityStructureHandle",
        "Relinkable handle to OptionletVolatilityStructure.");
}
