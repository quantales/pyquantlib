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
#include <ql/indexes/inflation/uscpi.hpp>
#include <ql/termstructures/inflationtermstructure.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_indexes::uscpi(py::module_& m) {
    // USCPI - US Consumer Price Index (zero inflation)
    py::class_<USCPI, ZeroInflationIndex, ext::shared_ptr<USCPI>>(
        m, "USCPI", "US Consumer Price Index.")
        .def(py::init<>(),
            "Constructs USCPI without a term structure.")
        .def(py::init<const Handle<ZeroInflationTermStructure>&>(),
            py::arg("h"),
            "Constructs USCPI with a term structure handle.")
        .def(py::init([](const ext::shared_ptr<ZeroInflationTermStructure>& ts) {
            return ext::make_shared<USCPI>(
                Handle<ZeroInflationTermStructure>(ts));
        }),
            py::arg("zeroInflationTermStructure"),
            "Constructs USCPI with a term structure.");

    // YYUSCPI - Year-on-year US CPI
    py::class_<YYUSCPI, YoYInflationIndex, ext::shared_ptr<YYUSCPI>>(
        m, "YYUSCPI", "Year-on-year US Consumer Price Index.")
        .def(py::init<>(),
            "Constructs YYUSCPI without a term structure.")
        .def(py::init<const Handle<YoYInflationTermStructure>&>(),
            py::arg("h"),
            "Constructs YYUSCPI with a term structure handle.")
        .def(py::init([](const ext::shared_ptr<YoYInflationTermStructure>& ts) {
            return ext::make_shared<YYUSCPI>(
                Handle<YoYInflationTermStructure>(ts));
        }),
            py::arg("yoyInflationTermStructure"),
            "Constructs YYUSCPI with a term structure.");
}
