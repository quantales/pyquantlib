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
#include <ql/indexes/inflation/euhicp.hpp>
#include <ql/termstructures/inflationtermstructure.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_indexes::euhicp(py::module_& m) {
    // EUHICP - EU Harmonised Index of Consumer Prices (zero inflation)
    py::class_<EUHICP, ZeroInflationIndex, ext::shared_ptr<EUHICP>>(
        m, "EUHICP", "EU Harmonised Index of Consumer Prices.")
        .def(py::init<>(),
            "Constructs EUHICP without a term structure.")
        .def(py::init<const Handle<ZeroInflationTermStructure>&>(),
            py::arg("h"),
            "Constructs EUHICP with a term structure handle.")
        .def(py::init([](const ext::shared_ptr<ZeroInflationTermStructure>& ts) {
            return ext::make_shared<EUHICP>(
                Handle<ZeroInflationTermStructure>(ts));
        }),
            py::arg("zeroInflationTermStructure"),
            "Constructs EUHICP with a term structure.");

    // EUHICPXT - EU HICP Excluding Tobacco (zero inflation)
    py::class_<EUHICPXT, ZeroInflationIndex, ext::shared_ptr<EUHICPXT>>(
        m, "EUHICPXT", "EU HICP Excluding Tobacco.")
        .def(py::init<>(),
            "Constructs EUHICPXT without a term structure.")
        .def(py::init<const Handle<ZeroInflationTermStructure>&>(),
            py::arg("h"),
            "Constructs EUHICPXT with a term structure handle.")
        .def(py::init([](const ext::shared_ptr<ZeroInflationTermStructure>& ts) {
            return ext::make_shared<EUHICPXT>(
                Handle<ZeroInflationTermStructure>(ts));
        }),
            py::arg("zeroInflationTermStructure"),
            "Constructs EUHICPXT with a term structure.");

    // YYEUHICP - Year-on-year EU HICP
    py::class_<YYEUHICP, YoYInflationIndex, ext::shared_ptr<YYEUHICP>>(
        m, "YYEUHICP", "Year-on-year EU HICP.")
        .def(py::init<>(),
            "Constructs YYEUHICP without a term structure.")
        .def(py::init<const Handle<YoYInflationTermStructure>&>(),
            py::arg("h"),
            "Constructs YYEUHICP with a term structure handle.")
        .def(py::init([](const ext::shared_ptr<YoYInflationTermStructure>& ts) {
            return ext::make_shared<YYEUHICP>(
                Handle<YoYInflationTermStructure>(ts));
        }),
            py::arg("yoyInflationTermStructure"),
            "Constructs YYEUHICP with a term structure.");

    // YYEUHICPXT - Year-on-year EU HICP Excluding Tobacco
    py::class_<YYEUHICPXT, YoYInflationIndex, ext::shared_ptr<YYEUHICPXT>>(
        m, "YYEUHICPXT", "Year-on-year EU HICP Excluding Tobacco.")
        .def(py::init<>(),
            "Constructs YYEUHICPXT without a term structure.")
        .def(py::init<const Handle<YoYInflationTermStructure>&>(),
            py::arg("h"),
            "Constructs YYEUHICPXT with a term structure handle.")
        .def(py::init([](const ext::shared_ptr<YoYInflationTermStructure>& ts) {
            return ext::make_shared<YYEUHICPXT>(
                Handle<YoYInflationTermStructure>(ts));
        }),
            py::arg("yoyInflationTermStructure"),
            "Constructs YYEUHICPXT with a term structure.");
}
