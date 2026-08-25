/*
 * PyQuantLib: Python bindings for QuantLib
 * https://github.com/quantales/pyquantlib
 *
 * Copyright (c) 2025 Yassine Idyiahia
 * SPDX-License-Identifier: BSD-3-Clause
 * See LICENSE for details.
 *
 * ---
 * QuantLib is free software distributed under its own modified BSD license,
 * and is copyright of its respective contributors.
 * https://www.quantlib.org/
 */

#include "pyquantlib/pyquantlib.h"
#include <ql/indexes/ibor/shir.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_indexes::shir(py::module_& m) {
    py::class_<Shir, OvernightIndex, ext::shared_ptr<Shir>>(
        m, "Shir",
        "Shekel Overnight Interest Rate (SHIR) index, published by the Bank of Israel.")
        .def(py::init<>(),
            "Constructs Shir without forwarding curve.")
        .def(py::init<const Handle<YieldTermStructure>&>(),
            py::arg("h"),
            "Constructs Shir with forwarding term structure handle.")
        .def(py::init([](const ext::shared_ptr<YieldTermStructure>& curve) {
            return ext::make_shared<Shir>(Handle<YieldTermStructure>(curve));
        }),
            py::arg("forwardingTermStructure"),
            "Constructs Shir with forwarding term structure.");
}
