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
#include <ql/indexes/ibor/eonia.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_indexes::eonia(py::module_& m) {
    py::class_<Eonia, OvernightIndex, ext::shared_ptr<Eonia>>(
        m, "Eonia",
        "Euro Overnight Index Average (EONIA) rate fixed by the ECB.")
        // Default constructor (no curve)
        .def(py::init<>(),
            "Constructs Eonia without forwarding curve.")
        // Handle constructor
        .def(py::init<const Handle<YieldTermStructure>&>(),
            py::arg("h"),
            "Constructs Eonia with forwarding term structure handle.")
        // Hidden handle constructor
        .def(py::init([](const ext::shared_ptr<YieldTermStructure>& curve) {
            return ext::make_shared<Eonia>(Handle<YieldTermStructure>(curve));
        }),
            py::arg("forwardingTermStructure"),
            "Constructs Eonia with forwarding term structure.");
}
