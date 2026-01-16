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
