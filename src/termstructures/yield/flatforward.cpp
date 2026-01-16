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
#include <ql/termstructures/yield/flatforward.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_termstructures::flatforward(py::module_& m) {
    py::class_<FlatForward, ext::shared_ptr<FlatForward>, YieldTermStructure>(
        m, "FlatForward",
        "Flat interest-rate curve.")
        // Reference date + rate
        .def(py::init<const Date&, Rate, const DayCounter&, Compounding, Frequency>(),
            py::arg("referenceDate"),
            py::arg("forward"),
            py::arg("dayCounter"),
            py::arg("compounding") = Continuous,
            py::arg("frequency") = Annual,
            "Constructs from reference date and forward rate.")
        // Reference date + quote handle
        .def(py::init<const Date&, const Handle<Quote>&, const DayCounter&,
                      Compounding, Frequency>(),
            py::arg("referenceDate"),
            py::arg("forward"),
            py::arg("dayCounter"),
            py::arg("compounding") = Continuous,
            py::arg("frequency") = Annual,
            "Constructs from reference date and quote handle.")
        // Settlement days + rate
        .def(py::init<Natural, const Calendar&, Rate, const DayCounter&,
                      Compounding, Frequency>(),
            py::arg("settlementDays"),
            py::arg("calendar"),
            py::arg("forward"),
            py::arg("dayCounter"),
            py::arg("compounding") = Continuous,
            py::arg("frequency") = Annual,
            "Constructs from settlement days and forward rate.")
        // Settlement days + quote handle
        .def(py::init<Natural, const Calendar&, const Handle<Quote>&,
                      const DayCounter&, Compounding, Frequency>(),
            py::arg("settlementDays"),
            py::arg("calendar"),
            py::arg("forward"),
            py::arg("dayCounter"),
            py::arg("compounding") = Continuous,
            py::arg("frequency") = Annual,
            "Constructs from settlement days and quote handle.")
        .def("compounding", &FlatForward::compounding,
            "Returns the compounding convention.")
        .def("compoundingFrequency", &FlatForward::compoundingFrequency,
            "Returns the compounding frequency.");
}
