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
#include <ql/instruments/nonstandardswaption.hpp>
#include <ql/instruments/swaption.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_instruments::nonstandardswaption(py::module_& m) {
    py::class_<NonstandardSwaption, Option, ext::shared_ptr<NonstandardSwaption>>(
        m, "NonstandardSwaption",
        "Option to enter into a nonstandard swap.")
        // Constructor from Swaption
        .def(py::init<const Swaption&>(),
            py::arg("fromSwaption"),
            "Constructs from a standard swaption.")
        // Full constructor
        .def(py::init<ext::shared_ptr<NonstandardSwap>,
                      const ext::shared_ptr<Exercise>&,
                      Settlement::Type, Settlement::Method>(),
            py::arg("swap"),
            py::arg("exercise"),
            py::arg("delivery") = Settlement::Physical,
            py::arg("settlementMethod") = Settlement::PhysicalOTC,
            "Constructs a nonstandard swaption.")
        // Inspectors
        .def("settlementType", &NonstandardSwaption::settlementType,
            "Returns the settlement type.")
        .def("settlementMethod", &NonstandardSwaption::settlementMethod,
            "Returns the settlement method.")
        .def("type", &NonstandardSwaption::type,
            "Returns the underlying swap type.")
        .def("underlyingSwap", &NonstandardSwaption::underlyingSwap,
            py::return_value_policy::reference_internal,
            "Returns the underlying nonstandard swap.")
        .def("isExpired", &NonstandardSwaption::isExpired,
            "Returns True if the swaption has expired.");
}
