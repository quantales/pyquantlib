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
#include <ql/indexes/ibor/zaronia.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_indexes::zaronia(py::module_& m) {
    py::class_<Zaronia, OvernightIndex, ext::shared_ptr<Zaronia>>(
        m, "Zaronia",
        "South African Rand Overnight Index Average (ZARONIA) index.")
        .def(py::init<>(),
            "Constructs Zaronia without forwarding curve.")
        .def(py::init<const Handle<YieldTermStructure>&>(),
            py::arg("h"),
            "Constructs Zaronia with forwarding term structure handle.")
        .def(py::init([](const ext::shared_ptr<YieldTermStructure>& curve) {
            return ext::make_shared<Zaronia>(Handle<YieldTermStructure>(curve));
        }),
            py::arg("forwardingTermStructure"),
            "Constructs Zaronia with forwarding term structure.");
}
