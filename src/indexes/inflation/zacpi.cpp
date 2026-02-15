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
#include <ql/indexes/inflation/zacpi.hpp>
#include <ql/termstructures/inflationtermstructure.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_indexes::zacpi(py::module_& m) {
    // ZACPI - South African CPI (zero inflation)
    py::class_<ZACPI, ZeroInflationIndex, ext::shared_ptr<ZACPI>>(
        m, "ZACPI", "South African Consumer Price Index.")
        .def(py::init<>(),
            "Constructs ZACPI without a term structure.")
        .def(py::init<const Handle<ZeroInflationTermStructure>&>(),
            py::arg("h"),
            "Constructs ZACPI with a term structure handle.")
        .def(py::init([](const ext::shared_ptr<ZeroInflationTermStructure>& ts) {
            return ext::make_shared<ZACPI>(
                Handle<ZeroInflationTermStructure>(ts));
        }),
            py::arg("zeroInflationTermStructure"),
            "Constructs ZACPI with a term structure.");

    // YYZACPI - Year-on-year South African CPI
    py::class_<YYZACPI, YoYInflationIndex, ext::shared_ptr<YYZACPI>>(
        m, "YYZACPI", "Year-on-year South African Consumer Price Index.")
        .def(py::init<>(),
            "Constructs YYZACPI without a term structure.")
        .def(py::init<const Handle<YoYInflationTermStructure>&>(),
            py::arg("h"),
            "Constructs YYZACPI with a term structure handle.")
        .def(py::init([](const ext::shared_ptr<YoYInflationTermStructure>& ts) {
            return ext::make_shared<YYZACPI>(
                Handle<YoYInflationTermStructure>(ts));
        }),
            py::arg("yoyInflationTermStructure"),
            "Constructs YYZACPI with a term structure.");
}
