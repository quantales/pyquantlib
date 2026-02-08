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
#include <ql/instruments/compositeinstrument.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_instruments::compositeinstrument(py::module_& m) {
    py::class_<CompositeInstrument, Instrument,
               ext::shared_ptr<CompositeInstrument>>(
        m, "CompositeInstrument",
        "Aggregate of instruments with weighted NPVs.")
        .def(py::init<>(), "Constructs an empty composite instrument.")
        .def("add", &CompositeInstrument::add,
            py::arg("instrument"),
            py::arg("multiplier") = 1.0,
            "Adds an instrument with a multiplier.")
        .def("subtract", &CompositeInstrument::subtract,
            py::arg("instrument"),
            py::arg("multiplier") = 1.0,
            "Subtracts an instrument with a multiplier.")
        .def("isExpired", &CompositeInstrument::isExpired,
            "Returns whether all components are expired.");
}
