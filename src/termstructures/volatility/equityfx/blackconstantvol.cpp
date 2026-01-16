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
#include <ql/termstructures/volatility/equityfx/blackconstantvol.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_termstructures::blackconstantvol(py::module_& m) {
    py::class_<BlackConstantVol, BlackVolatilityTermStructure,
               ext::shared_ptr<BlackConstantVol>>(
        m, "BlackConstantVol",
        "Constant Black volatility term structure.")
        // Reference date + volatility value
        .def(py::init<const Date&, const Calendar&, Volatility, const DayCounter&>(),
            py::arg("referenceDate"),
            py::arg("calendar"),
            py::arg("volatility"),
            py::arg("dayCounter"),
            "Constructs from reference date and constant volatility.")
        // Reference date + quote handle
        .def(py::init<const Date&, const Calendar&, Handle<Quote>, const DayCounter&>(),
            py::arg("referenceDate"),
            py::arg("calendar"),
            py::arg("volatility"),
            py::arg("dayCounter"),
            "Constructs from reference date and quote handle.")
        // Settlement days + volatility value
        .def(py::init<Natural, const Calendar&, Volatility, const DayCounter&>(),
            py::arg("settlementDays"),
            py::arg("calendar"),
            py::arg("volatility"),
            py::arg("dayCounter"),
            "Constructs from settlement days and constant volatility.")
        // Settlement days + quote handle
        .def(py::init<Natural, const Calendar&, Handle<Quote>, const DayCounter&>(),
            py::arg("settlementDays"),
            py::arg("calendar"),
            py::arg("volatility"),
            py::arg("dayCounter"),
            "Constructs from settlement days and quote handle.");
}
