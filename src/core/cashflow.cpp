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
#include <ql/cashflow.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_core::cashflow(py::module_& m) {
    py::class_<Event, PyEvent, ext::shared_ptr<Event>, Observable>(m, "Event",
        "Abstract base class for events with a date.")
        .def(py::init_alias<>())
        .def("date", &Event::date,
            "Returns the date of the event.");

    py::class_<CashFlow, PyCashFlow, ext::shared_ptr<CashFlow>, Event, LazyObject>(m, "CashFlow",
        "Abstract base class for a single cash flow.")
        .def(py::init_alias<>())
        .def("amount", &CashFlow::amount,
            "Returns the cash flow amount.")
        .def("hasOccurred", &CashFlow::hasOccurred,
            py::arg("refDate") = Date(),
            py::arg("includeRefDate") = py::none(),
            "Returns true if the cash flow has occurred by the reference date.");
}
