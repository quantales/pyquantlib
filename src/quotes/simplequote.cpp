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
#include <ql/quotes/simplequote.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_quotes::simplequote(py::module_& m) {
    py::class_<SimpleQuote, Quote, ext::shared_ptr<SimpleQuote>>(m, "SimpleQuote",
        "Simple quote for market data.")
        .def(py::init<>(),
            "Constructs an invalid SimpleQuote.")
        .def(py::init<Real>(),
            py::arg("value"),
            "Constructs a SimpleQuote with the given value.")
        .def("value", &SimpleQuote::value,
            "Returns the current value.")
        .def("setValue", &SimpleQuote::setValue,
            py::arg("value"),
            "Sets the quote value and notifies observers.")
        .def("isValid", &SimpleQuote::isValid,
            "Returns true if the quote holds a valid value.")
        .def("reset", &SimpleQuote::reset,
            "Resets the quote to an invalid state.");
}
