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
#include <ql/termstructures/yield/impliedtermstructure.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_termstructures::impliedtermstructure(py::module_& m) {
    py::class_<ImpliedTermStructure, YieldTermStructure,
               ext::shared_ptr<ImpliedTermStructure>>(
        m, "ImpliedTermStructure",
        "Implied yield term structure at a future reference date.")
        // Handle constructor
        .def(py::init<Handle<YieldTermStructure>, const Date&>(),
            py::arg("curveHandle"), py::arg("referenceDate"),
            "Constructs from yield curve handle and reference date.")
        // Hidden handle
        .def(py::init([](const ext::shared_ptr<YieldTermStructure>& curve,
                         const Date& referenceDate) {
            return ext::make_shared<ImpliedTermStructure>(
                Handle<YieldTermStructure>(curve), referenceDate);
        }),
            py::arg("curve"), py::arg("referenceDate"),
            "Constructs from yield curve and reference date (handle created internally).");
}
