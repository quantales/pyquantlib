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
#include <ql/instruments/callabilityschedule.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_instruments::callability(py::module_& m) {
    // Callability::Type enum
    py::enum_<Callability::Type>(m, "CallabilityType",
        "Callability type: Call or Put.")
        .value("Call", Callability::Call)
        .value("Put", Callability::Put);

    // Callability class
    py::class_<Callability, Event, ext::shared_ptr<Callability>>(
        m, "Callability",
        "Instrument callability (call or put) at a given date.")
        .def(py::init<const Bond::Price&, Callability::Type, const Date&>(),
            py::arg("price"),
            py::arg("type"),
            py::arg("date"),
            "Constructs a callability.")
        .def("price", &Callability::price,
            py::return_value_policy::reference_internal,
            "Returns the call/put price.")
        .def("type", &Callability::type,
            "Returns the callability type (Call or Put).")
        .def("date", &Callability::date,
            "Returns the call/put date.");
}
