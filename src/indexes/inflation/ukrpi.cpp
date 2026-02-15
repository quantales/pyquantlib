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
#include <ql/indexes/inflation/ukrpi.hpp>
#include <ql/termstructures/inflationtermstructure.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_indexes::ukrpi(py::module_& m) {
    // UKRPI - UK Retail Prices Index (zero inflation)
    py::class_<UKRPI, ZeroInflationIndex, ext::shared_ptr<UKRPI>>(
        m, "UKRPI", "UK Retail Prices Index.")
        .def(py::init<>(),
            "Constructs UKRPI without a term structure.")
        .def(py::init<const Handle<ZeroInflationTermStructure>&>(),
            py::arg("h"),
            "Constructs UKRPI with a term structure handle.")
        .def(py::init([](const ext::shared_ptr<ZeroInflationTermStructure>& ts) {
            return ext::make_shared<UKRPI>(
                Handle<ZeroInflationTermStructure>(ts));
        }),
            py::arg("zeroInflationTermStructure"),
            "Constructs UKRPI with a term structure.");

    // YYUKRPI - Year-on-year UK RPI
    py::class_<YYUKRPI, YoYInflationIndex, ext::shared_ptr<YYUKRPI>>(
        m, "YYUKRPI", "Year-on-year UK Retail Prices Index.")
        .def(py::init<>(),
            "Constructs YYUKRPI without a term structure.")
        .def(py::init<const Handle<YoYInflationTermStructure>&>(),
            py::arg("h"),
            "Constructs YYUKRPI with a term structure handle.")
        .def(py::init([](const ext::shared_ptr<YoYInflationTermStructure>& ts) {
            return ext::make_shared<YYUKRPI>(
                Handle<YoYInflationTermStructure>(ts));
        }),
            py::arg("yoyInflationTermStructure"),
            "Constructs YYUKRPI with a term structure.");
}
