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
#include <ql/quotes/derivedquote.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/functional.h>

namespace py = pybind11;
using namespace QuantLib;

namespace {

// Wrapper to make Python callable look like a C++ unary function
struct PyUnaryFunction {
    py::function func;

    explicit PyUnaryFunction(py::function f) : func(std::move(f)) {
        if (!func) {
            throw py::type_error("Invalid Python function.");
        }
    }

    Real operator()(Real x) const {
        try {
            py::object result = func(x);
            return result.cast<Real>();
        } catch (const py::cast_error& e) {
            throw py::type_error(
                std::string("Python function failed to cast result to Real: ") + e.what());
        }
    }
};

using PyDerivedQuote = DerivedQuote<PyUnaryFunction>;

}  // namespace

void ql_quotes::derivedquote(py::module_& m) {
    py::class_<PyDerivedQuote, Quote, ext::shared_ptr<PyDerivedQuote>>(m, "DerivedQuote",
        "Quote derived from another quote using a unary function.")
        .def(py::init([](const Handle<Quote>& h, py::function f) {
                return ext::make_shared<PyDerivedQuote>(h, PyUnaryFunction(f));
            }),
            py::arg("quote"),
            py::arg("function"),
            "Creates a derived quote from another quote and a Python function.");
}
