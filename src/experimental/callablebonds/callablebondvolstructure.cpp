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
#include <ql/experimental/callablebonds/callablebondvolstructure.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_experimental::callablebondvolstructure(py::module_& m) {
    auto base = py::module_::import("pyquantlib.base");

    // CallableBondVolatilityStructure (ABC)
    py::class_<CallableBondVolatilityStructure, TermStructure,
               ext::shared_ptr<CallableBondVolatilityStructure>>(
        base, "CallableBondVolatilityStructure",
        "Abstract base class for callable-bond volatility structures.")
        // Volatility (Time overload)
        .def("volatility",
            py::overload_cast<Time, Time, Rate, bool>(
                &CallableBondVolatilityStructure::volatility, py::const_),
            py::arg("optionTime"),
            py::arg("bondLength"),
            py::arg("strike"),
            py::arg("extrapolate") = false,
            "Returns the volatility for a given option time and bond length.")
        // Volatility (Date overload)
        .def("volatility",
            py::overload_cast<const Date&, const Period&, Rate, bool>(
                &CallableBondVolatilityStructure::volatility, py::const_),
            py::arg("optionDate"),
            py::arg("bondTenor"),
            py::arg("strike"),
            py::arg("extrapolate") = false,
            "Returns the volatility for a given option date and bond tenor.")
        // Black variance
        .def("blackVariance",
            py::overload_cast<Time, Time, Rate, bool>(
                &CallableBondVolatilityStructure::blackVariance, py::const_),
            py::arg("optionTime"),
            py::arg("bondLength"),
            py::arg("strike"),
            py::arg("extrapolate") = false,
            "Returns the Black variance.")
        // Limits
        .def("maxBondTenor", &CallableBondVolatilityStructure::maxBondTenor,
            py::return_value_policy::reference_internal,
            "Returns the maximum bond tenor.")
        .def("maxBondLength", &CallableBondVolatilityStructure::maxBondLength,
            "Returns the maximum bond length.")
        .def("minStrike", &CallableBondVolatilityStructure::minStrike,
            "Returns the minimum strike.")
        .def("maxStrike", &CallableBondVolatilityStructure::maxStrike,
            "Returns the maximum strike.");
}
