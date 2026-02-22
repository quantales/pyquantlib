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
#include <ql/instruments/floatfloatswaption.hpp>
#include <ql/instruments/swaption.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_instruments::floatfloatswaption(py::module_& m) {
    py::class_<FloatFloatSwaption, Option, ext::shared_ptr<FloatFloatSwaption>>(
        m, "FloatFloatSwaption",
        "Option to enter into a float-float swap.")
        .def(py::init<ext::shared_ptr<FloatFloatSwap>,
                      const ext::shared_ptr<Exercise>&,
                      Settlement::Type, Settlement::Method>(),
            py::arg("swap"),
            py::arg("exercise"),
            py::arg("delivery") = Settlement::Physical,
            py::arg("settlementMethod") = Settlement::PhysicalOTC,
            "Constructs a float-float swaption.")
        // Inspectors
        .def("settlementType", &FloatFloatSwaption::settlementType,
            "Returns the settlement type.")
        .def("settlementMethod", &FloatFloatSwaption::settlementMethod,
            "Returns the settlement method.")
        .def("type", &FloatFloatSwaption::type,
            "Returns the underlying swap type.")
        .def("underlyingSwap", &FloatFloatSwaption::underlyingSwap,
            py::return_value_policy::reference_internal,
            "Returns the underlying float-float swap.")
        .def("isExpired", &FloatFloatSwaption::isExpired,
            "Returns True if the swaption has expired.");
}
