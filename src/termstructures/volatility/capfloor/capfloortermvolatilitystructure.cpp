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
#include <ql/termstructures/volatility/capfloor/capfloortermvolatilitystructure.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_termstructures::capfloortermvolatilitystructure(py::module_& m) {
    py::class_<CapFloorTermVolatilityStructure,
               ext::shared_ptr<CapFloorTermVolatilityStructure>,
               VolatilityTermStructure>(
        m, "CapFloorTermVolatilityStructure",
        "Abstract base class for cap/floor term volatility structures.")
        // Volatility by Period
        .def("volatility",
            py::overload_cast<const Period&, Rate, bool>(
                &CapFloorTermVolatilityStructure::volatility, py::const_),
            py::arg("optionTenor"), py::arg("strike"),
            py::arg("extrapolate") = false,
            "Returns volatility for option tenor and strike.")
        // Volatility by Date
        .def("volatility",
            py::overload_cast<const Date&, Rate, bool>(
                &CapFloorTermVolatilityStructure::volatility, py::const_),
            py::arg("optionDate"), py::arg("strike"),
            py::arg("extrapolate") = false,
            "Returns volatility for option date and strike.")
        // Volatility by Time
        .def("volatility",
            py::overload_cast<Time, Rate, bool>(
                &CapFloorTermVolatilityStructure::volatility, py::const_),
            py::arg("optionTime"), py::arg("strike"),
            py::arg("extrapolate") = false,
            "Returns volatility for option time and strike.");
}
