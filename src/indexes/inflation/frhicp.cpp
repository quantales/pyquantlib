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
#include <ql/indexes/inflation/frhicp.hpp>
#include <ql/termstructures/inflationtermstructure.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_indexes::frhicp(py::module_& m) {
    // FRHICP - French HICP (zero inflation)
    py::class_<FRHICP, ZeroInflationIndex, ext::shared_ptr<FRHICP>>(
        m, "FRHICP", "French Harmonised Index of Consumer Prices.")
        .def(py::init<>(),
            "Constructs FRHICP without a term structure.")
        .def(py::init<const Handle<ZeroInflationTermStructure>&>(),
            py::arg("h"),
            "Constructs FRHICP with a term structure handle.")
        .def(py::init([](const ext::shared_ptr<ZeroInflationTermStructure>& ts) {
            return ext::make_shared<FRHICP>(
                Handle<ZeroInflationTermStructure>(ts));
        }),
            py::arg("zeroInflationTermStructure"),
            "Constructs FRHICP with a term structure.");

    // YYFRHICP - Year-on-year French HICP
    py::class_<YYFRHICP, YoYInflationIndex, ext::shared_ptr<YYFRHICP>>(
        m, "YYFRHICP", "Year-on-year French HICP.")
        .def(py::init<>(),
            "Constructs YYFRHICP without a term structure.")
        .def(py::init<const Handle<YoYInflationTermStructure>&>(),
            py::arg("h"),
            "Constructs YYFRHICP with a term structure handle.")
        .def(py::init([](const ext::shared_ptr<YoYInflationTermStructure>& ts) {
            return ext::make_shared<YYFRHICP>(
                Handle<YoYInflationTermStructure>(ts));
        }),
            py::arg("yoyInflationTermStructure"),
            "Constructs YYFRHICP with a term structure.");
}
