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
#include <ql/termstructures/credit/flathazardrate.hpp>
#include <ql/quote.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_termstructures::flathazardrate(py::module_& m) {
    py::class_<FlatHazardRate, DefaultProbabilityTermStructure,
               ext::shared_ptr<FlatHazardRate>>(
        m, "FlatHazardRate",
        "Flat hazard rate term structure.")
        // Date + Rate
        .def(py::init<const Date&, Rate, const DayCounter&>(),
            py::arg("referenceDate"),
            py::arg("hazardRate"),
            py::arg("dayCounter"),
            "Constructs from date and hazard rate.")
        // Date + Quote handle
        .def(py::init<const Date&, Handle<Quote>, const DayCounter&>(),
            py::arg("referenceDate"),
            py::arg("hazardRate"),
            py::arg("dayCounter"),
            "Constructs from date and hazard rate quote handle.")
        // Hidden handle: Date + shared_ptr<Quote>
        .def(py::init([](const Date& refDate,
                         const ext::shared_ptr<Quote>& quote,
                         const DayCounter& dc) {
            return ext::make_shared<FlatHazardRate>(
                refDate, Handle<Quote>(quote), dc);
        }),
            py::arg("referenceDate"),
            py::arg("hazardRate"),
            py::arg("dayCounter"),
            "Constructs from date and hazard rate quote.")
        // Settlement days + Calendar + Rate
        .def(py::init<Natural, const Calendar&, Rate, const DayCounter&>(),
            py::arg("settlementDays"),
            py::arg("calendar"),
            py::arg("hazardRate"),
            py::arg("dayCounter"),
            "Constructs from settlement days and hazard rate.")
        // Settlement days + Calendar + Quote handle
        .def(py::init<Natural, const Calendar&, Handle<Quote>,
                       const DayCounter&>(),
            py::arg("settlementDays"),
            py::arg("calendar"),
            py::arg("hazardRate"),
            py::arg("dayCounter"),
            "Constructs from settlement days and hazard rate quote handle.")
        .def("maxDate", &FlatHazardRate::maxDate, "Maximum date.");
}
