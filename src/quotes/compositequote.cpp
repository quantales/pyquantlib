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
#include <ql/quotes/compositequote.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/functional.h>

namespace py = pybind11;
using namespace QuantLib;

namespace {

// Wrapper to make Python callable look like a C++ binary function
struct PyBinaryFunction {
    py::function func;

    explicit PyBinaryFunction(py::function f) : func(std::move(f)) {
        if (!func) {
            throw py::type_error("Invalid Python function.");
        }
    }

    Real operator()(Real x, Real y) const {
        try {
            py::object result = func(x, y);
            return result.cast<Real>();
        } catch (const py::cast_error& e) {
            throw py::type_error(
                std::string("Python function failed to cast result to Real: ") + e.what());
        }
    }
};

using PyCompositeQuote = CompositeQuote<PyBinaryFunction>;

}  // namespace

void ql_quotes::compositequote(py::module_& m) {
    py::class_<PyCompositeQuote, Quote, ext::shared_ptr<PyCompositeQuote>>(m, "CompositeQuote",
        "Quote composed from two quotes using a binary function.")
        .def(py::init([](const Handle<Quote>& h1, const Handle<Quote>& h2, py::function f) {
                return ext::make_shared<PyCompositeQuote>(h1, h2, PyBinaryFunction(f));
            }),
            py::arg("quote1"),
            py::arg("quote2"),
            py::arg("function"),
            "Creates a composite quote from two quotes and a Python function.");
}
