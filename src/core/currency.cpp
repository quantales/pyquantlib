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
#include <ql/currency.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/operators.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_core::currency(py::module_& m) {
    py::class_<Currency, ext::shared_ptr<Currency>>(m, "Currency",
        "Currency specification.")
        .def(py::init<>(),
            "Default constructor, creates an empty currency.")
        .def("name", &Currency::name,
            "Returns the full currency name, e.g., 'U.S. Dollar'.")
        .def("code", &Currency::code,
            "Returns the ISO 4217 three-letter code, e.g., 'USD'.")
        .def("numericCode", &Currency::numericCode,
            "Returns the ISO 4217 numeric code, e.g., 840.")
        .def("symbol", &Currency::symbol,
            "Returns the currency symbol, e.g., '$'.")
        .def("fractionSymbol", &Currency::fractionSymbol,
            "Returns the fraction symbol, e.g., 'c' for cents.")
        .def("fractionsPerUnit", &Currency::fractionsPerUnit,
            "Returns the number of fractional units per currency unit, e.g., 100.")
        .def("rounding", &Currency::rounding,
            "Returns the rounding convention for this currency.")
        .def("triangulationCurrency", &Currency::triangulationCurrency,
            "Returns the triangulation currency, if any.")
        .def("empty", &Currency::empty,
            "Returns true if this is an empty (uninitialized) currency.")
        .def(py::self == py::self)
        .def(py::self != py::self);
}
