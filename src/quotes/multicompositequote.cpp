/*
 * PyQuantLib: Python bindings for QuantLib
 * https://github.com/quantales/pyquantlib
 *
 * Copyright (c) 2026 Yassine Idyiahia
 * SPDX-License-Identifier: BSD-3-Clause
 * See LICENSE for details.
 *
 * ---
 * QuantLib is free software distributed under its own modified BSD license,
 * and is copyright of its respective contributors.
 * https://www.quantlib.org/
 */

#include "pyquantlib/pyquantlib.h"
#include <ql/quotes/multicompositequote.hpp>
#include <ql/math/array.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

namespace {

// Wrapper to make a Python callable look like a C++ array function.
// The callable receives a list of the element values and returns a Real.
struct PyArrayFunction {
    py::function func;

    explicit PyArrayFunction(py::function f) : func(std::move(f)) {
        if (!func) {
            throw py::type_error("Invalid Python function.");
        }
    }

    Real operator()(Array values) const {
        try {
            py::list args;
            for (Real v : values)
                args.append(v);
            py::object result = func(args);
            return result.cast<Real>();
        } catch (const py::cast_error& e) {
            throw py::type_error(
                std::string("Python function failed to cast result to Real: ") + e.what());
        }
    }
};

using PyMultiCompositeQuote = MultiCompositeQuote<PyArrayFunction>;

}  // namespace

void ql_quotes::multicompositequote(py::module_& m) {
    py::class_<PyMultiCompositeQuote, Quote, ext::shared_ptr<PyMultiCompositeQuote>>(
        m, "MultiCompositeQuote",
        "Quote composed from several quotes using a function of their values.")
        .def(py::init([](const std::vector<Handle<Quote>>& elements, py::function f) {
                return ext::make_shared<PyMultiCompositeQuote>(elements, PyArrayFunction(f));
            }),
            py::arg("quotes"),
            py::arg("function"),
            "Creates a composite quote from a list of quotes and a Python function "
            "taking a list of their values.")
        .def("inputValue", &PyMultiCompositeQuote::inputValue, py::arg("i"),
            "Returns the value of the i-th input quote.");
}
