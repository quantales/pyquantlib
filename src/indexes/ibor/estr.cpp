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
#include <ql/indexes/ibor/estr.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_indexes::estr(py::module_& m) {
    py::class_<Estr, OvernightIndex, ext::shared_ptr<Estr>>(
        m, "Estr",
        "Euro Short-Term Rate (ESTR) index.")
        // Default constructor (no curve)
        .def(py::init<>(),
            "Constructs ESTR without forwarding curve.")
        // Handle constructor
        .def(py::init<const Handle<YieldTermStructure>&>(),
            py::arg("h"),
            "Constructs ESTR with forwarding term structure handle.")
        // Hidden handle constructor
        .def(py::init([](const ext::shared_ptr<YieldTermStructure>& curve) {
            return ext::make_shared<Estr>(Handle<YieldTermStructure>(curve));
        }),
            py::arg("forwardingTermStructure"),
            "Constructs ESTR with forwarding term structure.");
}
