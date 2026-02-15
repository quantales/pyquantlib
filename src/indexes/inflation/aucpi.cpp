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
#include <ql/indexes/inflation/aucpi.hpp>
#include <ql/termstructures/inflationtermstructure.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_indexes::aucpi(py::module_& m) {
    // AUCPI - Australian CPI (zero inflation)
    py::class_<AUCPI, ZeroInflationIndex, ext::shared_ptr<AUCPI>>(
        m, "AUCPI", "Australian Consumer Price Index.")
        .def(py::init<Frequency, bool>(),
            py::arg("frequency"),
            py::arg("revised"),
            "Constructs AUCPI without a term structure.")
        .def(py::init<Frequency, bool,
                       const Handle<ZeroInflationTermStructure>&>(),
            py::arg("frequency"),
            py::arg("revised"),
            py::arg("h"),
            "Constructs AUCPI with a term structure handle.")
        .def(py::init([](Frequency frequency, bool revised,
                         const ext::shared_ptr<ZeroInflationTermStructure>& ts) {
            return ext::make_shared<AUCPI>(
                frequency, revised,
                Handle<ZeroInflationTermStructure>(ts));
        }),
            py::arg("frequency"),
            py::arg("revised"),
            py::arg("zeroInflationTermStructure"),
            "Constructs AUCPI with a term structure.");

    // YYAUCPI - Year-on-year Australian CPI
    py::class_<YYAUCPI, YoYInflationIndex, ext::shared_ptr<YYAUCPI>>(
        m, "YYAUCPI", "Year-on-year Australian Consumer Price Index.")
        .def(py::init<Frequency, bool>(),
            py::arg("frequency"),
            py::arg("revised"),
            "Constructs YYAUCPI without a term structure.")
        .def(py::init<Frequency, bool,
                       const Handle<YoYInflationTermStructure>&>(),
            py::arg("frequency"),
            py::arg("revised"),
            py::arg("h"),
            "Constructs YYAUCPI with a term structure handle.")
        .def(py::init([](Frequency frequency, bool revised,
                         const ext::shared_ptr<YoYInflationTermStructure>& ts) {
            return ext::make_shared<YYAUCPI>(
                frequency, revised,
                Handle<YoYInflationTermStructure>(ts));
        }),
            py::arg("frequency"),
            py::arg("revised"),
            py::arg("yoyInflationTermStructure"),
            "Constructs YYAUCPI with a term structure.");
}
