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
#include <ql/indexes/ibor/nibor.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_indexes::nibor(py::module_& m) {
    py::class_<Nibor, IborIndex, ext::shared_ptr<Nibor>>(
        m, "Nibor",
        "NOK-NIBOR index published by Oslo Boers.")
        .def(py::init<const Period&>(),
            py::arg("tenor"),
            "Constructs NIBOR without forwarding curve.")
        .def(py::init<const Period&, const Handle<YieldTermStructure>&>(),
            py::arg("tenor"), py::arg("h"),
            "Constructs NIBOR with forwarding term structure handle.")
        .def(py::init([](const Period& tenor,
                         const ext::shared_ptr<YieldTermStructure>& curve) {
            return ext::make_shared<Nibor>(tenor, Handle<YieldTermStructure>(curve));
        }),
            py::arg("tenor"), py::arg("forwardingTermStructure"),
            "Constructs NIBOR with forwarding term structure.");
}
