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
#include <ql/quote.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_core::quote(py::module_& m) {
    py::class_<Quote, PyQuote, ext::shared_ptr<Quote>, Observable>(m, "Quote",
        "Abstract base class for market quotes.")
        .def("value", &Quote::value,
             "Returns the current value of the quote.")
        .def("isValid", &Quote::isValid,
             "Returns true if the quote holds a valid value.");
}

void ql_core::quotehandle(py::module_& m) {
    bindHandle<Quote>(m, "QuoteHandle", "Handle to Quote objects");
}

void ql_core::relinkablequotehandle(py::module_& m) {
    bindRelinkableHandle<Quote>(m, "RelinkableQuoteHandle",
                                "Relinkable handle to Quote objects");
}
