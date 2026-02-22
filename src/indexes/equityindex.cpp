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
#include <ql/indexes/equityindex.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <ql/quote.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_indexes::equityindex(py::module_& m) {
    py::class_<EquityIndex, Index, ext::shared_ptr<EquityIndex>>(
        m, "EquityIndex",
        "Base class for equity indexes.")
        // Minimal constructor (name, calendar, currency only)
        .def(py::init([](const std::string& name, const Calendar& fixingCalendar,
                         const Currency& currency) {
            return ext::make_shared<EquityIndex>(name, fixingCalendar, currency);
        }),
            py::arg("name"),
            py::arg("fixingCalendar"),
            py::arg("currency"),
            "Constructs an equity index without curves or spot.")
        // Full constructor with Handles
        .def(py::init<std::string, Calendar, Currency,
                      Handle<YieldTermStructure>,
                      Handle<YieldTermStructure>,
                      Handle<Quote>>(),
            py::arg("name"),
            py::arg("fixingCalendar"),
            py::arg("currency"),
            py::arg("interest"),
            py::arg("dividend"),
            py::arg("spot"),
            "Constructs an equity index with term structure handles.")
        // Hidden handle constructor
        .def(py::init([](const std::string& name, const Calendar& fixingCalendar,
                         const Currency& currency,
                         const ext::shared_ptr<YieldTermStructure>& interest,
                         const ext::shared_ptr<YieldTermStructure>& dividend,
                         const ext::shared_ptr<Quote>& spot) {
            return ext::make_shared<EquityIndex>(
                name, fixingCalendar, currency,
                interest ? Handle<YieldTermStructure>(interest) : Handle<YieldTermStructure>(),
                dividend ? Handle<YieldTermStructure>(dividend) : Handle<YieldTermStructure>(),
                spot ? Handle<Quote>(spot) : Handle<Quote>());
        }),
            py::arg("name"),
            py::arg("fixingCalendar"),
            py::arg("currency"),
            py::arg("interest"),
            py::arg("dividend"),
            py::arg("spot"),
            "Constructs an equity index (handles created internally).")
        // Inspectors
        .def("currency", &EquityIndex::currency,
            "Returns the index currency.")
        .def("equityInterestRateCurve", &EquityIndex::equityInterestRateCurve,
            "Returns the interest rate curve handle.")
        .def("equityDividendCurve", &EquityIndex::equityDividendCurve,
            "Returns the dividend curve handle.")
        .def("spot", &EquityIndex::spot,
            "Returns the spot quote handle.")
        // Fixing calculations
        .def("forecastFixing", &EquityIndex::forecastFixing,
            py::arg("fixingDate"),
            "Returns the forecast fixing for the given date.")
        // Clone
        .def("clone", &EquityIndex::clone,
            py::arg("interest"),
            py::arg("dividend"),
            py::arg("spot"),
            "Returns a copy linked to different curves or spot.");
}
